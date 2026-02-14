from __future__ import annotations

import sys
from collections import defaultdict
from contextvars import Token
from pathlib import Path
from typing import TYPE_CHECKING, Any

from aiofile import async_open
from fluent.runtime import FluentBundle, FluentResource
from fluent.runtime.bundle import Message

if TYPE_CHECKING:
    from bot.ext import Admonitions, CommandExemples, Context, TranslationBase

import asyncio

asyncio.Semaphore()


class TranslationEntry:
    __slots__ = ("bundle", "msg_id")

    def __init__(self, bundle: FluentBundle, msg_id: str) -> None:
        self.bundle: FluentBundle = bundle
        self.msg_id: str = msg_id

    def format(self, **kwargs: Any) -> str:
        msg = self.bundle.get_message(self.msg_id)
        if not msg or not msg.value:
            return f"{{missing_key: {self.msg_id}}}"
        text, _ = self.bundle.format_pattern(msg.value, kwargs)
        return text

    def get_message(self) -> Message:
        return self.bundle.get_message(self.msg_id)

    def __repr__(self) -> str:
        return f"TranslationEntry(id='{self.msg_id}')"


class TBase:
    _is_tbase = True
    _started = False
    prefix: str

    def __init__(self, parent: TranslationBase = None, file=None):
        self.parent: TranslationBase | None = parent
        self.lang_dict: LangDict = self.parent.lang_dict
        if file:
            asyncio.create_task(self.lang_dict.load_fluent_locales(Path(file).parent / "locales"))  # NOQA: RUF006

    def get_language(self, ctx: Context | str) -> str | None:
        if ctx:
            return ctx.user.language.lower() if ctx.user.language else None
        return ctx if type(ctx) is str and ctx in self.lang_dict else None

    def ctx_get(self) -> Context | None:
        return self.parent.ctx_get() if self.parent else None

    def ctx_set(self, ctx) -> Token | None:
        return self.parent.ctx_set(ctx) if self.parent else None

    @property
    def _cname(self):
        return sys._getframe(1).f_code.co_name

    def _untangle_any(self, ctx: Context, namespace: str) -> Any:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _untangle_any_lang(self, lang: str, namespace: str) -> Any:
        return self.lang_dict.get_lang(lang or "en", namespace)

    def _untangle_str(self, ctx: Context, namespace: str) -> str:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _untangle_commands(self, ctx: Context, namespace: str) -> CommandExemples:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _untangle_admonitions(self, ctx: Context, namespace: str) -> Admonitions:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _not_implemented(self) -> str:
        return self.parent.Exceptions.not_implemented().response_string

    def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
        return self._not_implemented()

    deco_helper: str = deco_helper

    def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
        return self._not_implemented()

    deco_usage: str = deco_usage

    def deco_description(self, ctx: Context, *args, **kwargs) -> str:
        return self._not_implemented()

    deco_description: str = deco_description

    def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:  # NOQA
        return CommandExemples([])

    deco_commands: CommandExemples = deco_commands

    def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:  # NOQA
        return Admonitions([])

    deco_admonitions: Admonitions = deco_admonitions

    def get_text(self, key: str, **kwargs) -> str:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_text(self.ctx_get(), key, prefix, **kwargs)

    def get_entry(self, key: str, **kwargs) -> TranslationEntry | None:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_entry(self.ctx_get(), key, prefix)

    def get_list(self, key: str, **kwargs) -> list[str]:
        raw = self.get_text(key, **kwargs)
        return [s.strip() for s in raw.split(",")]

    def get_text_by_lang(self, lang: str, key: str, **kwargs) -> str:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_text_by_lang(lang=lang, key=key, entry_prefix=prefix, **kwargs)

    def get_entry_by_lang(self, lang: str, key: str, **kwargs) -> TranslationEntry | None:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_entry_by_lang(lang=lang, key=key, entry_prefix=prefix)

    def get_list_by_lang(self, lang: str, key: str, include_en: bool = True, **kwargs) -> list[str]:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_list_by_lang(lang=lang, key=key, entry_prefix=prefix, include_en=include_en)

    def get_attributes_list(self, key: str, **kwargs) -> dict[str, list[str]]:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_attributes_list(self.ctx_get(), key, prefix)

    def get_attributes(self, key: str, **kwargs) -> dict[str, list[str]]:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_attributes(self.ctx_get(), key, prefix)


class ClassBase:
    def populate_subclasses(self, parent: object = None) -> None:
        try:
            for base_cls in self.__class__.__mro__:
                for name, cls in vars(base_cls).items():
                    if isinstance(cls, type) and getattr(cls, "_is_tbase", False):
                        setattr(self, name, cls(parent) if parent else cls())
        except Exception as e:
            print(e)


class LangDict:
    def __init__(self, parent: TranslationBase):
        self.parent = parent
        self._current_namespace: str | None = None
        self._skip_mode = False
        self._namespaces = defaultdict(dict)
        self._initialized = defaultdict(dict)
        self.semaphore = parent.bot.SemaphoreManager.get_semaphore("OI_Files", limit=50, burst_size=10)

    def define(self, lang: str | list[str], value: Any, namespace: str, msg_id: str):
        langs = [lang] if isinstance(lang, str) else lang

        for _lang in langs:
            l_lower = _lang.lower()
            if not isinstance(self._namespaces[namespace].get(l_lower), dict):
                self._namespaces[namespace][l_lower] = {}
            self._namespaces[namespace][l_lower][msg_id] = value
            self._initialized[namespace][l_lower] = True
        self._initialized[namespace]["__init__"] = True

    def is_initialized(self, namespace: str, lang: str | None = None) -> bool:
        if lang is None:
            return "__init__" in self._initialized[namespace]

        return self._initialized[namespace].get(lang.lower(), False)

    def get(self, namespace_or_lang: str, namespace: str | None = None):
        if namespace is None and namespace_or_lang in self._namespaces:
            return dict(self._namespaces[namespace_or_lang])
        if namespace is not None:
            return self._namespaces.get(namespace.lower(), {}).get(namespace_or_lang.lower())
        return None

    def get_namespace(self, namespace: str) -> dict[str, str]:
        return dict(self._namespaces[namespace])

    def get_lang(self, lang: str, namespace: str, fallback: str = "en") -> str | CommandExemples | Admonitions | None:
        return self._namespaces.get(namespace, {}).get(lang) or self._namespaces.get(namespace, {}).get(fallback)

    def get_lang_or_none(self, lang: str, namespace: str) -> str | CommandExemples | Admonitions | None:
        return self._namespaces.get(namespace, {}).get(lang) or None

    def __getitem__(self, item):
        raise KeyError("Direct access disabled — use get(lang, namespace) or get(namespace)")

    def get_lang_any(self, lang: str, namespace: str, key: str, fallback: str = "en") -> Any | None:
        messages = self._namespaces.get(namespace, {}).get(lang) or self._namespaces.get(namespace, {}).get(fallback)
        return messages.get(key) if isinstance(messages, dict) else None

    # async def load_fluent_locales(self, locales_path: Path):
    #     ftl_files = list(locales_path.glob("*.ftl"))
    #
    #     async def read_ftl(ftl_file: Path):
    #         lang_ = ftl_file.stem.lower()
    #
    #         async def get_bundle():
    #             async with async_open(ftl_file, "r", encoding="utf-8") as f:
    #                 content = await f.read()
    #                 resource = FluentResource(content)
    #                 bundle_ = FluentBundle([lang_], use_isolating=False)
    #                 bundle_.add_resource(resource)
    #                 return lang_, bundle_
    #
    #         if self.parent.bot.mock:
    #             return await get_bundle()
    #
    #         async with self.semaphore:
    #             return await get_bundle()
    #
    #     results = await asyncio.gather(*(read_ftl(f) for f in ftl_files))
    #     bundles: dict[str, FluentBundle] = dict(results)
    #
    #     if "pt_br" in bundles and "pt" not in bundles:
    #         bundles["pt"] = bundles["pt_br"]
    #     elif "pt" in bundles and "pt_br" not in bundles:
    #         bundles["pt_br"] = bundles["pt"]
    #
    #     for lang, bundle in bundles.items():
    #         for msg_id in bundle._messages:  # NOQA
    #             if "-" in msg_id:
    #                 prefix, internal_key = msg_id.split("-", 1)
    #             else:
    #                 prefix = "default"
    #                 internal_key = msg_id
    #
    #             entry = TranslationEntry(bundle, msg_id)
    #             self.define(lang, entry, prefix, internal_key)

    async def load_fluent_locales(self, locales_path: Path):
        ftl_files = list(locales_path.glob("*.ftl"))

        async def read_ftl(ftl_file: Path):
            lang_ = ftl_file.stem.lower()

            # Se for Mock, lê síncrono para evitar problemas de race condition no xdist
            if self.parent.bot.mock:
                with open(ftl_file, encoding="utf-8") as f:
                    content = f.read()
                return self._create_bundle(lang_, content)

            # Se for produção, usa o semáforo e aiofile
            async with self.semaphore, async_open(ftl_file, "r", encoding="utf-8") as f:
                content = await f.read()
                return self._create_bundle(lang_, content)

        results = await asyncio.gather(*(read_ftl(f) for f in ftl_files))
        bundles: dict[str, FluentBundle] = dict(results)

        if "pt_br" in bundles and "pt" not in bundles:
            bundles["pt"] = bundles["pt_br"]
        elif "pt" in bundles and "pt_br" not in bundles:
            bundles["pt_br"] = bundles["pt"]

        for lang, bundle in bundles.items():
            for msg_id in bundle._messages:  # NOQA
                if "-" in msg_id:
                    prefix, internal_key = msg_id.split("-", 1)
                else:
                    prefix = "default"
                    internal_key = msg_id

                entry = TranslationEntry(bundle, msg_id)
                self.define(lang, entry, prefix, internal_key)

    def _create_bundle(self, lang: str, content: str):
        resource = FluentResource(content)
        bundle = FluentBundle([lang], use_isolating=False)
        bundle.add_resource(resource)
        return lang, bundle

    def get_text(self, ctx: Context, key: str, entry_prefix: str = "default", **kwargs) -> str:
        lang = ctx.user.language or "en"
        entry: TranslationEntry | None = self.get_lang_any(lang.lower(), entry_prefix, key)
        return entry.format(**kwargs) if entry else f"{{missing: {key}}}"

    def get_entry(self, ctx, key: str, entry_prefix: str = "default") -> TranslationEntry | None:
        lang = ctx.user.language or "en"
        return self.get_lang_any(lang.lower(), entry_prefix, key)

    def get_list(self, ctx: Context, key: str) -> list[str]:
        raw = self.get_text(ctx, key)
        return [s.strip() for s in raw.split(",")]

    def get_text_by_lang(self, lang: str, key: str, entry_prefix: str = "default", **kwargs) -> str:
        entry: TranslationEntry | None = self.get_lang_any(lang.lower(), entry_prefix, key)
        if not entry:
            return f"{{missing: {entry_prefix}-{key}}}"
        return entry.format(**kwargs)

    def get_entry_by_lang(self, lang: str, key: str, entry_prefix: str = "default") -> TranslationEntry | None:
        return self.get_lang_any(lang.lower(), entry_prefix, key)

    def get_list_by_lang(
        self, lang: str, key: str, entry_prefix: str = "default", include_en: bool = True
    ) -> list[str]:
        raw = self.get_text_by_lang(lang.lower(), key, entry_prefix)
        current_list = [s.strip() for s in raw.split(",")] if "missing:" not in raw else []

        if include_en and lang.lower() != "en":
            raw_en = self.get_text_by_lang("en", key, entry_prefix)
            if "missing:" not in raw_en:
                en_list = [s.strip() for s in raw_en.split(",")]
                return list(dict.fromkeys(current_list + en_list))

        return current_list

    def get_attributes_list(self, ctx: Context, key: str, entry_prefix: str = "default") -> dict[str, list[str]]:
        entry = self.get_entry(ctx, key, entry_prefix)

        if not entry:
            return {}
        formatted = entry.get_message()
        if not formatted.attributes:
            return {}

        result = {}
        for attr_name, attr_value in formatted.attributes.items():
            items = [s.strip() for s in attr_value.value.split(",")]  # NOQA
            result[attr_name] = items
        return result

    def get_attributes(self, ctx: Context, key: str, entry_prefix: str = "default") -> dict[str, list[str]]:
        entry = self.get_entry(ctx, key, entry_prefix)

        if not entry:
            return {}
        formatted = entry.get_message()
        if not formatted.attributes:
            return {}

        return {attr_name: attr_value.value for attr_name, attr_value in formatted.attributes.items()}  # NOQA

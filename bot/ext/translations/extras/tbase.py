from __future__ import annotations

import inspect
from collections import defaultdict
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bot.ext import Admonitions, CommandExemples, Context


class TBase:
    _is_tbase = True

    def __init__(self):
        self.lang_dict: LangDict = LangDict()

    def get_language(self, ctx: Context | str) -> str | None:
        if ctx:
            return ctx.user.language.lower() if ctx.user.language else None
        return ctx if type(ctx) is str and ctx in self.lang_dict else None

    @property
    def _cname(self, depth=1):
        return inspect.stack()[depth].function

    def _untangle_any(self, ctx: Context, namespace: str) -> Any:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _untangle_str(self, ctx: Context, namespace: str) -> str:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _untangle_commands(self, ctx: Context, namespace: str) -> CommandExemples:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _untangle_admonitions(self, ctx: Context, namespace: str) -> Admonitions:
        return self.lang_dict.get_lang(self.get_language(ctx) or "en", namespace)

    def _not_implemented(self, ctx: Context, namespace: str) -> str:
        with self.lang_dict.once(self._cname):
            self.lang_dict.add_with("en", "Not implemented.")
            self.lang_dict.add_with(["pt_br", "pt"], "Não implementado.")
        return self._untangle_str(ctx, namespace=namespace)

    def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
        return self._not_implemented(ctx, namespace="not_implemented")

    deco_helper: str = deco_helper

    def deco_usage(self, ctx: Context, prefix: str | None = None, *args, **kwargs) -> str:
        return self._not_implemented(ctx, namespace="not_implemented")

    deco_usage: str = deco_usage

    def deco_description(self, ctx: Context, *args, **kwargs) -> str:
        return self._not_implemented(ctx, namespace="not_implemented")

    deco_description: str = deco_description

    def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:  # NOQA
        return CommandExemples([])

    deco_commands: CommandExemples = deco_commands

    def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:  # NOQA
        return Admonitions([])

    deco_admonitions: Admonitions = deco_admonitions


class ClassBase:
    def populate_subclasses(self, other_self: object = None) -> None:
        right_self = other_self or self
        for base_cls in right_self.__class__.__mro__:
            for name, cls in vars(base_cls).items():
                if isinstance(cls, type) and getattr(cls, "_is_tbase", False):
                    setattr(right_self, name, cls())


class LangDict:
    def __init__(self):
        self._namespaces: dict[str, dict[str, str]] = defaultdict(dict)
        self._current_namespace: str | None = None
        self._initialized: dict[str, bool] = defaultdict(bool)
        self._skip_mode = False

    @contextmanager
    def namespace(self, name: str):
        prev_namespace = self._current_namespace
        self._current_namespace = name
        try:
            yield self
        finally:
            self._current_namespace = prev_namespace

    @contextmanager
    def once(self, namespace: str):
        if not self._initialized[namespace]:
            self._skip_mode = False
            with self.namespace(namespace):
                yield
            self._initialized[namespace] = True
        else:
            self._skip_mode = True
            prev = self._current_namespace
            self._current_namespace = namespace
            try:
                yield
            finally:
                self._current_namespace = prev
            self._skip_mode = False

    def add(self, lang: str | list[str], value: str, namespace: str):
        if isinstance(lang, str):
            lang = [lang]
        for k in lang:
            self._namespaces[namespace.lower()][k.lower()] = value

    def add_with(self, lang: str | list[str], value: Any):
        if not self._current_namespace:
            raise RuntimeError("No active namespace. Use with 'with self.lang_dict.namespace(...)'")
        if self._skip_mode:
            return
        self.add(lang, value, self._current_namespace)

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

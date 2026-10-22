from __future__ import annotations

import sys
from collections import defaultdict
from contextvars import Token
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fluent.runtime import FluentBundle, FluentResource

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Admonitions, CommandExemples, Context, TranslationBase


class TranslationEntry:
    __slots__ = ("bundle", "msg_id")

    def __init__(self, bundle: FluentBundle, msg_id: str) -> None:
        self.bundle: FluentBundle = bundle
        self.msg_id: str = msg_id

    def format(self, **kwargs: Any) -> str:
        if not self.bundle.has_message(self.msg_id):
            return f"{{missing_key: {self.msg_id}}}"

        msg = self.bundle.get_message(self.msg_id)
        if not msg or not msg.value:
            return f"{{missing_key: {self.msg_id}}}"

        text, _ = self.bundle.format_pattern(msg.value, kwargs)
        return text if isinstance(text, str) else ""

    def get_message(self):
        return self.bundle.get_message(self.msg_id)

    def __repr__(self) -> str:
        return f"TranslationEntry(id='{self.msg_id}')"


class LangDict:
    def __init__(self, bot: Gorenmu):
        self.bot = bot
        # Cache de Bundles isolados por pasta e idioma: (folder_path, lang) -> FluentBundle
        self._bundles: dict[tuple[Path, str], FluentBundle] = {}

        # Armazenamento plano de mensagens: lang -> full_key -> TranslationEntry
        self._messages: defaultdict[str, dict[str, TranslationEntry]] = defaultdict(dict)

        # Mapeamento: prefixo_lower -> pasta locales
        self._prefix_to_folder: dict[str, Path] = {}
        self._unloaded_folders: set[Path] = set()

        # Rastreamento para reload limpo: folder_path -> set[(lang, full_key)]
        self._folder_to_keys: defaultdict[Path, set[tuple[str, str]]] = defaultdict(set)
        self._custom_data: defaultdict[str, dict[str, Any]] = defaultdict(dict)

    def _build_key(self, key: str, entry_prefix: str | None = None) -> str:
        if entry_prefix and entry_prefix.lower() != "default":
            return f"{entry_prefix}-{key}".lower()
        return key.lower()

    # -------------------------------------------------------------
    # Registro Explícito & Lazy Loading
    # -------------------------------------------------------------

    def _load_folder_sync(self, folder: Path):
        """Carrega todos os arquivos .ftl da pasta e cria os bundles isolados dela."""
        ftl_files = list(folder.glob("*.ftl"))
        resources_by_lang: defaultdict[str, list[str]] = defaultdict(list)

        for ftl_file in ftl_files:
            lang = ftl_file.stem.lower()
            try:
                content = ftl_file.read_text(encoding="utf-8")
                resources_by_lang[lang].append(content)
            except Exception:
                continue

        # Aliases para Português
        if "pt_br" in resources_by_lang and "pt" not in resources_by_lang:
            resources_by_lang["pt"] = list(resources_by_lang["pt_br"])
        elif "pt" in resources_by_lang and "pt_br" not in resources_by_lang:
            resources_by_lang["pt_br"] = list(resources_by_lang["pt"])

        for lang, contents in resources_by_lang.items():
            # Cria o bundle específico desta pasta para este idioma
            bundle = FluentBundle([lang], use_isolating=False)

            for raw_ftl in contents:
                bundle.add_resource(FluentResource(raw_ftl))

            self._bundles[(folder, lang)] = bundle

            for msg_id in list(bundle._messages.keys()):
                full_key = msg_id.lower()
                self._messages[lang][full_key] = TranslationEntry(bundle, msg_id)
                self._folder_to_keys[folder].add((lang, full_key))

    def _ensure_loaded(self, full_key: str):
        """Dispara a carga verificando prefixos compostos como 'anno-add'."""
        key_lower = full_key.lower()

        # 1. Tenta encontrar o prefixo exato registrado mais longo que casa com o início da chave
        matched_folder = None
        for registered_prefix, folder in self._prefix_to_folder.items():
            if key_lower.startswith(f"{registered_prefix}-") or key_lower == registered_prefix:
                matched_folder = folder
                break

        # 2. Se encontrou a pasta e ela ainda não foi carregada, carrega agora
        if matched_folder and matched_folder in self._unloaded_folders:
            self._unloaded_folders.remove(matched_folder)
            self._load_folder_sync(matched_folder)

    def register_domain(self, prefix: str, folder: Path):
        """Registra o prefixo associando-o à sua pasta locales."""
        folder_resolved = folder.resolve()
        p_lower = prefix.lower()

        self._prefix_to_folder[p_lower] = folder_resolved

        # Se a pasta ainda não foi lida na memória, adiciona na fila de pendentes
        if not any(f == folder_resolved for f, _ in self._bundles.keys()):
            self._unloaded_folders.add(folder_resolved)

    async def reload(self, target: str = "all") -> int:
        target_lower = target.strip().lower()

        # ---------------------------------------------------------
        # 1. Limpeza total ('all')
        # ---------------------------------------------------------
        if target_lower == "all":
            self._bundles.clear()
            self._messages.clear()
            self._folder_to_keys.clear()
            self._custom_data.clear()
            self._unloaded_folders = set(self._prefix_to_folder.values())
            return len(self._unloaded_folders)

        ns_prefix = f"{target_lower}-"
        for lang_dict in self._custom_data.values():
            keys_to_del = [k for k in lang_dict if k.startswith(ns_prefix) or k == target_lower]
            for k in keys_to_del:
                del lang_dict[k]

        folder = self._prefix_to_folder.get(target_lower)
        if not folder:
            # Mesmo que não tenha pasta .ftl (se for apenas um JSON/custom), já limpou o _custom_data
            return 1

        # Limpeza normal das traduções Fluent da pasta
        if folder in self._folder_to_keys:
            for lang, full_key in self._folder_to_keys[folder]:
                self._messages[lang].pop(full_key, None)
            del self._folder_to_keys[folder]

        keys_to_remove = [k for k in self._bundles if k[0] == folder]
        for k in keys_to_remove:
            del self._bundles[k]

        self._unloaded_folders.add(folder)
        return len(keys_to_remove) or 1

    # -------------------------------------------------------------
    # Métodos de Consumo
    # -------------------------------------------------------------

    def get_languages(self) -> list[str]:
        """Retorna todos os idiomas disponíveis nas pastas registradas."""
        langs: set[str] = set()
        for folder in self._prefix_to_folder.values():
            for file in folder.glob("*.ftl"):
                langs.add(file.stem.lower())

        if "pt_br" in langs:
            langs.add("pt")

        return sorted(list(langs)) if langs else ["en"]

    def get_lang_any(self, lang: str, key: str, fallback: str = "en") -> TranslationEntry | None:
        key_lower = key.lower()

        if key_lower not in self._messages.get(lang.lower(), {}):
            self._ensure_loaded(key_lower)

        messages = self._messages.get(lang.lower(), {})
        if key_lower in messages:
            return messages[key_lower]

        fallback_msgs = self._messages.get(fallback.lower(), {})
        return fallback_msgs.get(key_lower)

    def get_text(self, ctx: Any, key: str, entry_prefix: str = "default", **kwargs) -> str:
        lang = getattr(getattr(ctx, "user", None), "language", None) or "en"
        full_key = self._build_key(key, entry_prefix)
        entry: TranslationEntry | None = self.get_lang_any(lang.lower(), full_key)
        return entry.format(**kwargs) if entry else f"{{missing: {full_key}}}"

    def get_entry(self, ctx: Any, key: str, entry_prefix: str = "default") -> TranslationEntry | None:
        lang = getattr(getattr(ctx, "user", None), "language", None) or "en"
        full_key = self._build_key(key, entry_prefix)
        return self.get_lang_any(lang.lower(), full_key)

    def get_list(self, ctx: Any, key: str, entry_prefix: str = "default") -> list[str]:
        raw = self.get_text(ctx, key, entry_prefix=entry_prefix)
        return [s.strip() for s in raw.split(",")]

    def get_text_by_lang(self, lang: str, key: str, entry_prefix: str = "default", **kwargs) -> str:
        full_key = self._build_key(key, entry_prefix)
        entry: TranslationEntry | None = self.get_lang_any(lang.lower(), full_key)
        if not entry:
            return f"{{missing: {full_key}}}"
        return entry.format(**kwargs)

    def get_entry_by_lang(self, lang: str, key: str, entry_prefix: str = "default") -> TranslationEntry | None:
        full_key = self._build_key(key, entry_prefix)
        return self.get_lang_any(lang.lower(), full_key)

    def get_list_by_lang(
        self, lang: str, key: str, entry_prefix: str = "default", include_en: bool = True
    ) -> list[str]:
        full_key = self._build_key(key, entry_prefix)
        raw = self.get_text_by_lang(lang.lower(), key, entry_prefix)
        current_list = [s.strip() for s in raw.split(",")] if "missing:" not in raw else []

        if include_en and lang.lower() != "en":
            raw_en = self.get_text_by_lang("en", key, entry_prefix)
            if "missing:" not in raw_en:
                en_list = [s.strip() for s in raw_en.split(",")]
                return list(dict.fromkeys(current_list + en_list))

        return current_list

    def get_attributes_list(self, ctx: Any, key: str, entry_prefix: str = "default") -> dict[str, list[str]]:
        entry = self.get_entry(ctx, key, entry_prefix)
        if not entry:
            return {}
        formatted = entry.get_message()
        if not formatted or not getattr(formatted, "attributes", None):
            return {}

        result: dict[str, list[str]] = {}
        for attr_name, attr_value in formatted.attributes.items():
            result[attr_name] = [s.strip() for s in attr_value.value.split(",")]
        return result

    def get_attributes(self, ctx: Any, key: str, entry_prefix: str = "default") -> dict[str, str]:
        entry = self.get_entry(ctx, key, entry_prefix)
        if not entry:
            return {}
        formatted = entry.get_message()
        if not formatted or not getattr(formatted, "attributes", None):
            return {}

        return {attr_name: attr_value.value for attr_name, attr_value in formatted.attributes.items()}

    # -------------------------------------------------------------
    # Suporte a Dados Arbitrários Localizados (ex: Pets, Configs)
    # -------------------------------------------------------------

    def define(self, lang: str | list[str], value: Any, namespace: str, key: str):
        """Salva qualquer objeto customizado indexado por namespace/key e lang."""
        langs = [lang] if isinstance(lang, str) else lang
        full_key = f"{namespace}-{key}".lower()

        for _lang in langs:
            self._custom_data[_lang.lower()][full_key] = value

    def is_initialized(self, namespace: str) -> bool:
        """Verifica se algum dado desse namespace já foi inicializado."""
        ns_prefix = f"{namespace.lower()}-"
        for lang_dict in self._custom_data.values():
            if any(k.startswith(ns_prefix) for k in lang_dict):
                return True
        return False

    def get_raw(self, lang: str, namespace: str, key: str, fallback: str = "en") -> Any | None:
        """Recupera um objeto arbitrário salvo com fallback de idioma."""
        full_key = f"{namespace}-{key}".lower()
        l_lower = lang.lower()
        fb_lower = fallback.lower()

        return self._custom_data.get(l_lower, {}).get(full_key) or self._custom_data.get(fb_lower, {}).get(full_key)









class TBase:
    _is_tbase = True
    _started = False
    prefix: str
    parent: TranslationBase

    def __init__(self, parent: TranslationBase, file=None, is_base= False):
        self.parent: TranslationBase = parent
        self.lang_dict: LangDict = self.parent.lang_dict
        if file:
            self.locales_dir = Path(file).parent / "locales"
            self.parent.register_locale(self.prefix, is_base)

    def get_language(self, ctx: Context | str) -> str | None:
        if isinstance(ctx, str):
            return ctx if isinstance(ctx, str) and ctx in self.lang_dict else None
        return ctx.user.language.lower() if ctx.user.language else None

    def ctx_get(self) -> Context:
        return self.parent.ctx_get()

    def ctx_set(self, ctx) -> Token:
        return self.parent.ctx_set(ctx)

    @property
    def _cname(self):
        return sys._getframe(1).f_code.co_name

    def _not_implemented(self) -> str:
        return self.parent.Exceptions.not_implemented().response_string

    def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
        return self._not_implemented()

    def deco_usage(self, ctx: Context, prefix: str, *args, **kwargs) -> str:
        return self._not_implemented()

    def deco_description(self, ctx: Context, *args, **kwargs) -> str:
        return self._not_implemented()

    def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:  # NOQA
        return CommandExemples([])

    def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:  # NOQA
        return Admonitions([])

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

    def get_attributes(self, key: str, **kwargs) -> dict[str, str]:
        prefix = kwargs.pop("entry_prefix", self.prefix)
        return self.lang_dict.get_attributes(self.ctx_get(), key, prefix)


from __future__ import annotations

import datetime
import os
from hashlib import sha1
from typing import TYPE_CHECKING

import msgspec

from bot.ext import (
    Admonitions,
    CommandExemples,
    Response,
    TBase,
    TranslationBase,
)

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.models import Pets as DbPets

    from .pet import PetCmd


class PetRaw(msgspec.Struct):
    specie: dict[str, str]
    emoji: str
    price: int


def _load_json_data(_hash: str) -> dict[str, PetRaw]:
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_path, "extras", "pets.json")
    try:
        with open(path, "rb") as f:
            return msgspec.json.Decoder(dict[str, PetRaw]).decode(f.read())
    except (FileNotFoundError, msgspec.DecodeError):
        return {}


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: PetCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: PetCmd = parent
        self.populate_subclasses(parent=self)

    class Pet(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Pet"

        def pet_pat(self, name: str, emoji: str, emote: str):
            text = self.get_text(self._cname, name=name, emoji=emoji, emote=emote)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def pet_not_found(self, args) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        # --- Help Methods ---

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                    },
                ]
            )

    Pet: Pet

    class PetBuy(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "PetBuy"

        def no_cookies(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def not_enough_cookies(self, specie: str, price: int) -> Response:
            text = self.get_text(self._cname, specie=specie, price=price)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def pet_buy(self, specie: str, emoji: str, pet_id: int) -> Response:
            text = self.get_text(
                self._cname, specie=specie, emoji=emoji, prefix=self.ctx_get().prefix, command="pet name", pet_id=pet_id
            )
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def pet_list(self, pets: str) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix, pets=pets)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def not_found(self, specie: str) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix, specie=specie)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                    },
                    {
                        "args": self.get_text("cmd_ex2_args"),
                        "response": self.get_text("cmd_ex2_res"),
                    },
                ]
            )

    PetBuy: PetBuy

    class PetList(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "PetList"
            self.cache_hash = sha1(str(datetime.datetime.now().timestamp()).encode())

        def bot_name(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def mention_denied(self, name) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def pet(self, mention: str, pets: str) -> Response:
            text = self.get_text(self._cname, mention=mention, pets=pets)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def no_pets(self) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix, invocation="pet buy")
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def user_no_pets(self, mention: str) -> Response:
            text = self.get_text(self._cname, mention=mention)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                    },
                ]
            )

        def _internal_pets(self, lang: str | None = None) -> Pets:
            namespace = self._cname
            _internal_key = "_container"

            if not self.lang_dict.is_initialized(namespace):
                raw_data = _load_json_data(self.cache_hash.hexdigest())
                all_langs = {_lang for p in raw_data.values() for _lang in p.specie}
                all_langs.add("en")
                for _lang in all_langs:
                    localized_items: dict[str, PetType] = {}

                    for key, info in raw_data.items():
                        name = info.specie.get(_lang) or info.specie.get("en") or key
                        localized_items[key] = PetType(specie=name.lower(), emoji=info.emoji, price=info.price)
                    pets_instance = Pets(localized_items)
                    self.lang_dict.define(_lang, pets_instance, namespace, _internal_key)

            target_lang = (lang or self.ctx_get().user.language or "en").lower()
            manager = self.lang_dict.get_lang_any(target_lang, namespace, _internal_key) or self.lang_dict.get_lang_any(
                "en", namespace, _internal_key
            )

            return manager or Pets({})

        def get_pet(self, specie: str) -> PetType | None:
            return self._internal_pets().get(specie)

        def get_pets(self) -> Pets | None:
            return self._internal_pets()

        def get_formatted_pets(self, user_pets: list[DbPets], separator: str = " | ", show_id: bool = False) -> str:
            return self._internal_pets().format_list(user_pets, separator, show_id)

    PetList: PetList

    class PetName(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "PetName"

        def invalid_id(self, pet_id: str) -> Response:
            text = self.get_text(self._cname, pet_id=pet_id, prefix=self.ctx_get().prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def invalid_name(self, name: str, max_size: int) -> Response:
            text = self.get_text(self._cname, name=name, max_size=max_size)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def pet_renamed(self, pet_id: str, pet_name: str) -> Response:
            text = self.get_text(self._cname, pet_id=pet_id, pet_name=pet_name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

    PetName: PetName

    class PetSell(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Pet"

        def bot_name(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def price_not_int(self, price: str) -> Response:
            text = self.get_text(self._cname, price=price)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def price_third(self, price: int, minimum: int) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix, price=str(price), minimum=str(minimum))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def yourself(self) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def not_enough_cookies(self, name: str, amount: int) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix, name=name, amount=str(amount))
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_pets(self) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def start(self, user_name: str, pet_name: str) -> Response:
            text = self.get_text(self._cname, user_name=user_name, pet_name=pet_name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def sold(self, user: str, target: str) -> Response:
            text = self.get_text(self._cname, user=user, target=target)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def refused(self, user: str, target: str) -> Response:
            text = self.get_text(self._cname, user=user, target=target)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def timeout(self, pets: str) -> Response:
            text = self.get_text(self._cname, pets=pets)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def pet_not_find(self, pet_name) -> Response:
            text = self.get_text(self._cname, pet_name=pet_name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "prefix": self.get_text("cmd_ex1_prefix"),
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                    },
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "info",
                        "position": "top",
                        "title": self.get_text("adm_title"),
                        "message": self.get_text("adm_msg"),
                    }
                ]
            )

    PetSell: PetSell

    class PlaceHolder(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Pet"

        def bot_name(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def mention_denied(self, args) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def pet(self, mention: str, pets: str) -> Response:
            text = self.get_text(self._cname, mention=mention, pets=pets)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def no_pets(self) -> Response:
            text = self.get_text(self._cname, prefix=self.ctx_get().prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def user_no_pets(self, args) -> Response:
            text = self.get_text(self._cname, args=args)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        # --- Help Methods ---

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

        # region Hide.

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            return CommandExemples(
                [
                    {
                        "prefix": self.get_text("cmd_ex1_prefix"),
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                    },
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "info",
                        "position": "top",
                        "title": self.get_text("adm_title"),
                        "message": self.get_text("adm_msg"),
                    }
                ]
            )

        # endregion

    PlaceHolder: PlaceHolder


class PetType:
    def __init__(self, specie: str, emoji: str, price: int):
        self.specie = specie
        self.emoji = emoji
        self.price = price


class Pets:
    def __init__(self, items: dict[str, PetType]):
        self._items = items

    def list_all(self):
        return self._items.values()

    def get(self, specie: str) -> PetType | None:
        return self._items.get(specie)

    def format_list(self, user_pets: list[DbPets], separator: str = " | ", show_id: bool = False) -> str:
        formatted = []
        for p in user_pets:
            pet_data = self.get(p.specie)
            emoji = pet_data.emoji if pet_data else "❓"
            prefix = f"[{p.id}] " if show_id else ""
            formatted.append(f"{prefix}{p.name or p.specie} {emoji}")
        return separator.join(formatted)

from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu

    from .alias import AliasCmd
# TODO: The template generator for Alias


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu, parent: AliasCmd) -> None:
        super().__init__(bot, __file__)
        self.parent: AliasCmd = parent
        self.populate_subclasses(parent=self)

    class Table(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Table"

        def alias_table_headers(self) -> list[str]:
            return self.get_list(self._cname)

        def alias_table_replaces(self) -> list[str]:
            return self.get_list(self._cname)

        def alias_table_name(self, name: str) -> str:
            return self.get_text(self._cname, name=name)

    Table: Table

    class Alias(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Alias"

        def dont_have_alias(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_invalid_name(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def user_has_no_alias(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def deco_helper(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_usage(self, prefix: str | None = None, *args, **kwargs) -> str:
            return self.get_text(self._cname, prefix=prefix)

    Alias: Alias

    class Add(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Add"

        def no_command_to_add(self, prefix: str) -> Response:
            text = self.get_text(self._cname, prefix=prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_name_conflict(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_created(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def command_dont_exist(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
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
                        "suffix": self.get_text("cmd_ex1_suffix"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex2_prefix"),
                        "args": self.get_text("cmd_ex2_args", prefix=kwargs.get("prefix", "!")),
                        "response": self.get_text("cmd_ex2_res"),
                        "suffix": self.get_text("cmd_ex2_suffix", prefix=kwargs.get("prefix", "!")),
                    },
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "top",
                        "title": self.get_text("adm1_title"),
                        "message": self.get_text("adm1_msg"),
                    },
                    {
                        "admonition_type": "warning",
                        "position": "top",
                        "title": self.get_text("adm2_title"),
                        "message": self.get_text("adm2_msg"),
                    },
                ]
            )

    Add: Add

    class Check(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Check"

        def user_alias_list(self, names: str, url: str) -> Response:
            text = self.get_text(self._cname, names=names, url=url)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_alias_found(self, success: bool = False, handle: str | None = None, *args) -> Response:
            # Mapeando os args posicionais para nomes no FTL
            arg1 = args[0] if len(args) > 0 else ""
            arg2 = args[1] if len(args) > 1 else ""
            text = self.get_text(self._cname, alias_name=arg1, user_name=arg2)
            return Response(ctx=self.ctx_get(), success=success, handle=handle, response_string=text)

        def list_of_alias_of(self, mention: str, url: str) -> Response:
            text = self.get_text(self._cname, mention=mention, url=url)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def list_of_special_case(self, name: str, url1: str, url2: str) -> Response:
            text = self.get_text(self._cname, name=name, url1=url1, url2=url2)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def alias_not_found(self, mention: str, alias: str) -> Response:
            text = self.get_text(self._cname, mention=mention, alias=alias)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_deleted(self, alias: str) -> Response:
            text = self.get_text(self._cname, alias=alias)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def normal_message(self, name: str, invocation: str, url: str) -> Response:
            text = self.get_text(self._cname, name=name, invocation=invocation, url=url)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def appendix_message(self, parent: str, original: str, invocation: str, url: str) -> Response:
            text = self.get_text(self._cname, parent=parent, original=original, invocation=invocation, url=url)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def appendix(self, name: str, owner: str) -> str:
            return self.get_text(self._cname, name=name, owner=owner)

        def message(self, user: str, name: str, arg1: str, arg2: str) -> str:
            return self.get_text(self._cname, user=user, name=name, arg1=arg1, arg2=arg2)

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
                        "suffix": "",
                    }
                ]
            )

    Check: Check

    class Copy(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Copy"

        def alias_not_provided(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def target_alias_invalid_name(self, *args) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def no_alias_found(self, alias: str, name: str) -> Response:
            text = self.get_text(self._cname, alias=alias, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def link_to_a_link(self, prefix: str, user: str, target: str) -> Response:
            text = self.get_text(self._cname, prefix=prefix, user=user, target=target)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def copy_success(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def copy_with_name_of(self, target: str, name: str) -> Response:
            text = self.get_text(self._cname, target=target, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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
                        "suffix": self.get_text("cmd_ex1_suffix"),
                    }
                ]
            )

    Copy: Copy

    class Describe(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Describe"

        def no_args_to_parse(self, prefix: str) -> Response:
            text = self.get_text(self._cname, prefix=prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def description_updated(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def description_reverted(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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
                        "suffix": "",
                    }
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions([])

    Describe: Describe

    class Edit(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Edit"

        def no_args_provided(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def edit_link(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def edit_success(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def command_dont_exist(self, command: str) -> Response:
            text = self.get_text(self._cname, name=command)
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
                        "suffix": "",
                    }
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "warning",
                        "position": "bottom",
                        "title": self.get_text("adm1_title"),
                        "message": self.get_text("adm1_msg"),
                    }
                ]
            )

    Edit: Edit

    class Link(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Link"

        def link_no_args(self, prefix: str) -> Response:
            text = self.get_text(self._cname, prefix=prefix)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_name_already_exists(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def user_dont_has_alias(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def link_to_with_invalid_name(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def link_custom_name_invalid(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def link_to_link(self, target_name: str, user_name: str, alias_name: str) -> Response:
            text = self.get_text(self._cname, target_name=target_name, user_name=user_name, alias_name=alias_name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def link_success(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

        def link_name_string(self, name: str) -> str:
            return self.get_text(self._cname, name=name)

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
                        "suffix": "",
                    },
                    {
                        "prefix": self.get_text("cmd_ex2_prefix"),
                        "args": self.get_text("cmd_ex2_args"),
                        "response": self.get_text("cmd_ex2_res"),
                        "suffix": "",
                    },
                    {
                        "prefix": self.get_text("cmd_ex3_prefix"),
                        "args": self.get_text("cmd_ex3_args"),
                        "response": self.get_text("cmd_ex3_res"),
                        "suffix": "",
                    },
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions([])

    Link: Link

    class Remove(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Remove"

        def no_alias_name_provided(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_removed(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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
                        "suffix": self.get_text("cmd_ex1_suffix"),
                    }
                ]
            )

    Remove: Remove

    class Rename(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Rename"

        def no_name_provided(self) -> Response:
            text = self.get_text(self._cname)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_already_exists(self, name: str) -> Response:
            text = self.get_text(self._cname, name=name)
            return Response(ctx=self.ctx_get(), success=False, response_string=text)

        def alias_renamed(self, old: str, new: str) -> Response:
            text = self.get_text(self._cname, old=old, new=new)
            return Response(ctx=self.ctx_get(), success=True, response_string=text)

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
                        "suffix": "",
                    }
                ]
            )

    Rename: Rename

    class Extras(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Extras"

        def deco_description(self, *args, **kwargs) -> str:
            return self.get_text(self._cname)

        def deco_commands(self, *args, **kwargs) -> CommandExemples:
            p = kwargs.get("prefix", "!")
            return CommandExemples(
                [
                    {
                        "prefix": self.get_text("cmd_ex1_prefix"),
                        "args": self.get_text("cmd_ex1_args"),
                        "response": self.get_text("cmd_ex1_res"),
                        "suffix": "",
                    },
                    {
                        "prefix": self.get_text("cmd_ex2_prefix"),
                        "args": self.get_text("cmd_ex2_args", prefix=p),
                        "response": self.get_text("cmd_ex2_res"),
                        "suffix": self.get_text("cmd_ex2_suffix"),
                    },
                    {
                        "prefix": self.get_text("cmd_ex3_prefix"),
                        "args": self.get_text("cmd_ex3_args"),
                        "response": self.get_text("cmd_ex3_res"),
                        "suffix": "",
                    },
                ]
            )

        def deco_admonitions(self, *args, **kwargs) -> Admonitions:
            return Admonitions(
                [
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm1_title"),
                        "message": self.get_text("adm1_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm2_title"),
                        "message": self.get_text("adm2_msg"),
                    },
                    {
                        "admonition_type": "info",
                        "position": "bottom",
                        "title": self.get_text("adm3_title"),
                        "message": self.get_text("adm3_msg"),
                    },
                ]
            )

    Extras: Extras

    class Template(TBase):
        def __init__(self, parent: Translations):
            super().__init__(parent)
            self.prefix = "Template"

        def part1(self, command_title: str, rate: int, per: str, cooldown_type: str) -> str:
            return self.get_text(
                self._cname, command_title=command_title, rate=rate, per=per, cooldown_type=cooldown_type
            )

        def part2(self, description: str, aliases: str) -> str:
            return self.get_text(self._cname, description=description, aliases=aliases)

        def part3(self) -> str:
            return self.get_text(self._cname)

        def alias_template(self, command_title: str, aliases: str) -> str:
            return self.get_text(self._cname, command_title=command_title, aliases=aliases)

        def command_template(self, prefix: str, command_name: str, args: str, response: str) -> str:
            return self.get_text(self._cname, prefix=prefix, command_name=command_name, args=args, response=response)

        def admonition_template(self, type: str, title: str, message: str) -> str:
            return self.get_text(self._cname, type=type, title=title, message=message)

        def bucket_type(self, type_key: str) -> str:
            return self.get_text(self._cname, type=type_key)

    Template: Template

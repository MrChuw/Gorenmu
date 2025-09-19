# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context, commands


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    class Add(TBase):
        def __init__(self):
            super().__init__()

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to add an note.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para adicionar uma anotação.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}note add (text)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}note add (texto)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command is used to add annotation.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando serve para adicionar uma anotação.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {
                                "args": "add A note about something I want to be able to check forever.",
                                "response": "Note successfully created. 📝 (ID: (note ID))",
                            },
                            {
                                "args": 'add title:"title easier to remember" A note about something '
                                "I want to be able to check forever.",
                                "response": "Note successfully created. 📝 (ID: (note ID))",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "args": "add Uma anotação sobre algo que eu quero lembrar para sempre.",
                                "response": "Anotação criada com sucesso. 📝 (ID: <ID da nota>)",
                            },
                            {
                                "args": 'add title:"Título para facilitar" Uma anotação sobre algo '
                                "que eu quero lembrar para sempre.",
                                "response": "Anotação criada com sucesso. 📝 (ID: <ID da nota>)",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        def deco_admonitions(self, ctx: Context, *args, **kwargs) -> Admonitions:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "position": "bottom",
                                "title": "Maximum Length for 'add'!",
                                "message": "The message cannot exceed 450 characters; if it does, "
                                "an error will be returned.",
                            },
                            {
                                "admonition_type": "warning",
                                "position": "bottom",
                                "title": "Maximum Length for 'add' Title!",
                                "message": "The title cannot exceed 32 characters; if it does, "
                                "an error will be returned.",
                            },
                            {
                                "admonition_type": "tip",
                                "position": "top",
                                "title": "Annotations and Aliases",
                                "message": "Use aliases and notes together to create custom commands. "
                                "For example, with +alias add cakes note check (id), you can "
                                "use ++cakes to have the bot automatically send the note "
                                "content, without needing to use the full command note "
                                "check (id).",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "position": "bottom",
                                "title": "Limite máximo de caracteres para 'add'!",
                                "message": "A mensagem não pode exceder 450 caracteres. "
                                "Se exceder, um erro será retornado.",
                            },
                            {
                                "admonition_type": "warning",
                                "position": "bottom",
                                "title": "Limite máximo para o título!",
                                "message": "O título não pode ter mais de 32 caracteres. "
                                "Se exceder, um erro será retornado.",
                            },
                            {
                                "admonition_type": "tip",
                                "position": "top",
                                "title": "Notas e Aliases",
                                "message": "Use aliases e notas juntos para criar comandos personalizados. "
                                "Por exemplo, com `{prefix}alias add bolo note check <id>`, "
                                "você pode usar `{prefix}{prefix}bolo` para que o bot envie "
                                "automaticamente o conteúdo da anotação, sem precisar digitar o "
                                "comando completo `note check <id>`.",
                            },
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

    Add: Add

    class Check(TBase):
        def __init__(self):
            super().__init__()

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to check infos for an note.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para verificar uma anotação.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}note check (id)")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}note check (id)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to check an annotation.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando serve para consultar uma anotação.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "check", "response": "Your notes are those with ID: (title if available [id])"},
                            {"args": "check (id)", "response": "(Note content)"},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "check", "response": "Suas anotações são: <título se houver [id]>"},
                            {"args": "check <id>", "response": "<Conteúdo da anotação.>"},
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

    Check: Check

    class Delete(TBase):
        def __init__(self):
            super().__init__()

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to delete an note.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este subcomando é usado para deletar uma anotação.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "How to use: {}note delete cool_name")
                self.lang_dict.add_with(["pt_br", "pt"], "Como usar: {}note delete (id)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This subcommand is used to delete an annotation.")
                self.lang_dict.add_with(["pt_br", "pt"], "Este comando serve para excluir uma anotação.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [{"args": "delete (id)", "response": "Your note with ID (id) was successfully deleted. 🗑"}]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [{"args": "delete <id>", "response": "Sua anotação com ID <id> foi excluída com sucesso. 🗑"}]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

    Delete: Delete

    class Annotations(TBase):
        def __init__(self):
            super().__init__()

        def title_too_long(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The title must have a maximum of 32 characters.")
                self.lang_dict.add_with(["pt_br", "pt"], "O título deve ter um máximo de 32 caracteres.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def too_few_characters(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You forgot to send the annotation content.")
                self.lang_dict.add_with(["pt_br", "pt"], "Você se esqueceu de enviar o conteúdo da anotação.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def annotation_created(self, ctx: Context, note_id) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Note successfully created. 📝 (ID: {})")
                self.lang_dict.add_with(["pt_br", "pt"], "Nota criada com sucesso. 📝 (ID: {})")
            return response.format_response(self._untangle_str(ctx, self._cname), note_id)

        def no_annotations_with_id(self, ctx: Context, note_id) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You don't have any annotation with ID {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "Você não tem nenhuma anotação com ID {}.")
            return response.format_response(self._untangle_str(ctx, self._cname), note_id)

        def all_annotations(self, ctx: Context, note_id) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Your annotations are the ones with ID: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "Suas anotações são aquelas com ID: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), note_id)

        def annotation_content(self, ctx: Context, content) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), content)

        def deleted(self, ctx: Context, note_id) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Your annotation with ID {} was successfully deleted. 🗑")
                self.lang_dict.add_with(["pt_br", "pt"], "Sua anotação com ID {} foi excluída com sucesso. 🗑")
            return response.format_response(self._untangle_str(ctx, self._cname), note_id)

        def option_not_recognized(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", 'The valid options are only "add" "check" "delete"')
                self.lang_dict.add_with(["pt_br", "pt"], 'As opções válidas são apenas "add" "check" "delete"')
            return response.format_response(self._untangle_str(ctx, self._cname))

        def no_annotation_present(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You don't have any annotations saved.")
                self.lang_dict.add_with(["pt_br", "pt"], "Você não tem nenhuma anotação salva.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Creates permanent notes for the user.")
                self.lang_dict.add_with(["pt_br", "pt"], "Cria notas permanentes para o usuário.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}note add/check/delete")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}note add/check/delete")
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Creates permanent notes for the user.")
                self.lang_dict.add_with(["pt_br", "pt"], "Cria notas permanentes para o usuário.")
            return self._untangle_str(ctx, self._cname)

    Annotations: Annotations

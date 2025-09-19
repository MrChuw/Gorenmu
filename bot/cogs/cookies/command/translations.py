# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING

from bot.ext import Admonitions, CommandExemples, Response, TBase, TranslationBase

if TYPE_CHECKING:
    from bot.bot import Gorenmu
    from bot.ext import Context
    from bot.models import Cookies


class Translations(TranslationBase):
    def __init__(self, bot: Gorenmu) -> None:
        super().__init__(bot)
        self.populate_subclasses()

    # region Hide.

    class Cookies(TBase):
        def __init__(self):
            super().__init__()

        def invalid_option(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", 'Choose from one of the options "eat", "count", "top", "gift", "stock" or "sm"'
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], 'Escolha entre uma das opções "eat", "count", "top", "gift", "stock" ou "sm"'
                )
            return response.format_response(self._untangle_str(ctx, self._cname))

        def daily_limit_reached(self, ctx: Context, cooldown) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You're still on cooldown, wait {} until the next batch! ⌛")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Você ainda está em cooldown, espere {} até o próximo lote! ⌛"
                )
            return response.format_response(self._untangle_str(ctx, self._cname), cooldown)

        def user_not_found(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "user @{} has not yet been registered and has not used any cookie commands."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "o usuário @{} ainda não foi registrado e não usou nenhum comando de cookie."
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def cookie_not_found(self, ctx: Context, name) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "User @{} has not yet used any command related to cookies.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "O usuário @{} ainda não usou nenhum comando relacionado aos cookies."
                )
            return response.format_response(self._untangle_str(ctx, self._cname), name)

        def all_string(self, ctx: Context) -> list[str]:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", ["all"])
                self.lang_dict.add_with(["pt_br", "pt"], ["todos"])
            return self._untangle_any(ctx, self._cname) + self.lang_dict.get_lang("en", self._cname)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command used to manage cookies.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando usado para gerenciar cookies.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}alias Eat|Count|Gift|Stock|Top|SlotMachine (options)")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Para usar: {}cookie Eat|Count|Gift|Stock|Top|SlotMachine (opções)"
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Command used to manage cookies.")
                self.lang_dict.add_with(["pt_br", "pt"], "Comando usado para gerenciar cookies.")
            return self._untangle_str(ctx, self._cname)

    Cookies: Cookies

    class Eat(TBase):
        def __init__(self):
            super().__init__()

        def not_eat(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You didn't eat anything, wow!")
                self.lang_dict.add_with(["pt_br", "pt"], "Você não comeu nada, nossa!")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def negative_eat(self, ctx: Context, amount) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To eat {} cookies, you must first know how to reverse entropy.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Para comer {} cookies, você deve primeiro saber como reverter entropia."
                )
            return response.format_response(self._untangle_str(ctx, self._cname), amount)

        def multiple_eat(self, ctx: Context, amount) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you ate {} cookies in one sitting. 🥠")
                self.lang_dict.add_with(["pt_br", "pt"], "você comeu {} cookies de uma só vez. 🥠")
            return response.format_response(self._untangle_str(ctx, self._cname), amount)

        def eat(self, ctx: Context, text) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(["pt_br", "pt", "en"], "{}")
            return response.format_response(self._untangle_str(ctx, self._cname), text)

        def random_line(self, ctx: Context) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", Path(__file__).parent / "extras" / "lines_en.txt")
                self.lang_dict.add_with(["pt_br", "pt"], Path(__file__).parent / "extras" / "lines_pt_br.txt")
            return random.choice(self._untangle_any(ctx, self._cname).read_text().split("\n"))

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Get your daily fortune.")
                self.lang_dict.add_with(["pt_br", "pt"], "Pegue seu biscoito da sorte diário.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}cookie eat")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}cookie eat")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "This command is used to get a daily fortune.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Este comando é usado para pegar seu biscoito da sorte diário."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", CommandExemples([{"args": "eat", "response": "(random fortune from a list)"}])
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples([{"args": "eat", "response": "(Mensagem de sorte aleatória de uma lista)"}]),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Eat: Eat

    class Count(TBase):
        def __init__(self):
            super().__init__()

        def cc_bot_nick(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "I have infinite cookies, and I give away a fraction of them to you.")
                self.lang_dict.add_with(["pt_br", "pt"], "Tenho cookies infinitos e dou uma fração deles para você.")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def _format_cookie_count(self, ctx: Context) -> dict[str, str]:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    {
                        "cookie_count": "{} already eaten {} cookies 🥠.",
                        "stocked_count": "Has {} in stock.",
                        "received_count": "Was presented with {}.",
                        "donated_count": "Gifted {}.",
                        "not_redeemed_count": "And has a total of {} unredeemed.",
                        "total_count": "And there were a total of {} cookies have already been added to the account.",
                    },
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    {
                        "cookie_count": "{} já comeu {} biscoitos 🥠.",
                        "stocked_count": "Tem {} em estoque.",
                        "received_count": "Foi apresentado com {}.",
                        "donated_count": "Presenteou {}.",
                        "not_redeemed_count": "E tem um total de {} não resgatados.",
                        "total_count": "E um total de {} cookies já foram adicionados à conta.",
                    },
                )

            return self._untangle_any(ctx, self._cname)

        def format_cookie_count(self, ctx: Context, mention: str, cookie: Cookies, verb: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            translations: dict[str, str] = self._format_cookie_count(ctx)
            fields = [
                ("cookie_count", (verb, cookie.consumed)),
                ("stocked_count", cookie.stocked),
                ("received_count", cookie.received),
                ("donated_count", cookie.donated),
                ("not_redeemed_count", cookie.not_redeemed()),
                ("total_count", cookie.total),
            ]
            parts = []
            for key, value in fields:
                if isinstance(value, tuple):
                    if value[1] > 0:
                        parts.append(translations[key].format(*value))
                elif value > 0:
                    parts.append(translations[key].format(value))
            if parts:
                parts[0] = parts[0].lower()

            response_str = f"{mention} {' '.join(parts)}".strip()
            return response.format_response(response_str)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Get status about cookies.")
                self.lang_dict.add_with(["pt_br", "pt"], "Veja o status dos cookies.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}cookie count (user_name)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}cookie count (nome_do_usuário)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Get status about cookies.")
                self.lang_dict.add_with(["pt_br", "pt"], "Veja quantos cookies você ou outra pessoa possuem.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "cc", "response": "(status about your cookie account)"},
                            {"args": "cc other_user", "response": "(status about other_user cookie account)"},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "cc", "response": "(Status sobre sua conta de cookies)"},
                            {
                                "args": "cc outro_usuário",
                                "response": "(Status sobre a conta de cookies do outro usuário)",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Count: Count

    class Gift(TBase):
        def __init__(self):
            super().__init__()

        def gift_bot_nick(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "I don't want your cookie.")
                self.lang_dict.add_with(["pt_br", "pt"], "Não quero a seu cookie.")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def gift_user_himself(self, ctx: Context) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Did you try gifting it yourself, wow!")
                self.lang_dict.add_with(["pt_br", "pt"], "você tentou presentear você mesmo, uau!")
            return response.format_response(self._untangle_str(ctx, self._cname))

        def gift_no_stock_but_cooldown(self, ctx: Context, amount) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To gift, you must first redeem the {} cookies you have available.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Para presentear, você deve primeiro resgatar os {} cookies que você tem disponíveis.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), amount)

        def not_gifted(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "You didn't gift anything, wow!")
                self.lang_dict.add_with(["pt_br", "pt"], "Você não deu nada de presente, uau!")
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def negative_gift(self, ctx: Context, *args) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "You can't give negative cookies unless you're a cookie thief... and you're not, right?"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Você não pode dar cookies negativos, a menos que seja um ladrão de cookies... "
                    "e você não é, certo?",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), args)

        def multiple_gift(self, ctx: Context, person: str, amount: int | float) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you gifted @{} with {} cookie 🎁")
                self.lang_dict.add_with(["pt_br", "pt"], "você presenteou @{} com {} cookie 🎁")
            return response.format_response(self._untangle_str(ctx, self._cname), person, amount)

        def gift(self, ctx: Context, person) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you gave @{} a cookie 🎁")
                self.lang_dict.add_with(["pt_br", "pt"], "você deu um cookie para @{} 🎁")
            return response.format_response(self._untangle_str(ctx, self._cname), person)

        def gift_on_cooldown_no_stock(self, ctx: Context, cooldown) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "You don’t have any cookies 🍪 stored or waiting to be redeemed. The next one arrives in {}."
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Você não tem nenhum cookie 🍪 armazenado ou aguardando para ser resgatado. O próximo chega em {}.",
                )
            return response.format_response(self._untangle_str(ctx, self._cname), cooldown)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Gift someone your daily cookie.")
                self.lang_dict.add_with(["pt_br", "pt"], "Presenteie alguém com seus cookies.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}cookie gift (user_name) (amount|all)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}cookie gift (nome_do_usuário) (quantidade|all)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Gift someone your daily cookie.")
                self.lang_dict.add_with(["pt_br", "pt"], "Presenteie alguém com seus cookies.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "gift other_user", "response": "you gifted @other_user with 1 cookie 🎁"},
                            {"args": "gift other_user 2", "response": "you gifted @other_user with 2 cookie 🎁"},
                            {
                                "args": "gift other_user all",
                                "response": "you gifted @other_user with (all the cookies in your account) cookie 🎁",
                            },
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "gift outro_usuário", "response": "Você deu 1 cookie 🎁 para @outro_usuário"},
                            {"args": "gift outro_usuário 2", "response": "Você deu 2 cookies 🎁 para @outro_usuário"},
                            {
                                "args": "gift outro_usuário all",
                                "response": "Você deu (todos os cookies da sua conta) 🎁 para @outro_usuário",
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
                                "position": "top",
                                "title": "Careful With All",
                                "message": "Be careful with all, because you will transfer not only the "
                                "unredeemed ones, but also the ones you have saved.",
                            }
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    Admonitions(
                        [
                            {
                                "admonition_type": "warning",
                                "position": "top",
                                "title": "Cuidado com o 'all'!",
                                "message": "Cuidado ao usar 'all', pois você irá transferir não apenas os "
                                "cookies não coletados, mas também os que você já armazenou.",
                            }
                        ]
                    ),
                )
            return self._untangle_admonitions(ctx, self._cname)

        # endregion

    Gift: Gift

    class Stock(TBase):
        def __init__(self):
            super().__init__()

        def stock(self, ctx: Context, amount) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you stocked {} cookies 🍪, the next one comes out in 6h.")
                self.lang_dict.add_with(["pt_br", "pt"], "você estocou {} cookies 🍪, o próximo sai em 6h.")
            return response.format_response(self._untangle_str(ctx, self._cname), amount)

        def stock_not_daily(self, ctx: Context, amount) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you stocked {} cookies 🍪.")
                self.lang_dict.add_with(["pt_br", "pt"], "você estocou {} cookies 🍪.")
            return response.format_response(self._untangle_str(ctx, self._cname), amount)

        def stock_not_enough_cookies(self, ctx: Context, amount) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you can only stock {} 🍪.")
                self.lang_dict.add_with(["pt_br", "pt"], "você só pode estocar {}.")
            return response.format_response(self._untangle_str(ctx, self._cname), amount)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Stock your daily cookie.")
                self.lang_dict.add_with(["pt_br", "pt"], "Estoque seus cookies diários para usar depois.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "To use: {}cookie stock (all)")
                self.lang_dict.add_with(["pt_br", "pt"], "Para usar: {}cookie stock (all)")
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Stock your daily cookie.")
                self.lang_dict.add_with(["pt_br", "pt"], "Guarde seus cookies diários em vez de usá-los imediatamente.")
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "stock", "response": "you stocked 1 cookies 🍪, the next one comes out in 6h."},
                            {"args": "stock all", "response": "you stocked (number of all available) cookies 🍪."},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {
                                "args": "stock",
                                "response": "Você estocou 1 cookie 🍪, o próximo estará disponível em 6h.",
                            },
                            {
                                "args": "stock all",
                                "response": "Você estocou (quantidade de todos disponíveis) cookies 🍪.",
                            },
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Stock: Stock

    class Top(TBase):
        def __init__(self):
            super().__init__()

        def rank_dict(self, ctx: Context) -> dict[str, list[str]]:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    {
                        "stocked": ["stocked", "stocked"],
                        "streak": ["streak", "streak"],
                        "consumed": ["consumed", "cookiers"],
                        "donated": ["donated", "givers"],
                        "received": ["received", "receivers"],
                        "total": ["total", "total"],
                    },
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    {
                        "stocked": ["stocked", "stocked"],
                        "streak": ["streak", "streak"],
                        "consumed": ["consumed", "cookiers"],
                        "donated": ["donated", "givers"],
                        "received": ["received", "receivers"],
                        "total": ["total", "total"],
                    },
                )
            return self._untangle_any(ctx, self._cname)

        def ranks(self, ctx: Context, ranks) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "the ranks are: {}")
                self.lang_dict.add_with(["pt_br", "pt"], "as categoria são: {}")
            return response.format_response(self._untangle_str(ctx, self._cname), ranks)

        def top10_ish(self, ctx: Context, length, title, tops, index, amount) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "top {} {}: {} || You are in the {}th position in the ranking with {}.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "top {} {}: {} || Você está na {}ª posição na classificação com {}."
                )
            return response.format_response(self._untangle_str(ctx, self._cname), length, title, tops, index, amount)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "See who are the top cookie eaters or donors.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Veja quem são os melhores comedores, doadores ou acumuladores de cookies."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    "To use: {}cookie top (or pass one of the options stocked "
                    "| streak | consumed | donated | received | total)",
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Para usar: {}cookie top (ou passe uma das opções stocked "
                    "| streak | consumed | donated | received | total)",
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "See who are the top cookie eaters or donors.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Veja quem são os melhores em acumular, doar, comer ou manter sequência de cookies.",
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "top", "response": "top 10 stocked: 🏆 @user_name: (10) 🥈 ..."},
                            {"args": "top donated", "response": "top 10 givers: 🏆 @user_name: (10) 🥈 ..."},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "top", "response": "Top 10 acumuladores: 🏆 @nome_usuário: (10) 🥈 ..."},
                            {"args": "top donated", "response": "Top 10 doadores: 🏆 @nome_usuário: (10) 🥈 ..."},
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    Top: Top

    # endregion

    class SlotMachine(TBase):
        def __init__(self):
            super().__init__()

        def invalid_amount(self, ctx: Context, amount: str, amount_available: int) -> Response:
            response = Response(ctx=ctx, success=False, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "you are trying to bet {} but you only have {} unredeemed cookies.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "você está tentando apostar {} mas só tem {} cookies não resgatados."
                )
            return response.format_response(self._untangle_str(ctx, self._cname), amount, amount_available)

        def cookie_win_suffix(self, ctx: Context, total: int, time_suffix: str) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "and earned {} cookies. {}")
                self.lang_dict.add_with(["pt_br", "pt"], "e ganhou {} cookies. {}")
            return self._untangle_str(ctx, self._cname).format(total, time_suffix)

        def cookie_loss_suffix(self, ctx: Context, time_suffix) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "and lost everything. {}")
                self.lang_dict.add_with(["pt_br", "pt"], "e perdeu tudo. {}")
            return self._untangle_str(ctx, self._cname).format(time_suffix)

        def accumulated_message(self, ctx: Context, prefix: str, amount: str, suffix: str, emote: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} You have used {} unredeemed cookie(s) {} {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} Você usou {} cookie(s) não resgatado(s) {} {}")
            return response.format_response(self._untangle_str(ctx, self._cname), prefix, amount, suffix, emote)

        def last_cookie_message(self, ctx: Context, prefix: str, suffix: str, emote: str) -> Response:
            response = Response(ctx=ctx, success=True, handle=None, response_list=None)
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "{} You used your last available cookie {} {}")
                self.lang_dict.add_with(["pt_br", "pt"], "{} Você usou seu último cookie disponível {} {}")
            return response.format_response(self._untangle_str(ctx, self._cname), prefix, suffix, emote)

        def time_suffix(self, ctx: Context, time) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "The next one is available in {}.")
                self.lang_dict.add_with(["pt_br", "pt"], "O próximo está disponível em {}.")
            return self._untangle_str(ctx, self._cname).format(time)

        def deco_helper(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Bet your daily cookie for a chance to win more.")
                self.lang_dict.add_with(["pt_br", "pt"], "Aposte seus cookies para tentar ganhar mais.")
            return self._untangle_str(ctx, self._cname)

        def deco_usage(self, ctx: Context, prefix: str = None, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en", "To use: {}cookie slotmachine (all can be used to bet all unclaimed cookies quickly)"
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    "Para usar: {}cookie slotmachine (all pode ser usado para apostar todos "
                    "os cookies não coletados rapidamente)",
                )
            return self._untangle_str(ctx, self._cname).format(prefix)

        # region Hide.

        def deco_description(self, ctx: Context, *args, **kwargs) -> str:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with("en", "Bet your daily cookie for a chance to win others.")
                self.lang_dict.add_with(
                    ["pt_br", "pt"], "Use a máquina caça-níquel de cookies para tentar multiplicar seus cookies."
                )
            return self._untangle_str(ctx, self._cname)

        def deco_commands(self, ctx: Context, *args, **kwargs) -> CommandExemples:
            with self.lang_dict.once(self._cname):
                self.lang_dict.add_with(
                    "en",
                    CommandExemples(
                        [
                            {"args": "slotmachine", "response": "(the results of the slotmachine.)"},
                            {"args": "slotmachine all", "response": "(the results of the slotmachine.)"},
                        ]
                    ),
                )
                self.lang_dict.add_with(
                    ["pt_br", "pt"],
                    CommandExemples(
                        [
                            {"args": "slotmachine", "response": "(Resultado da máquina caça-níquel.)"},
                            {"args": "slotmachine all", "response": "(Resultado da máquina caça-níquel.)"},
                        ]
                    ),
                )
            return self._untangle_commands(ctx, self._cname)

        # endregion

    SlotMachine: SlotMachine

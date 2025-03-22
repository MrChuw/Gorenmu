from __future__ import annotations
from dataclasses import dataclass, field

import pathlib, json
import random
from typing import Any, TYPE_CHECKING, Callable, Dict, TypeVar, Protocol

from .extras import Activity as ActivityExtras
from .extras import Response
from .extras import Humanize
from .extras import TimeTools
from .extras import Dicio
from .extras import BaseFunctions
from .extras import WeatherTools

if TYPE_CHECKING:
    from bot.ext import Context
    from bot.models import Cookies
    from bot.ext.commands import Context


# For Humanize lang check: https://github.com/python-humanize/humanize/tree/main/src/humanize/locale
# For HyperTranslation default output lang check: bot.apis.translate.constants.GOOGLE_LANGUAGES_TO_CODES






class BaseTranslations:
    class TypeChecking(BaseFunctions):
        response: Response
        PlaceHolder2: response

    class SupportTools(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)
            self.populate_responses()
            self.Dicio: Dicio = Dicio()
        Dicio: Dicio
        mention: str

        class TimeTools(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
                self.TimeTools: TimeTools = TimeTools(self.obj, self.fallback)
                self.Humanize: Humanize = Humanize(self.get_object("Humanize"), self.get_object("Pattern time"))  # NOQA
            strftime: str
        TimeTools: TimeTools

        class Lottery(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
            bet_or_consultation: list[str]
        Lottery: Lottery

    class Exceptions(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)
            self.populate_responses()

        user_not_found_id: Response
        user_not_found_name: Response
        user_not_provided: Response
        never_seen: Response
        channel_not_found: Response
        message_too_long: Response
        time_expired: Response
        unexpected_error: Response
        too_much_characters: Response

        dev_required: str
        owner_required: str
        command_on_cooldown: str
        not_implemented: str
        error_not_registered: str
        error_on_response: str
        pipe_response: str
        command_not_pipeble: str
        lottery_seed: str
        announcement: str

    class Pipe(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        response: Response

    class Afk(BaseFunctions):
        def __init__(self, translation: dict, extras: BaseFunctions,):
            super().__init__(translation, None)
            self.populate_responses()
            _activity = extras.get_object("activity")["Activity"]
            self.afks = ActivityExtras(_activity).afks
        afks: dict[str, ActivityExtras.Status]
        afk_response: Response
        afk_content_response: Response

    class IsAfk(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        bot_nick: Response
        author_nick: Response
        is_afk: Response
        is_afk_content: Response
        is_not_afk: Response

    class RAfk(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        is_afk: Response
        is_afk_content: Response
        is_not_afk: Response

    class AfkListeners(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        is_afk: Response
        is_afk_content: Response

    class Alias(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)
            self.populate_responses()
        dont_have_alias: Response
        alias_invalid_name: Response
        user_has_no_alias: Response
        alias_table_headers: list[str]
        alias_table_replaces: list[str]
        alias_table_name: str

        class Add(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
            no_command_to_add: Response
            alias_name_conflict: Response
            alias_created: Response
            command_dont_exist: Response
        Add: Add

        class Check(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            user_alias_list: Response
            no_alias_found: Response
            list_of_alias_of: Response
            list_of_special_case: Response
            alias_not_found: Response
            alias_deleted: Response
            normal_message: Response
            appendix_message: Response
            appendix: str
            message: str
        Check: Check

        class Copy(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            alias_not_provided: Response
            target_alias_invalid_name: Response
            no_alias_found: Response
            link_to_a_link: Response
            copy_success: Response
            copy_with_name_of: Response
        Copy: Copy

        class Describe(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            no_args_to_parse: Response
            description_updated: Response
            description_reverted: Response
        Describe: Describe

        class Edit(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            no_args_provided: Response
            edit_link: Response
            edit_success: Response
            command_dont_exist: Response
        Edit: Edit

        class Link(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            link_no_args: Response
            alias_name_already_exists: Response
            user_dont_has_alias: Response
            link_with_invalid_name: Response
            link_to_link: Response
            link_success: Response
            link_name_string: str
        Link: Link

        class Remove(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            no_alias_name_provided: Response
            alias_removed: Response
        Remove: Remove

        class Rename(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            no_name_provided: Response
            alias_already_exists: Response
            alias_renamed: Response
        Rename: Rename

    class Chance(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        random_percentage: Response

    class Choice(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
            self.base_separators: list[str] = [",", " "]
            self.choice_separators: list[str] = self.base_separators + getattr(self, "additional_separators")
        chosen_option: Response
        choice_separators: list[str]

    class Count(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        character_count: Response

    class RandomColor(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        response_url: Response
        api_down: str

    class Reverse(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        reversed_string: Response

    class RandomLine(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        no_message_found: Response
        search_timeout: Response
        random_line: Response

    class UpSideDown(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        upsidedown: Response

    class Scp(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        links: Response

    class Wikihow(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        url: str
        links: Response

    class Wikipedia(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        url: str
        links: Response

    class Annotations(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        title_too_long: Response
        too_few_characters: Response
        annotation_created: Response
        no_annotations_with_id: Response
        all_annotations: Response
        annotation_content: Response
        deleted: Response
        id_not_provided: Response
        option_not_recognized: Response

    class HyperTranslate(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
        lang: str
        starter_string: str
        unexpected_error: Response
        translation: Response

    class Lottery(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.bets_values: dict[int, int] = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 11, 8: 25, 9: 63, 10: 187,
                                                11: 346, 12: 649, 13: 943, 14: 1038, 15: 1294}
            self.past: list[str] = self.get_object("past")
            self.current: list[str] = self.get_object("current")

            self.only_numbers: Response = Response(response=self.get_object("only_numbers"))
            self.duplicate_numbers: Response = Response(response=self.get_object("duplicate_numbers"))
            self.not_enough_cookies: Response = Response(response=self.get_object("not_enough_cookies"))
            self.not_enough_cookies_more_five: Response = Response(response=self.get_object("not_enough_cookies_more_five"))
            self.bet_place: Response = Response(response=self.get_object("bet_place"))
            self.lottery_lock: Response = Response(response=self.get_object("lottery_lock"))
            self.timeout: Response = Response(response=self.get_object("timeout"))
            self.too_much_numbers: Response = Response(response=self.get_object("too_much_numbers"))
            self.minimum_bet: Response = Response(response=self.get_object("minimum_bet"))

            self.no_bet_id: Response = Response(response=self.get_object("no_bet_id"))
            self.ticket_info: Response = Response(response=self.get_object("ticket_info"))
            self.no_old_bets_found: Response = Response(response=self.get_object("no_old_bets_found"))
            self.old_bets: Response = Response(response=self.get_object("old_bets"))
            self.no_active_bets_found: Response = Response(response=self.get_object("no_active_bets_found"))
            self.active_bets: Response = Response(response=self.get_object("active_bets"))
            self.no_bets: Response = Response(response=self.get_object("no_bets"))
            self.all_bets: Response = Response(response=self.get_object("all_bets"))
            self.unknown_option: Response = Response(response=self.get_object("unknown_option"))
            self.lottery_announce_messages: list[str] = self.get_object("lottery_announce_messages")

            self.winners: str = self.get_object("winners")
            self.no_winners: str = self.get_object("no_winners")

            self.lottery_result_announce: str = self.get_object("lottery_result_announce")
            self.remind_message: str = self.get_object("remind_message")

    class Cookies(BaseFunctions):
        def __init__(self, translation: dict, extras: BaseFunctions):
            super().__init__(translation, None)
            self.cookies_path: pathlib.Path = extras.get_object("cookies_path")

            self.daily_limit_reached: Response = Response(response=self.get_object("daily_limit_reached"))
            self.user_not_found: Response = Response(response=self.get_object("user_not_found"))
            self.invalid_option: Response = Response(response=self.get_object("invalid_option"))
            self.cookie_not_found: Response = Response(response=self.get_object("cookie_not_found"))

            self.not_eat: Response = Response(response=self.get_object("not_eat"))
            self.negative_eat: Response = Response(response=self.get_object("negative_eat"))
            self.multiple_eat: Response = Response(response=self.get_object("multiple_eat"))
            self.eat: Response = Response(response=self.get_object("eat"))

            self.cc_bot_nick: Response = Response(response=self.get_object("cc_bot_nick"))

            self.gift_bot_nick: Response = Response(response=self.get_object("gift_bot_nick"))
            self.gift_user_himself: Response = Response(response=self.get_object("gift_user_himself"))
            self.gift_on_cooldown_no_stock: Response = Response(response=self.get_object("gift_on_cooldown_no_stock"))
            self.invalid_gift_amount: Response = Response(response=self.get_object("invalid_gift_amount"))
            self.multiple_gift: Response = Response(response=self.get_object("multiple_gift"))
            self.gift: Response = Response(response=self.get_object("gift"))
            self.gift_not_enough_cookies: Response = Response(response=self.get_object("gift_not_enough_cookies"))
            self.stock: Response = Response(response=self.get_object("stock"))
            self.stock_not_daily: Response = Response(response=self.get_object("stock_not_daily"))
            self.stock_not_enough_cookies: Response = Response(response=self.get_object("stock_not_enough_cookies"))
            self.ranks: Response = Response(response=self.get_object("ranks"))
            self.top10_ish: Response = Response(response=self.get_object("top10_ish"))
            self.format_cookie_count: dict[str, str] = self.get_object("format_cookie_count")

            self.invalid_amount: Response = Response(response=self.get_object("invalid_amount"))
            self.daily_win: Response = Response(response=self.get_object("daily_win"))
            self.daily_single_loss: Response = Response(response=self.get_object("daily_single_loss"))
            self.not_daily_multiple_loss: Response = Response(response=self.get_object("not_daily_multiple_loss"))
            self.not_daily_single_loss: Response = Response(response=self.get_object("not_daily_single_loss"))
            self.not_daily_multiple_win: Response = Response(response=self.get_object("not_daily_multiple_win"))
            self.not_daily_lost_everything: Response = Response(response=self.get_object("not_daily_lost_everything"))

        def random_line(self):
            return random.choice(json.loads(self.cookies_path.read_text())["root"]["options"])

        def format_cookie_count(self, ctx: Context, *args: Any, **kwargs: Any):
            # Custom formatting function based on provided cookie stats.
            translations = self.format_cookie_count
            response = kwargs.pop("mention", "") + " "
            cookie: Cookies = kwargs.pop("cookie")
            response += translations["cookie_count"].format(cookie.consumed) if cookie.consumed > 0 else ""
            response += translations["stocked_count"].format(cookie.stocked) if cookie.stocked > 0 else ""
            response += translations["received_count"].format(cookie.received) if cookie.received > 0 else ""
            response += translations["donated_count"].format(cookie.donated) if cookie.donated > 0 else ""
            response += translations["not_redeemed_count"].format(cookie.not_redeemed()) if cookie.not_redeemed() > 0 else ""
            response += translations["total_count"].format(cookie.total)
            return Response({"response": response})


    class NSFW(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)

        class Imgur(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.links: Response = Response({})
                self.timeout: Response = Response(response=self.get_object("timeout"))
                self.time_message: str = self.get_object("time_message")
                self.all_images_embed: str = self.get_object("all_images_embed")
                self.all_images_embed_time: str = self.get_object("all_images_embed_time")

        class ImgurRepeated(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.links_repeated: Response = Response(response=self.get_object("links_repeated"))
                self.no_repeated: Response = Response(response=self.get_object("no_repeated"))

        class Boru(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.original: str = self.get_object("original")
                self.preview: str = self.get_object("preview")
                self.pls_wait: str = self.get_object("pls_wait")
                self.unexpected_error: Response = Response(response=self.get_object("unexpected_error"))
                self.success: Response = Response(response=self.get_object("success"))
                self.too_much_tags: Response = Response(response=self.get_object("too_much_tags"))

    class Admin(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_subclasses(base_cls=self)

        class Nada(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
            nada: Response
            vazio: Response
        Nada: Nada

        class Reload(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
            commands_reloaded: Response
            command_not_found: Response
            command_reloaded: Response
            command_reloaded_error: Response
            translations_reloaded: Response
            translations_reloaded_error: Response
        Reload: Reload

        class Restart(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
            success: Response
            unexpected_error: Response
        Restart: Restart

        class DisableNSFW(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
            success: Response
            unexpected_error: Response
        DisableNSFW: DisableNSFW

    # TODO
    class Markov(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.purge: str = self.get_object("purge")
            self.replace: str = self.get_object("replace")
            self.unlearn: str = self.get_object("unlearn")

    class Weather(BaseFunctions):
        def __init__(self, translation: dict, extras: BaseFunctions):
            super().__init__(translation, None)
            self.weather_codes = WeatherTools(tuple(obj["Weather"] for obj in extras.get_base("weather")))


# TODO: Lembrar dos pets, games, dungeons, Weather
class Translations(BaseFunctions, BaseTranslations):
    def __init__(self, translation: Dict[str, Any], lang: str, fallback: Dict[str, Any] = None):
        super().__init__(translation['strings'], fallback['strings'] if fallback else None)
        self._initialize_values(translation, fallback)
        self.lang = lang

    def _initialize_values(self, translation: Dict[str, Any], fallback: Dict[str, Any] = None):
        if fallback:
            extras = BaseFunctions(translation.get('extras', {}), fallback.get('extras', {}))
        else:
            extras = BaseFunctions(translation.get('extras', {}))

        extras_fields = {"Afk", "Cookies", "Weather"}
        self.populate_subclasses(
                extras=extras,
                extras_fields=extras_fields,
                base_cls=BaseTranslations(),
                add_to_self=True
        )


















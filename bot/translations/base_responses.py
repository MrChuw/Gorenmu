from __future__ import annotations

import pathlib, json
import random
from typing import Any, TYPE_CHECKING

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


# TODO: Lembrar dos pets, games, dungeons, Weather
class Translations(BaseFunctions):
    def __init__(self, translation: dict, fallback: dict = None):
        fallback_strings = fallback['strings'] if fallback else None
        extras = translation['extras'] if 'extras' in translation else fallback['extras']
        extras_fallback = fallback['extras'] if fallback else None
        extras = BaseFunctions(extras, extras_fallback)
        super().__init__(translation['strings'], fallback_strings)
        self.SupportTools = BaseTranslations.SupportTools(self.get_base("SupportTools"))
        self.Exceptions = BaseTranslations.Exceptions(self.get_base("Exceptions"))
        self.Admin = BaseTranslations.Admin(self.get_base("Admin"))
        self.Others = BaseTranslations.Others(self.get_base("Others"))
        self.Afk = BaseTranslations.Afk(self.get_base("Afk"), extras)
        self.Alias = BaseTranslations.Alias(self.get_base("Alias"))
        self.Chance = BaseTranslations.Chance(self.get_base("Chance"))
        self.Choice = BaseTranslations.Choice(self.get_base("Choice"))
        self.Count = BaseTranslations.Count(self.get_base("Count"))
        self.HyperTranslate = BaseTranslations.HyperTranslate(self.get_base("HyperTranslate"))
        self.NSFW = BaseTranslations.NSFW(self.get_base("NSFW"))
        self.RandomColor = BaseTranslations.RandomColor(self.get_base("RandomColor"))
        self.Reverse = BaseTranslations.Reverse(self.get_base("Reverse"))
        self.RandomLine = BaseTranslations.RandomLine(self.get_base("RandomLine"))
        self.Scp = BaseTranslations.Scp(self.get_base("Scp"))
        self.UpSideDown = BaseTranslations.UpSideDown(self.get_base("UpSideDown"))
        self.Wikihow = BaseTranslations.Wikihow(self.get_base("Wikihow"))
        self.Wikipedia = BaseTranslations.Wikipedia(self.get_base("Wikipedia"))
        self.Annotations = BaseTranslations.Annotations(self.get_base("Annotations"))
        self.Lottery = BaseTranslations.Lottery(self.get_base("Lottery"))
        self.Cookies = BaseTranslations.Cookies(self.get_base("Cookies"), extras)

        # TODO
        self.Markov = BaseTranslations.Markov(self.get_base("Markov"))
        self.Weather = BaseTranslations.Weather(self.get_base("Weather"), extras)
        del self.fallback, self.obj

    class TypeChecking(BaseFunctions):
        response: Response


class BaseTranslations:
    class SupportTools(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.mention: str = self.get_object("mention")
            self.TimeTools = self.TimeTools(self.get_base("TimeTools"))
            self.Lottery = self.Lottery(self.get_base("Lottery"))
            self.Dicio: Dicio = Dicio  # NOQA
            del self.fallback, self.obj

        class TimeTools(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.TimeTools: TimeTools = TimeTools(self.obj, self.fallback)
                self.Humanize: Humanize = Humanize(self.get_base("Humanize"), self.obj, self.fallback)  # NOQA
                self.strftime: str = self.get_object("strftime")
                del self.fallback, self.obj

        class Lottery(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.bet_or_consultation: list[str] = self.get_object("bet_or_consultation")
                del self.fallback, self.obj

    class Exceptions(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.LotteryExceptions = self.LotteryExceptions(self.get_object("LotteryExceptions"))
            self.ToolsExceptions = self.ToolsExceptions(self.get_object("ToolsExceptions"))
            self.BotMainLoopExceptions = self.BotMainLoopExceptions(self.get_object("BotMainLoopExceptions"))
            self.ResponseExceptions = self.ResponseExceptions(self.get_object("ResponseExceptions"))
            del self.fallback, self.obj

        class LotteryExceptions(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.lottery_seed: str = self.get_object("lottery_seed")
                del self.fallback, self.obj

        class ToolsExceptions(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.announcement: str = self.get_object("announcement")
                del self.fallback, self.obj

        class BotMainLoopExceptions(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.dev_required: str = self.get_object("dev_required")
                self.owner_required: str = self.get_object("owner_required")
                self.command_on_cooldown: str = self.get_object("command_on_cooldown")
                self.not_implemented: str = self.get_object("not_implemented")
                self.error_not_registered: str = self.get_object("error_not_registered")
                del self.fallback, self.obj

        class ResponseExceptions(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.error_on_response: str = self.get_object("error_on_response")
                self.pipe_response: str = self.get_object("pipe_response")
                self.command_not_pipeble: str = self.get_object("command_not_pipeble")
                del self.fallback, self.obj

    class Admin(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.Nada = self.Nada(self.get_base("Nada"))
            self.Reload = self.Reload(self.get_base("Reload"))
            self.Restart = self.Restart(self.get_base("Restart"))
            del self.fallback, self.obj

        class Nada(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.nada: Response = Response(response=self.get_object("nada"))
                del self.fallback, self.obj

        class Reload(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.commands_reloaded: Response = Response(response=self.get_object("commands_reloaded"))
                del self.fallback, self.obj

        class Restart(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.success: Response = Response({"response": self.get_object("success")})
                self.unexpected_error: Response = Response(response=self.get_object("unexpected_error"))
                del self.fallback, self.obj

    class Others(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.Pipe = self.Pipe(self.get_base("Pipe"))
            del self.fallback, self.obj

        class Pipe(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.response: Response = Response(response=self.get_object("response"))
                del self.fallback, self.obj

    class Afk(BaseFunctions):
        def __init__(self, translation: dict, extras: BaseFunctions,):
            super().__init__(translation, None)
            _activity = extras.get_object("activity")["Activity"]
            self.afks: dict[str, ActivityExtras.Status] = ActivityExtras(_activity).afks
            self.Afk = self.Afk(self.get_base("Afk"))
            self.IsAfk = self.IsAfk(self.get_base("IsAfk"))
            self.RAfk = self.RAfk(self.get_base("RAfk"))
            self.AfkListeners = self.AfkListeners(self.get_base("AfkListeners"))
            del self.fallback, self.obj

        class Afk(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.message_too_long: Response = Response(response=self.get_object("message_too_long"))
                self.afk_response: Response = Response(response=self.get_object("afk_response"))
                self.afk_content_response: Response = Response(response=self.get_object("afk_content_response"))
                del self.fallback, self.obj

        class IsAfk(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.bot_nick: Response = Response(response=self.get_object("bot_nick"))
                self.author_nick: Response = Response(response=self.get_object("author_nick"))
                self.never_seen: Response = Response(response=self.get_object("never_seen"))
                self.is_afk: Response = Response(response=self.get_object("is_afk"))
                self.is_afk_content: Response = Response(response=self.get_object("is_afk_content"))
                self.is_not_afk: Response = Response(response=self.get_object("is_not_afk"))
                del self.fallback, self.obj

        class RAfk(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.time_expired: Response = Response(response=self.get_object("time_expired"))
                self.is_afk: Response = Response(response=self.get_object("is_afk"))
                self.is_afk_content: Response = Response(response=self.get_object("is_afk_content"))
                self.is_not_afk: Response = Response(response=self.get_object("is_not_afk"))
                del self.fallback, self.obj

        class AfkListeners(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.is_afk: Response = Response(response=self.get_object("is_afk"))
                self.is_afk_content: Response = Response(response=self.get_object("is_afk_content"))
                del self.fallback, self.obj

    class Alias(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.user_not_found: Response = Response(response=self.get_object("user_not_found"))
            self.dont_have_alias: Response = Response(response=self.get_object("dont_have_alias"))
            self.alias_invalid_name: Response = Response(response=self.get_object("alias_invalid_name"))
            self.user_has_no_alias: Response = Response(response=self.get_object("user_has_no_alias"))
            self.alias_table_headers: list[str] = self.get_object("alias_table_headers")
            self.alias_table_replaces: list[str] = self.get_object("alias_table_replaces")
            self.alias_table_name: str = self.get_object("alias_table_name")
            self.Add = self.Add(self.get_base("Add"))
            self.Check = self.Check(self.get_base("Check"))
            self.Copy = self.Copy(self.get_base("Copy"))
            self.Describe = self.Describe(self.get_base("Describe"))
            self.Edit = self.Edit(self.get_base("Edit"))
            self.Link = self.Link(self.get_base("Link"))
            self.Remove = self.Remove(self.get_base("Remove"))
            self.Rename = self.Rename(self.get_base("Rename"))
            del self.fallback, self.obj

        class Add(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.no_command_to_add: Response = Response(response=self.get_object("no_command_to_add"))
                self.alias_name_conflict: Response = Response(response=self.get_object("alias_name_conflict"))
                self.alias_created: Response = Response(response=self.get_object("alias_created"))
                self.command_dont_exist: Response = Response(response=self.get_object("command_dont_exist"))
                del self.fallback, self.obj

        class Check(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.user_alias_list: Response = Response(response=self.get_object("user_alias_list"))
                self.no_alias_found: Response = Response(response=self.get_object("no_alias_found"))
                self.list_of_alias_of: Response = Response(response=self.get_object("list_of_alias_of"))
                self.list_of_special_case: Response = Response(response=self.get_object("list_of_special_case"))
                self.alias_not_found: Response = Response(response=self.get_object("alias_not_found"))
                self.appendix: str = self.get_object("appendix")
                self.alias_deleted: Response = Response(response=self.get_object("alias_deleted"))
                self.appendix_message: Response
                self.message: str = self.get_object("message")
                self.normal_message: Response = Response(response=self.get_object("normal_message"))
                del self.fallback, self.obj

        class Copy(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.user_not_provided: Response = Response(response=self.get_object("user_not_provided"))
                self.alias_not_provided: Response = Response(response=self.get_object("alias_not_provided"))
                self.target_alias_invalid_name: Response = Response(response=self.get_object("target_alias_invalid_name"))
                self.no_alias_found: Response = Response(response=self.get_object("no_alias_found"))
                self.link_to_a_link: Response = Response(response=self.get_object("link_to_a_link"))
                self.copy_success: Response = Response(response=self.get_object("copy_success"))
                self.copy_with_name_of: Response = Response(response=self.get_object("copy_with_name_of"))
                del self.fallback, self.obj

        class Describe(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.no_args_to_parse: Response = Response(response=self.get_object("no_args_to_parse"))
                self.description_updated: Response = Response(response=self.get_object("description_updated"))
                self.description_reverted: Response = Response(response=self.get_object("description_reverted"))
                del self.fallback, self.obj

        class Edit(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.no_args_provided: Response = Response(response=self.get_object("no_args_provided"))
                self.edit_link: Response = Response(response=self.get_object("edit_link"))
                self.edit_success: Response = Response(response=self.get_object("edit_success"))
                self.command_dont_exist: Response = Response(response=self.get_object("command_dont_exist"))
                del self.fallback, self.obj

        class Link(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.link_no_args: Response = Response(response=self.get_object("link_no_args"))
                self.alias_name_already_exists: Response = Response(response=self.get_object("alias_name_already_exists"))
                self.user_dont_has_alias: Response = Response(response=self.get_object("user_dont_has_alias"))
                self.link_with_invalid_name: Response = Response(response=self.get_object("link_with_invalid_name"))
                self.link_name_string: str = self.get_object("link_name_string")
                self.link_to_link: Response = Response(response=self.get_object("link_to_link"))
                self.link_success: Response = Response(response=self.get_object("link_success"))
                del self.fallback, self.obj

        class Remove(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.no_alias_name_provided: Response = Response(response=self.get_object("no_alias_name_provided"))
                self.alias_removed: Response = Response(response=self.get_object("alias_removed"))
                del self.fallback, self.obj

        class Rename(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.no_name_provided: Response = Response(response=self.get_object("no_name_provided"))
                self.alias_already_exists: Response = Response(response=self.get_object("alias_already_exists"))
                self.alias_renamed: Response = Response(response=self.get_object("alias_renamed"))
                del self.fallback, self.obj

    class Chance(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.random_percentage: Response = Response(response=self.get_object("random_percentage"))
            del self.fallback, self.obj

    class Choice(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.base_separators: list[str] = [",", " "]
            self.choice_separators: list[str] = self.base_separators + self.get_object("additional_separators")
            self.chosen_option: Response = Response(response=self.get_object("chosen_option"))
            del self.fallback, self.obj

    class Count(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.character_count: Response = Response(response=self.get_object("character_count"))
            del self.fallback, self.obj

    class HyperTranslate(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            # Use bot.apis.translate.constants.GOOGLE_LANGUAGES_TO_CODES as reference for the languages
            self.lang: str = self.get_object("base_lang")
            self.quantity_error: Response = Response(response=self.get_object("quantity_error"))
            self.starter_string: str = self.get_object("starter_string")
            self.unexpected_error: Response = Response(response=self.get_object("unexpected_error"))
            self.translation: Response = Response(response=self.get_object("translation"))
            del self.fallback, self.obj

    class NSFW(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.Imgur = self.Imgur(self.get_base("Imgur"))
            self.ImgurRepeated = self.ImgurRepeated(self.get_base("ImgurRepeated"))
            self.Boru = self.Boru(self.get_base("Boru"))
            del self.fallback, self.obj

        class Imgur(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.links: Response = Response({})
                self.time_message: str = self.get_object("time_message")
                self.all_images_embed: str = self.get_object("all_images_embed")
                self.all_images_embed_time: str = self.get_object("all_images_embed_time")
                self.timeout: Response = Response(response=self.get_object("timeout"))
                del self.fallback, self.obj

        class ImgurRepeated(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.links_repeated: Response = Response(response=self.get_object("links_repeated"))
                self.no_repeated: Response = Response(response=self.get_object("no_repeated"))
                del self.fallback, self.obj

        class Boru(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.original: str = self.get_object("original")
                self.preview: str = self.get_object("preview")
                self.pls_wait: str = self.get_object("pls_wait")
                self.unexpected_error: Response = Response(response=self.get_object("unexpected_error"))
                self.success: Response = Response(response=self.get_object("success"))
                self.too_much_tags: Response = Response(response=self.get_object("too_much_tags"))
                del self.fallback, self.obj

    class RandomColor(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.response_url: Response = Response(response=self.get_object("response_url"))
            del self.fallback, self.obj

    class Reverse(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.reversed_string: Response = Response(response=self.get_object("reversed_string"))
            del self.fallback, self.obj

    class RandomLine(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.channel_not_found: Response = Response(response=self.get_object("channel_not_found"))
            self.user_not_found: Response = Response(response=self.get_object("user_not_found"))
            self.no_message_found: Response = Response(response=self.get_object("no_message_found"))
            self.random_line: Response = Response(response=self.get_object("random_line"))
            del self.fallback, self.obj

    class Scp(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.links: Response = Response({})
            self.unexpected_error: Response = Response(response=self.get_object("unexpected_error"))
            del self.fallback, self.obj

    class UpSideDown(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.upsidedown: Response = Response(response=self.get_object("upsidedown"))
            del self.fallback, self.obj

    class Wikihow(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.url: str = self.get_object("url")
            self.links: Response = Response({})
            self.unexpected_error: Response = Response(response=self.get_object("unexpected_error"))
            del self.fallback, self.obj

    class Wikipedia(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.url: str = self.get_object("url")
            self.links: Response = Response({})
            self.unexpected_error: Response = Response(response=self.get_object("unexpected_error"))
            del self.fallback, self.obj

    class Annotations(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.too_much_characters: Response = Response(response=self.get_object("too_much_characters"))
            self.title_too_long: Response = Response(response=self.get_object("title_too_long"))
            self.too_few_characters: Response = Response(response=self.get_object("too_few_characters"))
            self.annotation_created: Response = Response(response=self.get_object("annotation_created"))
            self.no_annotations_with_id: Response = Response(response=self.get_object("no_annotations_with_id"))
            self.all_annotations: Response = Response(response=self.get_object("all_annotations"))
            self.annotation_content: Response = Response(response=self.get_object("annotation_content"))
            self.deleted: Response = Response(response=self.get_object("deleted"))
            self.id_not_provided: Response = Response(response=self.get_object("id_not_provided"))
            self.option_not_recognized: Response = Response(response=self.get_object("option_not_recognized"))
            del self.fallback, self.obj

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
            del self.fallback, self.obj

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
            del self.fallback

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

        class SlotMachine(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.daily_limit_reached: Response = Response({"response": self.get_object("daily_limit_reached")})
                self.invalid_amount: Response = Response({"response": self.get_object("invalid_amount")})
                self.daily_win: Response = Response({"response": self.get_object("daily_win")})
                self.daily_single_loss: Response = Response({"response": self.get_object("daily_single_loss")})
                self.not_daily_multiple_loss: Response = Response({"response": self.get_object("not_daily_multiple_loss")})
                self.not_daily_single_loss: Response = Response({"response": self.get_object("not_daily_single_loss")})
                self.not_daily_multiple_win: Response = Response({"response": self.get_object("not_daily_multiple_win")})
                self.not_daily_lost_everything: Response = Response({"response": self.get_object("not_daily_lost_everything")})
                del self.fallback, self.obj













    # TODO
    class Markov(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.purge: str = self.get_object("purge")
            self.replace: str = self.get_object("replace")
            self.unlearn: str = self.get_object("unlearn")

            del self.fallback, self.obj


    class Weather(BaseFunctions):
        def __init__(self, translation: dict, extras: BaseFunctions):
            super().__init__(translation, None)
            self.weather_codes = WeatherTools(tuple(obj["Weather"] for obj in extras.get_base("weather")))

            del self.fallback, self.obj



















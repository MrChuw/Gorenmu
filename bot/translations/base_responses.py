from __future__ import annotations

import json
import pathlib
import random
import re
from typing import Any, Dict, TYPE_CHECKING

from .extras import Activity as ActivityExtras, BaseFunctions, EmoteEmotions, Humanize, Response

if TYPE_CHECKING:
    from bot.ext import Context
    from bot.models import Cookies


# For Humanize lang check: https://github.com/python-humanize/humanize/tree/main/src/humanize/locale
# For HyperTranslation default output lang check: bot.apis.translate.constants.GOOGLE_LANGUAGES_TO_CODES


class BaseTranslations:
    class TypeChecking(BaseFunctions):
        response: Response

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
            all: Response
            module_reloaded: Response
            module_reloaded_error: Response

        Reload: Reload

        class Restart(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            success: Response
            unexpected_error: Response

        Restart: Restart

    class SupportTools(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
            self.populate_subclasses(base_cls=self)

        class LanguageContext(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
                self.populate_subclasses(base_cls=self)

            mention: str

            class Verbs(BaseFunctions):
                def __init__(self, translation: dict):
                    super().__init__(translation, None)
                    self.populate_responses()

                second_person: str
                third_person: str

            Verbs: Verbs

        LanguageContext: LanguageContext

        class TimeTools(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
                self.Humanize: Humanize = Humanize(self.get_object("Humanize"), self.get_object("Pattern time"))

            strftime: str

        TimeTools: TimeTools

        class Lottery(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()

            bet_or_consultation: list[str]

        Lottery: Lottery

        class Emotes(BaseFunctions):
            def __init__(self, translation: dict):
                super().__init__(translation, None)
                self.populate_responses()
                self.emotions = EmoteEmotions(self.emotions)  # NOQA

            emotions: EmoteEmotions

        Emotes: Emotes

    class Exceptions(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        # Responses
        user_not_found_id: Response
        user_not_found_name: Response
        time_expired: Response
        no_content_provided: Response
        too_much_characters: Response
        no_id_provided: Response
        id_not_valid: Response
        user_not_provided: Response
        guard_caught: Response
        unexpected_error: Response
        link: Response
        timeout: Response
        never_seen: Response
        channel_not_found: Response

        # Strings
        dev_required: str
        message_too_long: str
        owner_required: str
        command_on_cooldown: str
        not_implemented: str
        error_not_registered: str
        command_not_pipeble: str
        pipe_response_error: str
        pipe_response: str

    class Pipe(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        response: Response

    class Afk(BaseFunctions):
        def __init__(self, translation: dict, extras: BaseFunctions):
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
        return_expired: str

    class AfkListeners(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        is_afk: Response
        is_afk_content: Response

    class Alias(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()
            self.populate_subclasses(base_cls=self)

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
            link_to_with_invalid_name: Response
            link_custom_name_invalid: Response
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
            self.base_separators: list[str] = [",", r"\s+"]
            self.choice_separators: list[str] = self.base_separators + getattr(self, "additional_separators")
            self.pattern: str = "|".join(s if s.startswith("\\") else re.escape(s) for s in self.choice_separators)

        chosen_option: Response
        choice_separators: list[str]
        pattern: str

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

        no_channel_message: Response
        no_user_message: Response
        no_user_on_channel: Response
        search_timeout: Response
        random_line: Response

    class UpSideDown(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        upsidedown: Response

    class Wikihow(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        url: str

    class Wikipedia(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        url: str

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
        option_not_recognized: Response
        no_annotation_present: Response

    class HyperTranslate(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        base_lang: str
        starter_string: str
        unexpected_error: Response
        translation: Response

    class Cookies(BaseFunctions):
        def __init__(self, translation: dict, extras: BaseFunctions):
            super().__init__(translation, None)
            self.populate_responses()
            self.cookies_path: pathlib.Path = extras.get_object("cookies_path")

        cookies_path: pathlib.Path
        order_dict: dict[str, dict[str, list[str]]]
        formats_cookie_count: dict[str, str]
        invalid_option: Response
        daily_limit_reached: Response
        user_not_found: Response

        not_eat: Response
        negative_eat: Response
        multiple_eat: Response
        eat: Response

        cookie_not_found: Response

        cc_bot_nick: Response

        gift_bot_nick: Response
        gift_user_himself: Response
        gift_on_cooldown_no_stock: Response
        invalid_gift_amount: Response
        not_gifted: Response
        negative_gift: Response
        multiple_gift: Response
        gift: Response
        gift_not_enough_cookies: Response
        gift_no_stock_but_cooldown: Response

        stock: Response
        stock_not_daily: Response
        stock_not_enough_cookies: Response
        ranks: Response
        top10_ish: Response

        invalid_amount: Response

        all_string: str
        time_suffix: str

        cookie_win_suffix: str
        cookie_loss_suffix: str
        accumulated_message: Response
        last_cookie_message: Response

        daily_win: Response
        daily_single_loss: Response
        not_daily_multiple_loss: Response
        not_daily_single_loss: Response
        not_daily_multiple_win: Response
        not_daily_lost_everything: Response

        def random_line(self):
            return random.choice(json.loads(self.cookies_path.read_text())["options"])

        def format_cookie_count(self, ctx: Context, *args: Any, **kwargs: Any):  # NOQA
            # Custom formatting function based on provided cookie stats.
            translations = self.formats_cookie_count
            mention = kwargs.pop("mention", "")
            cookie: Cookies = kwargs.pop("cookie")
            verb: str = kwargs.pop("verb")
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

            response = f"{mention} {' '.join(parts)}".strip()

            return Response({"ctx": ctx, "response_string": response})

    class Safebooru(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        original: str
        preview: str
        too_much_tags: Response
        unexpected_error: Response
        success: Response

    class PixelSorting(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        no_url: Response
        invalid_content_type: Response
        took_too_long: Response
        image: Response

    class Ping(BaseFunctions):
        def __init__(self, translation: dict):
            super().__init__(translation, None)
            self.populate_responses()

        ping: Response


class Translations(BaseFunctions, BaseTranslations):
    def __init__(self, translation: Dict[str, Any], lang: str, fallback: Dict[str, Any] = None):
        super().__init__(translation["strings"], fallback["strings"] if fallback else None)
        self._initialize_values(translation, fallback)
        self.lang = lang

    def _initialize_values(self, translation: Dict[str, Any], fallback: Dict[str, Any] = None):
        if fallback:
            extras = BaseFunctions(translation.get("extras", {}), fallback.get("extras", {}))
        else:
            extras = BaseFunctions(translation.get("extras", {}))

        extras_fields = {"Afk", "Cookies", "Weather"}
        self.populate_subclasses(
            extras=extras, extras_fields=extras_fields, base_cls=BaseTranslations(), add_to_self=True
        )

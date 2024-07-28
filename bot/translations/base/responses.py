# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from bot.translations.base import Response
from bot.translations.base.extras import (
    BaseTranslation, fight_option, PetFuncCallable, PetsDict, Status, WeatherTools,
)

if TYPE_CHECKING:
    from ext.commands import Context


class BaseTranslations:
    class IDE:
        class TypeChecking(BaseTranslation):
            response: Response
            pass

    class Activity:
        afks: dict[str, Status]

        class Afk(BaseTranslation):
            message_too_long: Response
            afk_content_response: Response
            afk_response: Response

        class IsAfk(BaseTranslation):
            bot_nick: Response
            author_nick: Response
            never_seen: Response
            is_afk: Response
            is_afk_content: Response
            is_not_afk: Response

        class RAfk(BaseTranslation):
            time_expired: Response
            is_afk: Response
            is_afk_content: Response
            is_not_afk: Response

        class AfkListeners(BaseTranslation):
            is_afk: Response
            is_afk_content: Response

    class Admin:
        class AddUser(BaseTranslation):
            user_not_found: Response
            user_response: Response

        class AddBot(BaseTranslation):
            user_not_found: Response
            user_already_added: Response
            user_added: Response

        class AllChannels(BaseTranslation):
            channels: Response

        class Announce(BaseTranslation):
            announce: Response

        class ApiBot(BaseTranslation):
            added_with_success: Response

        class ChannelLog(BaseTranslation):
            channel_already_added: Response
            channel_added: Response

        class CookieGive(BaseTranslation):
            cookie_given: Response

        class CountUser(BaseTranslation):
            user_quantity: Response

        class DBGrep(BaseTranslation):
            user_not_found: Response
            user_info: Response
            channel_info: Response

        class DelFromDB(BaseTranslation):
            user_not_found: Response
            user_deleted: Response
            users_deleted: Response

        class DisableNSFW(BaseTranslation):
            commands_disabled: Response

        class LotteryStart(BaseTranslation):
            pass  # TODO: Fazer isso daqui

        class Nada(BaseTranslation):
            nada: Response

        class Reload(BaseTranslation):
            commands_reloaded: Response

        class Restart(BaseTranslation):
            success: Response
            unexpected_error: Response

        class RGit(BaseTranslation):
            git_pulled: Response

    class Random:
        class Chance(BaseTranslation):
            random_percentage: Response

        class Choice(BaseTranslation):
            chosen_option: Response

        class Count(BaseTranslation):
            character_count: Response

        class HyperTranslate(BaseTranslation):
            quantity_error: Response
            starter_string: str
            api_error: Response
            unexpected_error: Response
            translation: Response

        class Imgur(BaseTranslation):
            links: Response
            timeout: Response

        class Imgur7(BaseTranslation):
            links: Response
            timeout: Response

        class ImgurRepeated(BaseTranslation):
            links_repeated: Response

        class RandomColor(BaseTranslation):
            response: Response
            response_url: Response

        class Reverse(BaseTranslation):
            reversed_string: Response

        class RandomLine(BaseTranslation):
            channel_not_found: Response
            user_not_found: Response
            no_message_found: Response
            no_option_found: Response
            random_line: Response

        class Scp(BaseTranslation):
            links: Response
            unexpected_error: Response

        class UpSideDown(BaseTranslation):
            upsidedown: Response

        class Wikihow(BaseTranslation):
            links: Response
            unexpected_error: Response

        class Wikipedia(BaseTranslation):
            links: Response
            unexpected_error: Response

    class Annotations:
        class Annotation(BaseTranslation):
            no_content_provided: Response
            too_much_annotations: Response
            too_much_characters: Response
            annotation_created: Response

        class Annotations(BaseTranslation):
            annotation_content: Response
            not_permitted: Response
            deleted: Response
            no_annotations_with_id: Response
            no_id_provided: Response
            all_annotations: Response
            no_annotations: Response

    class Lottery:
        class Bet(BaseTranslation):
            lottery_lock: Response
            not_enough_cookies: Response
            five_numbers_bet: Response
            more_than_five_numbers_bet: Response
            too_much_numbers: Response

            only_numbers: Response
            duplicate_numbers: Response
            minimum_bet: Response

        class Lottery(BaseTranslation):
            lottery_lock: Response
            timeout: Response
            not_enough_cookies: Response
            five_numbers_bet: Response
            more_than_five_numbers_bet: Response
            too_much_numbers: Response
            only_numbers: Response
            duplicate_numbers: Response
            minimum_bet: Response

            old_bets: Response
            no_bets_next_lottery: Response
            new_bets: Response
            invalid_option: Response

    class NSFW:
        class Boru(BaseTranslation):
            pls_wait: str
            unexpected_error: Response
            success: Response

        class AllBoorus(BaseTranslation):
            pls_wait: str
            unexpected_error: Response
            too_much_tags: Response
            success: Response

    class Cookies:
        def cookie_file(self) -> list[str] | None:
            return

        class Cookie(BaseTranslation):
            not_eat: Response
            negative_eat: Response
            multiple_eat: Response
            eat: Response
            not_enough_cookies: Response
            daily_limit_reached: Response

        class CookieCount(BaseTranslation):
            # Use english as reference.
            bot_nick: Response
            user_not_found: Response
            cookie: Response
            no_cookie: Response

            @staticmethod
            def format_cookie(self: Response, ctx: Context, *args: Any, **kwargs: Any):
                pass

        class Gift(BaseTranslation):
            invalid_amount: Response
            bot_nick: Response
            user_himself: Response
            user_not_found: Response
            multiple_gift: Response
            gift: Response
            daily_limit_reached: Response

        class SlotMachine(BaseTranslation):
            daily_limit_reached: Response
            invalid_amount: Response

            daily_win: Response
            daily_single_loss: Response

            not_daily_multiple_loss: Response
            not_daily_single_loss: Response

            not_daily_multiple_win: Response
            not_daily_lost_everything: Response

        class Stock(BaseTranslation):
            invalid_number: Response
            invalid_amount: Response
            single_stock: Response
            invalid_quantity: Response
            old_stock: Response
            multiple_stock: Response
            multiple_old_stock: Response
            daily_limit_reached: Response

        class Top(BaseTranslation):
            ranks: Response
            top10_ish: Response

    class Copy:
        class Copy(BaseTranslation):
            success: Response
            copy: Response
            wrong_id: Response

        class DeleteCopy(BaseTranslation):
            deleted: Response
            not_owner: Response
            error: Response

        class RandomCopy(BaseTranslation):
            success: Response

    class Dungeons:
        dungeonrank_dict: dict[str, dict[str, str | None]]

        class DungeonLevel(BaseTranslation):
            bot_nick: Response
            no_class_chosen: Response
            player_status: Response
            player_not_found: Response

        class DungeonRank(BaseTranslation):
            winrate: Response
            player_rank: str
            normal: Response

        class DungeonEnter(BaseTranslation):
            class_rank_up: Response
            class_to_choose: Response
            dungeon_result: Response
            cooldown: Response
            class_choice: Response
            class_first_choice: Response

        class DungeonFast(BaseTranslation):
            class_to_choose: Response
            cooldown: Response
            dungeon_result: Response
            class_first_choice: Response

    class General:
        class BotInfo(BaseTranslation):
            info: Response
            site: Response
            uptime: Response

        class Bug(BaseTranslation):
            bug_id: Response

        class Channels(BaseTranslation):
            quantity: Response
            names: Response

        class Color(BaseTranslation):
            user_not_found: Response
            unexpected_error: Response
            user_has_no_color: str
            user_color: str
            author_color: str
            response: Response
            response_link: Response

        class Dict(BaseTranslation):
            word_not_found: Response
            word: Response

        class Echo(BaseTranslation):
            echo: Response

        class Help(BaseTranslation):
            command_site: Response
            command: Response
            command_aliases: Response

        class Join(BaseTranslation):
            join_message: str
            already_in_channel_disabled: Response
            joined: Response
            already_in_channel: Response

        class LastSeen(BaseTranslation):
            bot_nick: Response
            author: Response
            author_not_found: Response
            not_authorized: Response
            last_seen: Response

        class Leave(BaseTranslation):
            not_in_channel: Response
            left: Response

        class Nicks(BaseTranslation):
            user_not_found: Response
            nicks: Response
            last_nick: Response
            no_nick: Response

        class Ping(BaseTranslation):
            ping: Response

        class PopOut(BaseTranslation):
            url: Response

        class Preview(BaseTranslation):
            no_stream: Response
            response: Response

        class Spam(BaseTranslation):
            number_not_valid: Response
            content_not_valid: Response
            response: Response

        class Suggest(BaseTranslation):
            suggest_id: Response

    class Infos:
        class AccountAge(BaseTranslation):
            user_not_found: Response
            birthday_year: Response
            birthday_years: Response
            birthday: Response
            age: Response

        class Avatar(BaseTranslation):
            user_not_found: Response
            author_avatar: Response
            bot_avatar: Response
            nick_avatar: Response

        class FirstFollow(BaseTranslation):
            first_and_follow: Response
            not_first_but_followed: Response
            follow_but_not_followed: Response
            alone: Response

        class FollowAge(BaseTranslation):
            user_not_found: Response
            follow_yourself: Response
            not_followed: Response
            follow: Response

        class Live(BaseTranslation):
            bot_nick: Response
            user_not_found: Response
            channel_offline: Response
            stream: Response
            stream_with_print: Response

        class Title(BaseTranslation):
            bot_nick: Response
            user_not_found: Response
            no_title_game: Response
            no_title: Response
            title_no_game: Response
            full_title: Response

    class Interactive:
        class Fight(BaseTranslation):
            options = fight_option
            bot_nick: Response
            internal_fight: Response
            already_fight: Response
            result: Response
            refused: Response
            timeout: Response

        class Hug(BaseTranslation):
            bot: Response
            yourself: Response
            hug: Response

        class Kiss(BaseTranslation):
            bot: Response
            yourself: Response
            kiss: Response

        class Love(BaseTranslation):
            yourself: Response
            ship: Response

        class Pat(BaseTranslation):
            bot: Response
            yourself: Response
            pat: Response

        class Penis(BaseTranslation):
            bot: Response
            penis: Response

        class Slap(BaseTranslation):
            bot: Response
            yourself: Response
            slap: Response

        class Tuck(BaseTranslation):
            bot: Response
            yourself: Response
            tuck: Response

    class Markov:
        class Markov(BaseTranslation):
            channel_not_found: Response
            user_not_found: Response
            no_start: Response
            markov_generated: Response

    class Marry:
        class Marry(BaseTranslation):
            bot: Response
            yourself: Response
            user_not_found: Response
            proposal_already_in_progress: Response
            someone_arrived_first: Response
            author_limit_reached: Response
            already_married: Response
            limit_reached: Response
            not_enough_cookies: Response

            proposal_message: str

            not_enough_cookies2: Response
            proposal_accept: Response
            no_proposal: Response

            proposal_denied: Response

            timeout: Response

        class Divorce(BaseTranslation):
            bot: Response
            yourself: Response
            not_married: Response
            user_not_found: Response
            divorce: Response
            wrong_person: Response

        class MarryAge(BaseTranslation):
            bot: Response
            user_not_found: Response
            not_married: Response
            response: Response
            married: str
            divorced: str

    class Pet:
        PetsDict: PetsDict
        FromListToPetList: PetFuncCallable

        class Pet(BaseTranslation):
            bot: Response
            user_not_found: Response
            mention_denied: Response
            pets: Response
            no_pets: Response
            user_no_pets: Response

        class PetBuy(BaseTranslation):
            no_cookies: Response
            not_enough_cookies: Response
            name_too_large: str
            timeout: Response
            timeout_response: Response
            what_name: str
            are_you_sure: str
            pet_name: str
            pet_buy: Response
            no_options: Response

        class PetList(BaseTranslation):
            pet_list: Response

        class PetName(BaseTranslation):
            no_pets: Response

            what_pet_to_name: str

            timeout: Response

            what_name: str

            new_name: Response

        class PetPat(BaseTranslation):
            no_pet_name: Response
            no_pets: Response
            pet_pat: Response
            wrong_pet_name: Response

        class PetSell(BaseTranslation):
            pass

    class Profile:
        class Mention(BaseTranslation):
            mention_on: Response

        class NickName(BaseTranslation):
            nickname_too_large: Response
            nickname_removed: Response
            nickname_changed: Response

        class SaveCity(BaseTranslation):
            city_removed: Response
            city_added: Response

        class SaveColor(BaseTranslation):
            color_removed: Response
            color_added: Response

        class UnMention(BaseTranslation):
            mention_off: Response

    class Reminder:
        class Remind(BaseTranslation):
            bot: Response
            user_not_found: Response
            user_opt_out: Response
            author_too_much_reminds: Response
            user_too_much_reminds: Response
            time_not_found: Response
            remind_on_back: Response
            dont_have_time_machine: Response
            minimum_time: Response
            remind_on_time: Response

        class Reminds(BaseTranslation):
            remind_for: Response
            remind_timed_with_content: Response
            remind_timed_without_content: Response
            remind_deleted: Response
            remind_not_found: Response
            no_id_selected: Response
            author_reminds: Response
            author_dont_have_reminds: Response

        class RemindListener(BaseTranslation):
            remind_timed_with_content: Response
            remind_timed_without_content: Response

    class Settings:
        class BanWord(BaseTranslation):
            word_added: Response
            word_already_on_list: Response

        class Disable(BaseTranslation):
            command_dont_exist: Response
            command_cannot_be_disabled: Response
            command_already_disabled: Response
            command_disabled: Response

        class Enable(BaseTranslation):
            command_dont_exist: Response
            command_reactivated: Response
            command_already_activated: Response

        class Prefix(BaseTranslation):
            prefix_invalid: Response
            prefix_invalid_or_absent: Response
            prefix_already_in_use: Response
            prefix_changed: Response
            prefix_too_large: Response

        class Start(BaseTranslation):
            already_on: Response
            started: Response

        class Stop(BaseTranslation):
            stopped: Response

        class UnBanWord(BaseTranslation):
            word_removed: Response
            word_not_found: Response

    class Tools:

        class Math(BaseTranslation):
            result: Response
            error: Response

        class Shorten(BaseTranslation):
            no_links_found: Response
            shorten_links: Response
            shorten_link: Response
            shorten_error: Response

        class Time(BaseTranslation):
            time: Response
            future_time: Response
            past_time: Response
            unit_not_found: Response
            too_much_time: Response

        class UserId(BaseTranslation):
            user_not_found: Response
            id_or_name: Response

        class Weather(BaseTranslation, WeatherTools):
            city_not_passed: Response
            city_not_found: Response
            weather: Response

            @staticmethod
            def format_weather(self: Response, ctx: Context, *args: Any, **kwargs: Any):
                pass

    class Tower:
        class EnterTower(BaseTranslation):
            class_rank_up: Response
            class_to_choose: Response
            cooldown: Response
            tower_result: Response
            class_choice: Response
            class_first_choice: Response

        class FastTower(BaseTranslation):
            class_to_choose: Response
            cooldown: Response
            tower_result: Response
            class_first_choice: Response

        class TowerLevel(BaseTranslation):
            bot_nick: Response
            no_class_chosen: Response
            player_status: Response
            player_not_found: Response















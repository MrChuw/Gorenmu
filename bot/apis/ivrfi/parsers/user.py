from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypeVar

from bot.apis.ivrfi.parsers.common import (
    from_bool,
    from_datetime,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
)

T = TypeVar("T")


@dataclass
class Badge:
    set_id: str | None = None
    title: str | None = None
    description: str | None = None
    version: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Badge":
        assert isinstance(obj, dict)
        set_id = from_union([from_str, from_none], obj.get("setID"))
        title = from_union([from_str, from_none], obj.get("title"))
        description = from_union([from_str, from_none], obj.get("description"))
        version = from_union([from_none, lambda x: int(from_str(x))], obj.get("version"))
        return Badge(set_id, title, description, version)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.set_id is not None:
            result["setID"] = from_union([from_str, from_none], self.set_id)
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.version is not None:
            result["version"] = from_union(
                [
                    lambda input_value: from_none(
                        (lambda checked_value: is_type(type(None), checked_value))(input_value)
                    ),
                    lambda input_value: from_str(
                        (lambda coerced_value: str((lambda int_candidate: is_type(int, int_candidate))(coerced_value)))(
                            input_value
                        )
                    ),
                ],
                self.version,
            )
        return result


@dataclass
class ChatSettings:
    chat_delay_ms: int | None = None
    followers_only_duration_minutes: int | None = None
    slow_mode_duration_seconds: int | None = None
    block_links: bool | None = None
    is_subscribers_only_mode_enabled: bool | None = None
    is_emote_only_mode_enabled: bool | None = None
    is_fast_subs_mode_enabled: bool | None = None
    is_unique_chat_mode_enabled: bool | None = None
    require_verified_account: bool | None = None
    rules: list[str] | None = None

    @staticmethod
    def from_dict(obj: Any) -> "ChatSettings":
        assert isinstance(obj, dict)
        chat_delay_ms = from_union([from_int, from_none], obj.get("chatDelayMs"))
        followers_only_duration_minutes = from_union([from_int, from_none], obj.get("followersOnlyDurationMinutes"))
        slow_mode_duration_seconds = from_union([from_int, from_none], obj.get("slowModeDurationSeconds"))
        block_links = from_union([from_bool, from_none], obj.get("blockLinks"))
        is_subscribers_only_mode_enabled = from_union([from_bool, from_none], obj.get("isSubscribersOnlyModeEnabled"))
        is_emote_only_mode_enabled = from_union([from_bool, from_none], obj.get("isEmoteOnlyModeEnabled"))
        is_fast_subs_mode_enabled = from_union([from_bool, from_none], obj.get("isFastSubsModeEnabled"))
        is_unique_chat_mode_enabled = from_union([from_bool, from_none], obj.get("isUniqueChatModeEnabled"))
        require_verified_account = from_union([from_bool, from_none], obj.get("requireVerifiedAccount"))
        rules = from_union([lambda x: from_list(from_str, x), from_none], obj.get("rules"))
        return ChatSettings(
            chat_delay_ms,
            followers_only_duration_minutes,
            slow_mode_duration_seconds,
            block_links,
            is_subscribers_only_mode_enabled,
            is_emote_only_mode_enabled,
            is_fast_subs_mode_enabled,
            is_unique_chat_mode_enabled,
            require_verified_account,
            rules,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.chat_delay_ms is not None:
            result["chatDelayMs"] = from_union([from_int, from_none], self.chat_delay_ms)
        if self.followers_only_duration_minutes is not None:
            result["followersOnlyDurationMinutes"] = from_union(
                [from_int, from_none], self.followers_only_duration_minutes
            )
        if self.slow_mode_duration_seconds is not None:
            result["slowModeDurationSeconds"] = from_union([from_int, from_none], self.slow_mode_duration_seconds)
        if self.block_links is not None:
            result["blockLinks"] = from_union([from_bool, from_none], self.block_links)
        if self.is_subscribers_only_mode_enabled is not None:
            result["isSubscribersOnlyModeEnabled"] = from_union(
                [from_bool, from_none], self.is_subscribers_only_mode_enabled
            )
        if self.is_emote_only_mode_enabled is not None:
            result["isEmoteOnlyModeEnabled"] = from_union([from_bool, from_none], self.is_emote_only_mode_enabled)
        if self.is_fast_subs_mode_enabled is not None:
            result["isFastSubsModeEnabled"] = from_union([from_bool, from_none], self.is_fast_subs_mode_enabled)
        if self.is_unique_chat_mode_enabled is not None:
            result["isUniqueChatModeEnabled"] = from_union([from_bool, from_none], self.is_unique_chat_mode_enabled)
        if self.require_verified_account is not None:
            result["requireVerifiedAccount"] = from_union([from_bool, from_none], self.require_verified_account)
        if self.rules is not None:
            result["rules"] = from_union([lambda x: from_list(from_str, x), from_none], self.rules)
        return result


@dataclass
class LastBroadcast:
    started_at: datetime | None = None
    title: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> "LastBroadcast":
        assert isinstance(obj, dict)
        started_at = from_union([from_datetime, from_none], obj.get("startedAt"))
        if isinstance(started_at, datetime) and started_at.tzinfo is not None:
            started_at = datetime.fromtimestamp(started_at.timestamp())
        title = from_union([from_none, from_str], obj.get("title"))
        return LastBroadcast(started_at, title)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.started_at is not None:
            result["startedAt"] = from_union([lambda x: x.isoformat(), from_none], self.started_at)
        if self.title is not None:
            result["title"] = from_union([from_none, from_str], self.title)
        return result


@dataclass
class Panel:
    id: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Panel":
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        return Panel(id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union(
                [
                    lambda input_value: from_none((lambda maybe_none: is_type(type(None), maybe_none))(input_value)),
                    lambda input_value: from_str(
                        (lambda intermediate: str((lambda maybe_int: is_type(int, maybe_int))(intermediate)))(
                            input_value
                        )
                    ),
                ],
                self.id,
            )
        return result


@dataclass
class Roles:
    is_affiliate: bool | None = None
    is_partner: bool | None = None
    is_staff: bool | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Roles":
        assert isinstance(obj, dict)
        is_affiliate = from_union([from_bool, from_none], obj.get("isAffiliate"))
        is_partner = from_union([from_bool, from_none], obj.get("isPartner"))
        is_staff = from_union([from_bool, from_none], obj.get("isStaff"))
        return Roles(is_affiliate, is_partner, is_staff)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.is_affiliate is not None:
            result["isAffiliate"] = from_union([from_bool, from_none], self.is_affiliate)
        if self.is_partner is not None:
            result["isPartner"] = from_union([from_bool, from_none], self.is_partner)
        if self.is_staff is not None:
            result["isStaff"] = from_union([from_bool, from_none], self.is_staff)
        return result


@dataclass
class Game:
    display_name: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Game":
        assert isinstance(obj, dict)
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        return Game(display_name)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.display_name is not None:
            result["displayName"] = from_union([from_str, from_none], self.display_name)
        return result


@dataclass
class Stream:
    title: str | None = None
    id: str | None = None
    created_at: datetime | None = None
    type: str | None = None
    viewers_count: int | None = None
    game: Game | None = None

    @staticmethod
    def from_dict(obj: Any) -> "Stream":
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        id = from_union([from_str, from_none], obj.get("id"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        if isinstance(created_at, datetime) and created_at.tzinfo is not None:
            created_at = datetime.fromtimestamp(created_at.timestamp())
        type = from_union([from_str, from_none], obj.get("type"))
        viewers_count = from_union([from_int, from_none], obj.get("viewersCount"))
        game = from_union([Game.from_dict, from_none], obj.get("game"))
        return Stream(title, id, created_at, type, viewers_count, game)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.created_at is not None:
            result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.viewers_count is not None:
            result["viewersCount"] = from_union([from_int, from_none], self.viewers_count)
        if self.game is not None:
            result["game"] = from_union([lambda x: to_class(Game, x), from_none], self.game)
        return result


@dataclass
class UserElement:
    banned: bool | None = None
    display_name: str | None = None
    login: str | None = None
    id: int | None = None
    bio: str | None = None
    follows: str | None = None
    followers: int | None = None
    profile_view_count: str | None = None
    chat_color: str | None = None
    logo: str | None = None
    banner: str | None = None
    verified_bot: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    emote_prefix: str | None = None
    roles: Roles | None = None
    badges: list[Badge] | None = None
    chatter_count: int | None = None
    chat_settings: ChatSettings | None = None
    stream: Stream | None = None
    last_broadcast: LastBroadcast | None = None
    panels: list[Panel] | None = None

    @staticmethod
    def from_dict(obj: Any) -> "UserElement":
        assert isinstance(obj, dict)
        banned = from_union([from_bool, from_none], obj.get("banned"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        login = from_union([from_str, from_none], obj.get("login"))
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        bio = from_union([from_str, from_none], obj.get("bio"))
        follows = from_none(obj.get("follows"))
        followers = from_union([from_int, from_none], obj.get("followers"))
        profile_view_count = from_none(obj.get("profileViewCount"))
        chat_color = from_union([from_none, from_str], obj.get("chatColor"))
        logo = from_union([from_str, from_none], obj.get("logo"))
        banner = from_union([from_none, from_str], obj.get("banner"))
        verified_bot = from_none(obj.get("verifiedBot"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        updated_at = from_union([from_datetime, from_none], obj.get("updatedAt"))
        emote_prefix = from_union([from_str, from_none], obj.get("emotePrefix"))
        roles = from_union([Roles.from_dict, from_none], obj.get("roles"))
        badges = from_union([lambda x: from_list(Badge.from_dict, x), from_none], obj.get("badges"))
        chatter_count = from_union([from_int, from_none], obj.get("chatterCount"))
        chat_settings = from_union([ChatSettings.from_dict, from_none], obj.get("chatSettings"))
        stream = from_union([from_none, Stream.from_dict], obj.get("stream"))
        last_broadcast = from_union([LastBroadcast.from_dict, from_none], obj.get("lastBroadcast"))
        panels = from_union([lambda x: from_list(Panel.from_dict, x), from_none], obj.get("panels"))
        return UserElement(
            banned,
            display_name,
            login,
            id,
            bio,
            follows,
            followers,
            profile_view_count,
            chat_color,
            logo,
            banner,
            verified_bot,
            created_at,
            updated_at,
            emote_prefix,
            roles,
            badges,
            chatter_count,
            chat_settings,
            stream,
            last_broadcast,
            panels,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.banned is not None:
            result["banned"] = from_union([from_bool, from_none], self.banned)
        if self.display_name is not None:
            result["displayName"] = from_union([from_str, from_none], self.display_name)
        if self.login is not None:
            result["login"] = from_union([from_str, from_none], self.login)
        if self.id is not None:
            result["id"] = from_union(
                [
                    lambda value: from_none((lambda val: is_type(type(None), val))(value)),
                    lambda value: from_str((lambda val: str((lambda inner_val: is_type(int, inner_val))(val)))(value)),
                ],
                self.id,
            )
        if self.bio is not None:
            result["bio"] = from_union([from_str, from_none], self.bio)
        if self.follows is not None:
            result["follows"] = from_none(self.follows)
        if self.followers is not None:
            result["followers"] = from_union([from_int, from_none], self.followers)
        if self.profile_view_count is not None:
            result["profileViewCount"] = from_none(self.profile_view_count)
        if self.chat_color is not None:
            result["chatColor"] = from_union([from_none, from_str], self.chat_color)
        if self.logo is not None:
            result["logo"] = from_union([from_str, from_none], self.logo)
        if self.banner is not None:
            result["banner"] = from_union([from_none, from_str], self.banner)
        if self.verified_bot is not None:
            result["verifiedBot"] = from_none(self.verified_bot)
        if self.created_at is not None:
            result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.updated_at is not None:
            result["updatedAt"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.emote_prefix is not None:
            result["emotePrefix"] = from_union([from_str, from_none], self.emote_prefix)
        if self.roles is not None:
            result["roles"] = from_union([lambda x: to_class(Roles, x), from_none], self.roles)
        if self.badges is not None:
            result["badges"] = from_union(
                [
                    lambda x: from_list(lambda item_lambda: to_class(Badge, x), x),
                    from_none,
                ],
                self.badges,
            )
        if self.chatter_count is not None:
            result["chatterCount"] = from_union([from_int, from_none], self.chatter_count)
        if self.chat_settings is not None:
            result["chatSettings"] = from_union([lambda x: to_class(ChatSettings, x), from_none], self.chat_settings)
        if self.stream is not None:
            result["stream"] = from_union([from_none, lambda x: to_class(Stream, x)], self.stream)
        if self.last_broadcast is not None:
            result["lastBroadcast"] = from_union([lambda x: to_class(LastBroadcast, x), from_none], self.last_broadcast)
        if self.panels is not None:
            result["panels"] = from_union(
                [
                    lambda x: from_list(lambda item_lambda: to_class(Panel, x), x),
                    from_none,
                ],
                self.panels,
            )
        return result


def user_from_dict(s: Any) -> list[UserElement]:
    return from_list(UserElement.from_dict, s)


def user_to_dict(item_list: list[UserElement]) -> Any:
    return from_list(lambda item_lambda: to_class(UserElement, item_list), item_list)

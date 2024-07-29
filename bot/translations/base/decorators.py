from __future__ import annotations

from typing import TYPE_CHECKING

from twitchio.ext.commands import Command, Context as TwitchioContext

if TYPE_CHECKING:
    from bot.ext.commands import Context


class BaseDecorator:
    helper: str
    usage: str
    description: str


class BaseDecorators:
    @staticmethod
    def get_decorator(source: Context | Command, ctx: Context) -> BaseDecorator | None:
        decorators = None
        if isinstance(source, TwitchioContext):
            decorators = source.command.decorators
        elif isinstance(source, Command):
            decorators = source.decorators

        for classe in dir(BaseDecorators):
            for attr_name in dir(getattr(BaseDecorators, classe)):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(getattr(BaseDecorators, classe), attr_name)
                if isinstance(decorators, attr):
                    decorator_class = getattr(
                        ctx.bot.TranslationManager.get_decorator(ctx.user.language or "pt-br"),
                        classe,
                        None,
                    )
                    if decorator_class:
                        decorator_class = getattr(decorator_class, attr_name)
                        return decorator_class()
        return None

    @staticmethod
    def get_helper(source: Context | Command, ctx: Context, prefix: str) -> str:
        return BaseDecorators.get_decorator(source, ctx).helper.format(prefix)

    @staticmethod
    def get_usage(source: Context | Command, ctx: Context, prefix: str) -> str:
        return BaseDecorators.get_decorator(source, ctx).usage.format(prefix)

    @staticmethod
    def get_description(source: Context | Command, ctx: Context) -> str:
        return BaseDecorators.get_decorator(source, ctx).description

    class IDE:
        class TypeChecking(BaseDecorator):
            pass

    class Activity:
        class Afk(BaseDecorator):
            pass

        class IsAfk(BaseDecorator):
            pass

        class RAfk(BaseDecorator):
            pass

    class Admin:
        class AddUser(BaseDecorator):
            pass

        class AddBot(BaseDecorator):
            pass

        class AllChannels(BaseDecorator):
            pass

        class Announce(BaseDecorator):
            pass

        class ApiBot(BaseDecorator):
            pass

        class ChannelLog(BaseDecorator):
            pass

        class CookieGive(BaseDecorator):
            pass

        class CountUser(BaseDecorator):
            pass

        class DBGrep(BaseDecorator):
            pass

        class DelFromDB(BaseDecorator):
            pass

        class DisableNSFW(BaseDecorator):
            pass

        class LotteryStart(BaseDecorator):
            pass

        class Nada(BaseDecorator):
            pass

        class Reload(BaseDecorator):
            pass

        class Restart(BaseDecorator):
            pass

        class RGit(BaseDecorator):
            pass

    class Random:
        class Chance(BaseDecorator):
            pass

        class Choice(BaseDecorator):
            pass

        class Count(BaseDecorator):
            pass

        class HyperTranslate(BaseDecorator):
            pass

        class Imgur(BaseDecorator):
            pass

        class Imgur7(BaseDecorator):
            pass

        class ImgurRepeated(BaseDecorator):
            pass

        class RandomColor(BaseDecorator):
            pass

        class Reverse(BaseDecorator):
            pass

        class RandomLine(BaseDecorator):
            pass

        class Scp(BaseDecorator):
            pass

        class UpSideDown(BaseDecorator):
            pass

        class Wikihow(BaseDecorator):
            pass

        class Wikipedia(BaseDecorator):
            pass

    class Annotations:
        class Annotation(BaseDecorator):
            pass

        class Annotations(BaseDecorator):
            pass

    class Lottery:
        class Bet(BaseDecorator):
            pass

        class Lottery(BaseDecorator):
            pass

    class NSFW:
        class Boru(BaseDecorator):
            pass

        class AllBoorus(BaseDecorator):
            pass

    class Cookies:
        class Cookie(BaseDecorator):
            pass

        class CookieCount(BaseDecorator):
            pass

        class Gift(BaseDecorator):
            pass

        class SlotMachine(BaseDecorator):
            pass

        class Stock(BaseDecorator):
            pass

        class Top(BaseDecorator):
            pass

    class Copy:
        class Copy(BaseDecorator):
            pass

        class DeleteCopy(BaseDecorator):
            pass

        class RandomCopy(BaseDecorator):
            pass

    class Dungeons:
        class DungeonLevel(BaseDecorator):
            pass

        class DungeonRank(BaseDecorator):
            pass

        class DungeonEnter(BaseDecorator):
            pass

        class DungeonFast(BaseDecorator):
            pass

    class General:
        class BotInfo(BaseDecorator):
            pass

        class Bug(BaseDecorator):
            pass

        class Channels(BaseDecorator):
            pass

        class Color(BaseDecorator):
            pass

        class Dict(BaseDecorator):
            pass

        class Echo(BaseDecorator):
            pass

        class Help(BaseDecorator):
            pass

        class Join(BaseDecorator):
            pass

        class LastSeen(BaseDecorator):
            pass

        class Leave(BaseDecorator):
            pass

        class Nicks(BaseDecorator):
            pass

        class Ping(BaseDecorator):
            pass

        class PopOut(BaseDecorator):
            pass

        class Preview(BaseDecorator):
            pass

        class Spam(BaseDecorator):
            pass

        class Suggest(BaseDecorator):
            pass

    class Infos:
        class AccountAge(BaseDecorator):
            pass

        class Avatar(BaseDecorator):
            pass

        class FirstFollow(BaseDecorator):
            pass

        class FollowAge(BaseDecorator):
            pass

        class Live(BaseDecorator):
            pass

        class Title(BaseDecorator):
            pass

    class Interactive:
        class Fight(BaseDecorator):
            pass

        class Hug(BaseDecorator):
            pass

        class Kiss(BaseDecorator):
            pass

        class Love(BaseDecorator):
            pass

        class Pat(BaseDecorator):
            pass

        class Penis(BaseDecorator):
            pass

        class Slap(BaseDecorator):
            pass

        class Tuck(BaseDecorator):
            pass

    class Markov:
        class Markov(BaseDecorator):
            pass

    class Marry:
        class Marry(BaseDecorator):
            pass

        class Divorce(BaseDecorator):
            pass

        class MarryAge(BaseDecorator):
            pass

    class Pet:
        class Pet(BaseDecorator):
            pass

        class PetBuy(BaseDecorator):
            pass

        class PetList(BaseDecorator):
            pass

        class PetName(BaseDecorator):
            pass

        class PetPat(BaseDecorator):
            pass

        class PetSell(BaseDecorator):
            pass

    class Profile:
        class NickName(BaseDecorator):
            pass

        class SaveColor(BaseDecorator):
            pass

        class SaveCity(BaseDecorator):
            pass

        class Mention(BaseDecorator):
            pass

        class UnMention(BaseDecorator):
            pass

    class Reminder:
        class Remind(BaseDecorator):
            pass

        class Reminds(BaseDecorator):
            pass

    class Settings:
        class BanWord(BaseDecorator):
            pass

        class Disable(BaseDecorator):
            pass

        class Enable(BaseDecorator):
            pass

        class Prefix(BaseDecorator):
            pass

        class Start(BaseDecorator):
            pass

        class Stop(BaseDecorator):
            pass

        class UnBanWord(BaseDecorator):
            pass

    class Tools:
        class Math(BaseDecorator):
            pass

        class Shorten(BaseDecorator):
            pass

        class Time(BaseDecorator):
            pass

        class UserId(BaseDecorator):
            pass

        class Weather(BaseDecorator):
            pass

    class Tower:
        class EnterTower(BaseDecorator):
            pass

        class FastTower(BaseDecorator):
            pass

        class TowerLevel(BaseDecorator):
            pass















































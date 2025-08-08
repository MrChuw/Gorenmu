# -*- coding: utf-8 -*-
from twitchio.ext.commands import CommandExistsError  # NOQA
from twitchio.ext.commands import (
    BadArgument,
    CommandInvokeError,
    CommandNotFound,
    CommandOnCooldown,
    GuardFailure,
    MissingRequiredArgument,
    ModuleAlreadyLoadedError,
    ModuleLoadFailure,
)

InvalidArgument = (BadArgument, MissingRequiredArgument)


class InvalidUsername(BadArgument):
    pass


# Base custom Guard error
class CustomGuardError(GuardFailure):
    __slots__ = ()


class AlreadyPlaying(CustomGuardError):
    pass


class BotOffline(CustomGuardError):
    pass


class CommandDisabled(CustomGuardError):
    pass


class ModRequired(CustomGuardError):
    pass


class DevRequired(CustomGuardError):
    pass


class OwnerRequired(CustomGuardError):
    pass


class UserIsNotAllowed(CustomGuardError):
    pass


class ContentHasBanword(CustomGuardError):
    pass


class GameIsAlreadyRunning(CustomGuardError):
    pass


class VipRequired(CustomGuardError):
    pass


class SubRequired(CustomGuardError):
    pass


class UnknownError(CustomGuardError):
    pass


class MissingOAuthTokenError(Exception):
    pass

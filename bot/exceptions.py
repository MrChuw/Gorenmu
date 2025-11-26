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

__all__ = [
    CommandExistsError,
    CommandInvokeError,
    CommandNotFound,
    CommandOnCooldown,
    ModuleAlreadyLoadedError,
    ModuleLoadFailure,
    InvalidArgument,
    "InvalidUsernameError",
    "CustomGuardError",
    "AlreadyPlayingError",
    "BotOfflineError",
    "CommandDisabledError",
    "ModRequiredError",
    "DevRequiredError",
    "OwnerRequiredError",
    "UserIsNotAllowedError",
    "ContentHasBanwordError",
    "GameIsAlreadyRunningError",
    "VipRequiredError",
    "SubRequiredError",
    "UnknownErrorError",
    "MissingOAuthTokenError",
]


class InvalidUsernameError(BadArgument):
    pass


# Base custom Guard error
class CustomGuardError(GuardFailure):
    __slots__ = ()


class AlreadyPlayingError(CustomGuardError):
    pass


class BotOfflineError(CustomGuardError):
    pass


class CommandDisabledError(CustomGuardError):
    pass


class ModRequiredError(CustomGuardError):
    pass


class DevRequiredError(CustomGuardError):
    pass


class OwnerRequiredError(CustomGuardError):
    pass


class UserIsNotAllowedError(CustomGuardError):
    pass


class ContentHasBanwordError(CustomGuardError):
    pass


class GameIsAlreadyRunningError(CustomGuardError):
    pass


class VipRequiredError(CustomGuardError):
    pass


class SubRequiredError(CustomGuardError):
    pass


class UnknownErrorError(CustomGuardError):
    pass


class MissingOAuthTokenError(Exception):
    pass

# -*- coding: utf-8 -*-
from twitchio.ext.commands import (  # NOQA
    BadArgument,
    GuardFailure,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
    CommandInvokeError,
    CommandExistsError,
    ModuleLoadFailure,
    ModuleAlreadyLoadedError,
    # TwitchCommandError,
    # InvalidCogMethod,
    # InvalidCog,
    # ArgumentParsingFailed,
)

# TODO: Limpar os erros.
InvalidArgument = (BadArgument, MissingRequiredArgument)


class InvalidUsername(BadArgument):
    """Username invalido."""


class AlreadyPlaying(GuardFailure):
    """Um jogo ja esta rodando nesse canal."""


class BotOffline(GuardFailure):
    """Bot offline neste canal."""


class CommandDisabled(GuardFailure):
    """Comando esta disablilitado neste canal."""


class InappropriateMessage(GuardFailure):
    """Mensagem contem conteúdo inapropriado para o canal."""


class ModRequired(GuardFailure):
    """Usuário não é autorizado a usar este comando no canal."""


class PremiumRequired(GuardFailure):
    """Usuário não é autorizado a usar este comando no canal."""


class DevRequired(GuardFailure):
    """Usuário não é autorizado a usar este comando."""


class OwnerRequired(GuardFailure):
    """Usuário não é autorizado a usar este comando."""


class ConfRequired(GuardFailure):
    """Você precisa receber a confiança para usar este comando."""


class UserIsNotAllowed(GuardFailure):
    """ """


class ContentHasBanword(GuardFailure):
    """ """


class GameIsAlreadyRunning(GuardFailure):
    """ """


class VipRequired(GuardFailure):
    """ """


class SubRequired(GuardFailure):
    """ """


class UnknownError(GuardFailure):
    """ """


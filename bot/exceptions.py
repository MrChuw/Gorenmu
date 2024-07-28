# -*- coding: utf-8 -*-
from twitchio.ext.commands.errors import (  # NOQA
    BadArgument,
    CheckFailure,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
    TwitchCommandError,
    InvalidCogMethod,
    InvalidCog,
    MissingRequiredArgument,
    BadArgument,
    ArgumentParsingFailed,
    CommandNotFound,
    CommandOnCooldown,
    CheckFailure,
)

# TODO: Limpar os erros.
InvalidArgument = (ArgumentParsingFailed, BadArgument, MissingRequiredArgument)


class InvalidUsername(BadArgument):
    """Username invalido."""


class AlreadyPlaying(CheckFailure):
    """Um jogo ja esta rodando nesse canal."""


class BotOffline(CheckFailure):
    """Bot offline neste canal."""


class CommandDisabled(CheckFailure):
    """Comando esta disablilitado neste canal."""


class InappropriateMessage(CheckFailure):
    """Mensagem contem conteúdo inapropriado para o canal."""


class ModRequired(CheckFailure):
    """Usuário não é autorizado a usar este comando no canal."""


class PremiumRequired(CheckFailure):
    """Usuário não é autorizado a usar este comando no canal."""


class DevRequired(CheckFailure):
    """Usuário não é autorizado a usar este comando."""


class OwnerRequired(CheckFailure):
    """Usuário não é autorizado a usar este comando."""


class ConfRequired(CheckFailure):
    """Você precisa receber a confiança para usar este comando."""


class UserIsNotAllowed(CheckFailure):
    """ """


class ContentHasBanword(CheckFailure):
    """ """


class GameIsAlreadyRunning(CheckFailure):
    """ """


class VipRequired(CheckFailure):
    """ """


class SubRequired(CheckFailure):
    """ """


class UnknownError(CheckFailure):
    """ """


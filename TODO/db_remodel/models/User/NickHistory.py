from __future__ import annotations

from tortoise import fields

from models.base import Base, NickHistory
from models.timezonefield import DatetimeTzField
from typing import Any, List, Optional, Tuple, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.User.User import User


# TODO:
#   await Tortoise._db.execute_query("ALTER TABLE historico_de_nicks RENAME TO nick_history;")
#   talvez usar assim. criar um pre-check antes do bot iniciar que garante que ele trocou realmente o nome da tabela
class Historico_de_Nicks(Base):
    nicks: NickHistory = fields.TextField()
    created_at: DatetimeTzField = DatetimeTzField(auto_now_add=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="historico_de_nicks"
    )

    def __sizeof__(self):
        return len(self.nicks)

    class Meta:
        table = "historico_de_nicks"

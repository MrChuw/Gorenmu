# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from typing import Optional, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from bot.models import Player




class Rank:
    def __init__(self, _name: str, _order_by: str, _title: str, _class: str | None) -> None:
        self._name = _name
        self._order_by = _order_by
        self._title = _title
        self._class = _class

    @property
    def name(self) -> str:
        return self._name

    @property
    def order_by(self) -> str:
        return self._order_by

    @property
    def title(self) -> str:
        return self._title

    @property
    def class_(self) -> str | None:
        return self._class



class Dungeon:
    def __init__(self, data: dict) -> None:
        self.rank_dict = self.generate_rank(data["Rank"])
        self.classes = self.create_classes(data["Classes"])
        self.quotes: list[dict] = data["Quotes"]
        pass

    @staticmethod
    def generate_rank(data: dict) -> dict:
        ranks = {}
        for key, value in data.items():
            if key is "winrate":
                ranks[key] = Rank(_name=key, _order_by="wins", _title=value, _class=None)
            elif key in ["victory", "victories", "win", "wins"]:
                ranks[key] = Rank(_name=key, _order_by="wins", _title=value, _class=None)
            elif key in ["defeat", "defeats", "lose", "losses"]:
                ranks[key] = Rank(_name=key, _order_by="defeats", _title=value, _class=None)
            elif key in ["warrior", "warriors", "warrior_f", "warriors_f"]:
                ranks[key] = Rank(_name=key, _order_by="level", _title=value, _class="w")
            elif key in ["mage", "mages", "mage_f", "mages_f"]:
                ranks[key] = Rank(_name=key, _order_by="level", _title=value, _class="m")
            elif key in ["archer", "archers", "archer_f", "archers_f"]:
                ranks[key] = Rank(_name=key, _order_by="level", _title=value, _class="a")
            elif key is "default":
                ranks[key] = Rank(_name=key, _order_by="level", _title=value, _class=None)
        return ranks

    @staticmethod
    def create_classes(data: dict) -> dict[str, dict[str, str | dict[str, list[str]]]]:
        __w_M_A: list[str] = data["Warrior 1"]
        __w_M_B: list[str] = data["Warrior 2"]
        __w_F_A: list[str] = data["Female Warrior 1"]
        __w_F_B: list[str] = data["Female Warrior 2"]
        __a_M_A: list[str] = data["Archer 1"]
        __a_M_B: list[str] = data["Archer 2"]
        __a_F_A: list[str] = data["Female Archer 1"]
        __a_F_B: list[str] = data["Female Archer 2"]
        __m_M_A: list[str] = data["Mage 1"]
        __m_M_B: list[str] = data["Mage 2"]
        __m_F_A: list[str] = data["Female Mage 1"]
        __m_F_B: list[str] = data["Female Mage 2"]
        return {
            "w": {"M": {"A": __w_M_A, "B": __w_M_B}, "F": {"A": __w_F_A, "B": __w_F_B}, "emoji": "⚔️"},
            "a": {"M": {"A": __a_M_A, "B": __a_M_B}, "F": {"A": __a_F_A, "B": __a_F_B}, "emoji": "🏹"},
            "m": {"M": {"A": __m_M_A, "B": __m_M_B}, "F": {"A": __m_F_A, "B": __m_F_B}, "emoji": "🧙"},
        }


    def generate_dungeon(self, dungeon: int = None) -> Tuple[dict, int]:
        dungeons = self.quotes
        dungeon = int(dungeon) if dungeon else random.randint(0, len(dungeons) - 1)
        return dungeons[dungeon], dungeon


    def resume_dungeon(self, player: Player, choice: str = None, multiplier: int = 1) -> Tuple[Player, str]:
        d = self.generate_dungeon(player.dungeon)[0]
        result = random.choices(["win", "lose"], weights=(0.90, 0.10), k=1)[0]
        if not choice:
            choice = random.choice(["1", "2"])
            quote, options = d["quote"].split('"+ed 1"')
            option = (
                options.split('ou "+ed 2"')[int(choice) - 1].replace("para", "Você decide", 1).rstrip()
            )
            response = quote + option + ". "
            response += d[choice][result]
        else:
            response = d[choice][result]
        if result == "win":
            player.wins += 1
            gained = (random.randint(50, 75) + 3 * player.level) * multiplier
            player.xp += gained
            response += f" +{gained} XP."
            if player.xp > 100 * player.level + 25 * sum(range(1, player.level + 1)):
                player.level += +1
                if player.level % 10 == 0 and player.level < 70:
                    response += f", alcançou level {player.level} ⬆"
                    if player.level == 30:
                        op1, op2 = self.options_sub_class(player.class_, player.gender)
                        player.sub_class = ""
                        response += f" e pode se tornar {op1} ou {op2}!"
                    else:
                        lvl = player.level // 10 if player.level < 60 else 7
                        if lvl in self.classes[player.class_][player.gender][player.sub_class]:
                            c = self.classes[player.class_][player.gender][player.sub_class][lvl]
                            response += f" e se tornou {c}"
                else:
                    response += f" e alcançou level {player.level} ⬆"
        else:
            player.defeats += 1
            response += " 0 XP"
        player.dungeon = ""
        return player, response


    def options_class(self) -> dict:
        initial_classes = {}
        for class_, c in self.classes.items():
            initial_classes[c["M"]["A"][0]] = {"class_": class_, "gender": "M"}
            initial_classes[c["F"]["A"][0]] = {"class_": class_, "gender": "F"}
        return initial_classes


    def options_sub_class(self, class_: str, gender: str) -> tuple[str, str]:
        option_a = self.classes[class_][gender]["A"][3]
        option_b = self.classes[class_][gender]["B"][3]
        return option_a, option_b


    def choose_class(self, choice: str) -> Optional[str]:
        options = self.options_class()
        for option, values in options.items():
            if choice == option.lower():
                return values


    def choose_sub_class(self, choice: str, class_: str, gender: str) -> Optional[str]:
        options = self.options_sub_class(class_, gender)
        if choice == options[0].lower():
            return "A"
        if choice == options[1].lower():
            return "B"

from dataclasses import dataclass

@dataclass
class Values:
    _name: str
    _value: int
    _right_name: str

    @property
    def value(self) -> int:
        return self._value

    @property
    def name(self) -> str:
        return f"{self._name}"

    @property
    def right_name(self) -> str:
        return f"{self._right_name}"


bets_values: dict = {
    1: Values("One dozen", 5, "Dozen"),
    2: Values("Pair", 5, "Pair"),
    3: Values("Triple", 5, "Triple"),
    4: Values("Quad", 5, "Quad"),
    5: Values("Quintuple", 5, "Quintuple"),
    6: Values("Sextuple", 5, "Sextuple"),
    7: Values("Septuple", 5, "Septuple"),
    8: Values("Octuple", 5, "Octuple"),
    9: Values("Nonuple", 5, "Nonuple"),
    10: Values("Decuple", 5, "Decuple"),
    11: Values("Undecuple", 5, "Undecuple"),
    12: Values("Duodecuple", 5, "Duodecuple"),
    13: Values("Tredecuple", 5, "Tredecuple"),
    14: Values("Quattuordecuple", 5, "Quattuordecuple"),
    15: Values("Quindecuple", 5, "Close"),
}

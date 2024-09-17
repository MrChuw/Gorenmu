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
    1: Values("Uma dezena", 5, "Dezena"),
    2: Values("Duque", 5, "Duque"),
    3: Values("Terno", 5, "Terno"),
    4: Values("Quadra", 5, "Quadra"),
    5: Values("Quina", 5, "Quina"),
    6: Values("Sena", 5, "Sena"),
    7: Values("Heptasena", 11, "Septena"),
    8: Values("Octasena", 25, "Octena"),
    9: Values("Nonasena", 63, "Nona"),
    10: Values("Decasena", 187, "Dezena"),
    11: Values("Hendecasena", 346, "Undezena"),
    12: Values("Dodecasena", 649, "Dozezena"),
    13: Values("Tridecasena", 943, "Trezena"),
    14: Values("Tetradasena", 1038, "Quatorzena"),
    15: Values("Pentadasena", 1294, "Fechamento"),
}












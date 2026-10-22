class Unit:
    def __init__(self, value: "int | float | Unit", unit_str: str) -> None:
        self._conversion: dict[str, float] = {
            'm': 1.0,
            'cm': 0.01,
            'mm': 0.001,
            'km': 1000.0,
            'inch': 0.0254,
            'in': 0.0254,
            'ft': 0.3048,
            'yard': 0.9144,
            'yd': 0.9144,
            'mile': 1609.344,
            'mi': 1609.344,
            'g': 0.001,
            'kg': 1.0,
            'tonne': 1000.0,
            'lb': 0.45359237,
            'pound': 0.45359237,
            'oz': 0.028349523125,
            's': 1.0,
            'sec': 1.0,
            'min': 60.0,
            'hour': 3600.0,
            'h': 3600.0,
            'day': 86400.0,
            'K': 1.0,
            'degC': 1.0,
            'degF': 1.0,
        }

        self._offset: dict[str, float] = {'K': 0.0, 'degC': 273.15, 'degF': 459.67}

        if isinstance(value, Unit):
            self.value = value.value  # noqa
            self.unit = value.unit  # noqa
            return

        self.value = value
        self.unit = unit_str

    def to(self, target_unit: str) -> 'Unit':
        dim = self._dimension(self.unit)
        if dim != self._dimension(target_unit):
            raise ValueError(
                f"Incompatible units: {self.unit} -> {target_unit}", self.unit, target_unit, "ERR_DIMENSION"
            )
        factor_self = self._conversion.get(self.unit, 1.0)
        factor_target = self._conversion.get(target_unit, 1.0)
        offset_self = self._offset.get(self.unit, 0.0)
        offset_target = self._offset.get(target_unit, 0.0)
        if dim == 'temperature':
            kelvin = self.value * factor_self + offset_self
            new_value = (kelvin - offset_target) / factor_target
        else:
            new_value = self.value * factor_self / factor_target
        return Unit(new_value, target_unit)

    @staticmethod
    def _dimension(unit: str) -> str:
        if unit in ['m', 'cm', 'mm', 'km', 'inch', 'in', 'ft', 'yard', 'yd', 'mile', 'mi']:
            return 'length'
        if unit in ['g', 'kg', 'tonne', 'lb', 'pound', 'oz']:
            return 'mass'
        if unit in ['s', 'sec', 'min', 'hour', 'h', 'day']:
            return 'time'
        if unit in ['K', 'degC', 'degF']:
            return 'temperature'
        raise ValueError(f"Unknown dimension for unit {unit}", unit, "ERR_UNIT")

    def __add__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.to(self.unit)
            return Unit(self.value + other.value, self.unit)
        return Unit(self.value + other, self.unit)

    def __sub__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.to(self.unit)
            return Unit(self.value - other.value, self.unit)
        return Unit(self.value - other, self.unit)

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit(self.value * other.value, f"{self.unit}*{other.unit}")
        return Unit(self.value * other, self.unit)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return Unit(self.value / other.value, f"{self.unit}/{other.unit}")
        return Unit(self.value / other, self.unit)

    def __pow__(self, power):
        return Unit(self.value**power, f"{self.unit}^{power}")

    def __neg__(self):
        return Unit(-self.value, self.unit)

    def __abs__(self):
        return Unit(abs(self.value), self.unit)

    def __eq__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.to(self.unit)
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.to(self.unit)
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.to(self.unit)
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.to(self.unit)
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.to(self.unit)
            return self.value >= other.value
        return self.value >= other

    def __repr__(self):
        return f"Unit({self.value}, '{self.unit}')"

    def __str__(self):
        return f"{self.value} {self.unit}"

    def format(self, options=None) -> str:  # noqa
        return str(self)

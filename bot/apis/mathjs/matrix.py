from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from typing import Any

import numpy as np


class Index:
    def __init__(self, *indices):
        self.indices = indices

    def __repr__(self):
        return f"Index({', '.join(map(str, self.indices))})"


def index(*args):
    return Index(*args)


class _RawNum(str):
    def __repr__(self) -> str:
        return self


class Matrix(np.ndarray):
    def __new__(cls, data=None, dtype=None):
        if data is None:
            data = []
        if isinstance(data, Matrix):
            return data.view(cls)
        arr = np.array(data, dtype=dtype)
        return arr.view(cls)

    def __mul__(self, other):
        if isinstance(other, (int, float, complex, Decimal)):
            if self._scalar_overflows_float(other):
                return self._multiply_with_decimal(other)
            return Matrix(np.multiply(self, other))
        if isinstance(other, np.ndarray) and other.ndim == 2 and self.ndim == 2:
            return Matrix(np.matmul(self, other))
        return Matrix(np.multiply(self, other))

    @staticmethod
    def _scalar_overflows_float(value: Any) -> bool:
        if isinstance(value, bool):
            return False
        if isinstance(value, (int, Decimal)):
            try:
                float(value)
            except OverflowError:
                return True
        return False

    def _multiply_with_decimal(self, other: Any) -> Matrix:
        other_dec = other if isinstance(other, Decimal) else Decimal(other)

        def _mul(x: Any) -> Decimal:
            x_dec = x if isinstance(x, Decimal) else Decimal(str(x))
            return x_dec * other_dec

        return self.map(_mul)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        return Matrix(super().__add__(other))

    def __sub__(self, other):
        return Matrix(super().__sub__(other))

    def __truediv__(self, other):
        return Matrix(np.divide(self, other))

    def __pow__(self, power):  # noqa  # ty: ignore[invalid-method-override]
        is_int_power = isinstance(power, (int, np.integer)) and not isinstance(power, bool)
        if is_int_power and self.ndim == 2 and self.shape[0] == self.shape[1]:
            return self._matrix_power(int(power))
        return Matrix(np.power(self, power))

    def _matrix_power(self, power: int) -> Matrix:
        n = self.shape[0]

        if power == 0:
            return Matrix(np.eye(n, dtype=int).astype(object))

        if power < 0:
            base = Matrix(np.linalg.inv(self.astype(float))).astype(object)
            power = -power
        else:
            base = self.astype(object)

        result = Matrix(np.eye(n, dtype=int).astype(object))
        p = power
        while p > 0:
            if p & 1:
                result = Matrix(np.matmul(result, base))
            p >>= 1
            if p > 0:
                base = Matrix(np.matmul(base, base))
        return result

    def __neg__(self):
        return Matrix(-self)

    def transpose(self):  # noqa  # ty: ignore[invalid-method-override]
        return Matrix(self.T)

    def conjugate(self):
        return Matrix(np.conj(self))

    def tolist(self):
        return np.ndarray.tolist(self)

    def __repr__(self) -> str:
        return f"Matrix({self.tolist()})"

    def __str__(self) -> str:
        return str(self.tolist())

    def astype(self, dtype):  # noqa  # ty: ignore[invalid-method-override]
        return Matrix(super().astype(dtype))

    def subset(self, idx, replacement=None):
        np_idx = idx.indices if isinstance(idx, Index) else idx

        if isinstance(np_idx, (int, np.integer)):
            np_idx = (np_idx,)

        if replacement is None:
            if self.ndim == 1 and len(np_idx) == 1:
                i = np_idx[0]
                if i < 1:
                    raise IndexError("Index out of range (1-based)", i, "ERR_INDEX")
                if i > len(self):
                    return None
                return self[i - 1]
            return self[np_idx]
        else:
            if self.ndim == 1 and len(np_idx) == 1:
                i = np_idx[0]
                data = self.tolist()
                while len(data) < i:
                    data.append(0)
                data[i - 1] = replacement
                return Matrix(data)
            else:
                try:
                    self[np_idx] = replacement
                    return Matrix(self.copy())
                except IndexError as e:
                    new_shape = list(self.shape)
                    for dim, idx_val in enumerate(np_idx):
                        if isinstance(idx_val, (int, np.integer)) and idx_val >= new_shape[dim]:
                            new_shape[dim] = idx_val + 1
                    new_data = np.zeros(new_shape)
                    if self.size > 0:
                        slices = tuple(slice(0, s) for s in self.shape)
                        new_data[slices] = self
                    new_data[np_idx] = replacement
                    return Matrix(new_data)

    def map(self, func: Callable[[Any], Any]) -> Matrix:
        vec_func = np.vectorize(func, otypes=[object])
        return Matrix(vec_func(self))

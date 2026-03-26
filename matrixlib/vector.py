"""vector.py
Purpose: Lightweight vector operations for structural analysis.
Assumptions: Real-valued vectors only.
Units: Unit-agnostic; inherited from problem data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Vector:
    """Dense vector container.

    Inputs:
        values: Iterable numeric values.
    Outputs:
        Vector object with mutable `values` list.
    """

    values: List[float]

    @classmethod
    def zeros(cls, n: int) -> "Vector":
        return cls([0.0] * n)

    @classmethod
    def from_iterable(cls, values: Iterable[float]) -> "Vector":
        return cls([float(v) for v in values])

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, idx: int) -> float:
        return self.values[idx]

    def __setitem__(self, idx: int, value: float) -> None:
        self.values[idx] = float(value)

    def copy(self) -> "Vector":
        return Vector(self.values.copy())

    def dot(self, other: "Vector") -> float:
        if len(self) != len(other):
            raise ValueError("Vector length mismatch")
        return sum(a * b for a, b in zip(self.values, other.values))

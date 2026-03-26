"""dense.py
Purpose: Basic dense matrix class for small element-level operations.
Assumptions: Square matrices are used in solvers/element routines.
Units: Unit-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from matrixlib.vector import Vector


@dataclass
class DenseMatrix:
    data: List[List[float]]

    @classmethod
    def zeros(cls, rows: int, cols: int) -> "DenseMatrix":
        return cls([[0.0 for _ in range(cols)] for _ in range(rows)])

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.data), len(self.data[0]) if self.data else 0

    def __getitem__(self, key: tuple[int, int]) -> float:
        i, j = key
        return self.data[i][j]

    def __setitem__(self, key: tuple[int, int], value: float) -> None:
        i, j = key
        self.data[i][j] = float(value)

    def transpose(self) -> "DenseMatrix":
        r, c = self.shape
        out = DenseMatrix.zeros(c, r)
        for i in range(r):
            for j in range(c):
                out[j, i] = self[i, j]
        return out

    def matmul(self, other: "DenseMatrix") -> "DenseMatrix":
        r1, c1 = self.shape
        r2, c2 = other.shape
        if c1 != r2:
            raise ValueError("Matrix dimensions incompatible")
        out = DenseMatrix.zeros(r1, c2)
        for i in range(r1):
            for k in range(c1):
                aik = self[i, k]
                if aik == 0.0:
                    continue
                for j in range(c2):
                    out[i, j] += aik * other[k, j]
        return out

    def mul_vector(self, vec: Vector) -> Vector:
        rows, cols = self.shape
        if cols != len(vec):
            raise ValueError("Matrix-vector dimensions incompatible")
        out = Vector.zeros(rows)
        for i in range(rows):
            out[i] = sum(self[i, j] * vec[j] for j in range(cols))
        return out

"""banded.py
Purpose: Symmetric banded matrix storage and LDL^T solver.
Assumptions: Matrix is symmetric positive definite.
Units: Unit-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass

from matrixlib.vector import Vector


@dataclass
class SymmetricBandedMatrix:
    """Store lower triangle of a symmetric banded matrix.

    Attributes:
        n: matrix size
        half_bandwidth: number of diagonals in lower storage (>=1)
        rows[i]: values for columns max(0, i-half_bandwidth+1) .. i
    """

    n: int
    half_bandwidth: int
    rows: list[list[float]]

    @classmethod
    def create(cls, n: int, half_bandwidth: int) -> "SymmetricBandedMatrix":
        if half_bandwidth < 1:
            raise ValueError("half_bandwidth must be at least 1")
        rows: list[list[float]] = []
        for i in range(n):
            width = min(half_bandwidth, i + 1)
            rows.append([0.0] * width)
        return cls(n=n, half_bandwidth=half_bandwidth, rows=rows)

    def _lower_col_start(self, i: int) -> int:
        return max(0, i - self.half_bandwidth + 1)

    def _has(self, i: int, j: int) -> bool:
        if i < j:
            i, j = j, i
        return j >= self._lower_col_start(i)

    def add(self, i: int, j: int, value: float) -> None:
        if i < j:
            i, j = j, i
        if not self._has(i, j):
            raise IndexError("Entry outside band")
        self.rows[i][j - self._lower_col_start(i)] += value

    def get(self, i: int, j: int) -> float:
        if i < j:
            i, j = j, i
        if not self._has(i, j):
            return 0.0
        return self.rows[i][j - self._lower_col_start(i)]

    def to_dense(self) -> list[list[float]]:
        out = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            j0 = self._lower_col_start(i)
            for j in range(j0, i + 1):
                v = self.get(i, j)
                out[i][j] = v
                out[j][i] = v
        return out


class BandedLDLTSolver:
    """LDL^T solver for symmetric banded matrices."""

    @staticmethod
    def factorize(a: SymmetricBandedMatrix) -> tuple[list[list[float]], list[float]]:
        n = a.n
        hb = a.half_bandwidth
        l = [[0.0] * min(hb - 1, i) for i in range(n)]
        d = [0.0] * n

        for i in range(n):
            k_start_i = max(0, i - hb + 1)

            for j in range(k_start_i, i):
                sum_ij = a.get(i, j)
                k_start_j = max(0, j - hb + 1)
                k0 = max(k_start_i, k_start_j)
                for k in range(k0, j):
                    li_k = l[i][k - k_start_i]
                    lj_k = l[j][k - k_start_j]
                    sum_ij -= li_k * d[k] * lj_k
                l[i][j - k_start_i] = sum_ij / d[j]

            sum_ii = a.get(i, i)
            for k in range(k_start_i, i):
                lik = l[i][k - k_start_i]
                sum_ii -= lik * lik * d[k]
            d[i] = sum_ii
            if d[i] == 0.0:
                raise ZeroDivisionError("Zero pivot in banded LDL^T factorization")

        return l, d

    @staticmethod
    def solve(a: SymmetricBandedMatrix, b: Vector) -> Vector:
        if len(b) != a.n:
            raise ValueError("Dimension mismatch")

        n = a.n
        hb = a.half_bandwidth
        l, d = BandedLDLTSolver.factorize(a)

        y = [0.0] * n
        for i in range(n):
            k_start_i = max(0, i - hb + 1)
            yi = b[i]
            for k in range(k_start_i, i):
                yi -= l[i][k - k_start_i] * y[k]
            y[i] = yi

        z = [y[i] / d[i] for i in range(n)]

        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            xi = z[i]
            j_max = min(n - 1, i + hb - 1)
            for j in range(i + 1, j_max + 1):
                k_start_j = max(0, j - hb + 1)
                if i >= k_start_j:
                    xi -= l[j][i - k_start_j] * x[j]
            x[i] = xi

        return Vector.from_iterable(x)

"""skyline.py
Purpose: Symmetric skyline matrix storage and LDL^T solver.
Assumptions: Matrix is symmetric positive definite for stable solve.
Units: Unit-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass

from matrixlib.vector import Vector


@dataclass
class SkylineMatrix:
    """Symmetric skyline matrix.

    Storage:
      - `profile[i]`: first (smallest) column index stored in row i.
      - `rows[i]`: values from column profile[i]..i (lower triangle row slice).
    """

    n: int
    profile: list[int]
    rows: list[list[float]]

    @classmethod
    def from_profile(cls, n: int, profile: list[int]) -> "SkylineMatrix":
        rows = [[0.0] * (i - profile[i] + 1) for i in range(n)]
        return cls(n=n, profile=profile[:], rows=rows)

    @classmethod
    def full(cls, n: int) -> "SkylineMatrix":
        return cls.from_profile(n, [0 for _ in range(n)])

    def _has(self, i: int, j: int) -> bool:
        if i < j:
            i, j = j, i
        return j >= self.profile[i]

    def get(self, i: int, j: int) -> float:
        if i < j:
            i, j = j, i
        if not self._has(i, j):
            return 0.0
        return self.rows[i][j - self.profile[i]]

    def add(self, i: int, j: int, value: float) -> None:
        if i < j:
            i, j = j, i
        if not self._has(i, j):
            raise IndexError("Entry outside skyline profile")
        self.rows[i][j - self.profile[i]] += value

    def to_dense(self) -> list[list[float]]:
        out = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.profile[i], i + 1):
                val = self.get(i, j)
                out[i][j] = val
                out[j][i] = val
        return out


class SkylineLDLTSolver:
    """In-place LDL^T factorization and solve for SkylineMatrix."""

    @staticmethod
    def factorize(a: SkylineMatrix) -> tuple[list[list[float]], list[float], list[int]]:
        n = a.n
        profile = a.profile
        l = [[0.0] * (i - profile[i]) for i in range(n)]
        d = [0.0] * n

        for i in range(n):
            start_i = profile[i]
            for j in range(start_i, i):
                sum_ij = a.get(i, j)
                start_j = profile[j]
                k0 = max(start_i, start_j)
                for k in range(k0, j):
                    sum_ij -= l[i][k - start_i] * d[k] * l[j][k - start_j]
                l[i][j - start_i] = sum_ij / d[j]

            sum_ii = a.get(i, i)
            for k in range(start_i, i):
                lik = l[i][k - start_i]
                sum_ii -= lik * lik * d[k]
            d[i] = sum_ii
            if d[i] == 0.0:
                raise ZeroDivisionError("Zero pivot encountered in LDL^T")

        return l, d, profile

    @staticmethod
    def solve(a: SkylineMatrix, b: Vector) -> Vector:
        if len(b) != a.n:
            raise ValueError("Dimension mismatch")

        l, d, profile = SkylineLDLTSolver.factorize(a)
        n = a.n

        y = [0.0] * n
        for i in range(n):
            yi = b[i]
            start_i = profile[i]
            for k in range(start_i, i):
                yi -= l[i][k - start_i] * y[k]
            y[i] = yi

        z = [y[i] / d[i] for i in range(n)]

        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            xi = z[i]
            for j in range(i + 1, n):
                if i >= profile[j]:
                    xi -= l[j][i - profile[j]] * x[j]
            x[i] = xi

        return Vector.from_iterable(x)

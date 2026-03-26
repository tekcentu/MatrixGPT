"""solver.py
Purpose: Solve K*D=F using symmetric banded LDL^T routine.
"""

from matrixlib.banded import BandedLDLTSolver, SymmetricBandedMatrix
from matrixlib.vector import Vector


def solve_displacements(k: SymmetricBandedMatrix, f: Vector) -> Vector:
    return BandedLDLTSolver.solve(k, f)

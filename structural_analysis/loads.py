"""loads.py
Purpose: Assemble reduced load vector F.
Inputs: nodal loads and equation numbering E.
Outputs: Vector F (size = number of active equations).
"""

from matrixlib.vector import Vector
from structural_analysis.model import NodalLoad


def assemble_load_vector(loads: list[NodalLoad], e_numbering: dict[int, list[int]], num_eq: int) -> Vector:
    f = Vector.zeros(num_eq)
    for load in loads:
        eqs = e_numbering[load.node_id]
        values = [load.fx, load.fy, load.mz]
        for dof in range(3):
            q = eqs[dof]
            if q != 0:
                f[q - 1] += values[dof]
    return f

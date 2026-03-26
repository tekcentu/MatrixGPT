"""postprocess.py
Purpose: Recover element local end forces.
Inputs: solved displacement vector D, G mapping, element cache.
Outputs: per-element local force vectors.
"""

from matrixlib.vector import Vector


def member_end_forces(
    d: Vector,
    g_map: dict[int, list[int]],
    element_cache: dict[int, tuple],
) -> dict[int, Vector]:
    forces = {}
    for mid, g in g_map.items():
        k_local, r, _k_global, _length, _c, _s = element_cache[mid]
        d_global = Vector.zeros(6)
        for p in range(6):
            gp = g[p]
            if gp > 0:
                d_global[p] = d[gp - 1]

        d_local = r.mul_vector(d_global)
        f_local = k_local.mul_vector(d_local)
        forces[mid] = f_local
    return forces

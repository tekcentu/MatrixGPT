"""assembly.py
Purpose: Assemble global stiffness matrix using banded symmetric storage.
Inputs: members, E numbering, element matrices.
Outputs: SymmetricBandedMatrix K.
"""

from matrixlib.banded import SymmetricBandedMatrix
from structural_analysis.element import element_matrices
from structural_analysis.model import Material, Member, Node
from structural_analysis.numbering import member_g_vector


def compute_half_bandwidth(gs: list[list[int]]) -> int:
    """Return half-bandwidth from element DOF maps.

    half_bandwidth = max(|i-j|)+1 over active equation pairs.
    """

    hb = 1
    for g in gs:
        active = [eq - 1 for eq in g if eq > 0]
        for i in active:
            for j in active:
                dist = abs(i - j) + 1
                if dist > hb:
                    hb = dist
    return hb


def assemble_global_stiffness(
    members: dict[int, Member],
    nodes: dict[int, Node],
    materials: dict[int, Material],
    e_numbering: dict[int, list[int]],
    num_eq: int,
) -> tuple[SymmetricBandedMatrix, dict[int, list[int]], dict[int, tuple]]:
    g_map: dict[int, list[int]] = {}
    element_cache: dict[int, tuple] = {}

    for mid, member in members.items():
        g_map[mid] = member_g_vector(member, e_numbering)

    half_bandwidth = compute_half_bandwidth(list(g_map.values()))
    k_global = SymmetricBandedMatrix.create(num_eq, half_bandwidth)

    for mid, member in members.items():
        mat = materials[member.material_id]
        k_local, r, k_elem, length, c, s = element_matrices(member, nodes, mat)
        element_cache[mid] = (k_local, r, k_elem, length, c, s)
        g = g_map[mid]

        for p in range(6):
            gp = g[p]
            if gp == 0:
                continue
            for q in range(6):
                gq = g[q]
                if gq == 0:
                    continue
                k_global.add(gp - 1, gq - 1, k_elem[p, q])

    return k_global, g_map, element_cache

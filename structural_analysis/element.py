"""element.py
Purpose: Build local/global stiffness matrices for 2D frame elements.
Inputs: node coordinates and material properties.
Outputs: k_local, rotation matrix R, and k_global (all 6x6).
Assumptions: Euler-Bernoulli beam-column, small displacements.
Units: Consistent units required.
"""

from math import sqrt

from matrixlib.dense import DenseMatrix
from structural_analysis.model import Material, Member, Node


def element_matrices(member: Member, nodes: dict[int, Node], material: Material) -> tuple[DenseMatrix, DenseMatrix, DenseMatrix, float, float, float]:
    ni = nodes[member.start_node]
    nj = nodes[member.end_node]

    dx = nj.x - ni.x
    dy = nj.y - ni.y
    length = sqrt(dx * dx + dy * dy)
    c = dx / length
    s = dy / length

    e = material.elastic_modulus
    a = material.area
    i = material.inertia

    ae_l = e * a / length
    ei = e * i
    k1 = 12.0 * ei / (length**3)
    k2 = 6.0 * ei / (length**2)
    k3 = 4.0 * ei / length
    k4 = 2.0 * ei / length

    k_local = DenseMatrix.zeros(6, 6)
    local = [
        [ae_l, 0, 0, -ae_l, 0, 0],
        [0, k1, k2, 0, -k1, k2],
        [0, k2, k3, 0, -k2, k4],
        [-ae_l, 0, 0, ae_l, 0, 0],
        [0, -k1, -k2, 0, k1, -k2],
        [0, k2, k4, 0, -k2, k3],
    ]
    for r in range(6):
        for col in range(6):
            k_local[r, col] = local[r][col]

    r = DenseMatrix.zeros(6, 6)
    transform = [
        [c, s, 0, 0, 0, 0],
        [-s, c, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, c, s, 0],
        [0, 0, 0, -s, c, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    for rr in range(6):
        for cc in range(6):
            r[rr, cc] = transform[rr][cc]

    k_global = r.transpose().matmul(k_local).matmul(r)
    return k_local, r, k_global, length, c, s

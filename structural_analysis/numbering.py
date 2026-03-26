"""numbering.py
Purpose: Build equation numbering matrix E and element mapping vectors G.
Inputs: node IDs and support list.
Outputs: E matrix and helpers.
"""

from structural_analysis.model import Member, Support


def build_equation_numbering(node_ids: list[int], supports: list[Support]) -> tuple[dict[int, list[int]], int]:
    restraint = {node_id: [0, 0, 0] for node_id in node_ids}
    for s in supports:
        restraint[s.node_id] = [s.tx, s.ty, s.rz]

    e = {node_id: [0, 0, 0] for node_id in node_ids}
    eq = 1
    for node_id in node_ids:
        for dof in range(3):
            if restraint[node_id][dof] == 0:
                e[node_id][dof] = eq
                eq += 1
            else:
                e[node_id][dof] = 0

    return e, eq - 1


def member_g_vector(member: Member, e: dict[int, list[int]]) -> list[int]:
    i = e[member.start_node]
    j = e[member.end_node]
    return [i[0], i[1], i[2], j[0], j[1], j[2]]

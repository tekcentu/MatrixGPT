"""run_analysis.py
Purpose: End-to-end 2D frame analysis driver.
"""

from __future__ import annotations

import json
import sys

from structural_analysis.assembly import assemble_global_stiffness
from structural_analysis.loads import assemble_load_vector
from structural_analysis.numbering import build_equation_numbering
from structural_analysis.parser import parse_input
from structural_analysis.postprocess import member_end_forces
from structural_analysis.solver import solve_displacements


def run(input_file: str) -> dict:
    model = parse_input(input_file)
    node_ids = sorted(model["nodes"].keys())

    e, num_eq = build_equation_numbering(node_ids, model["supports"])
    k, g_map, cache = assemble_global_stiffness(
        model["members"], model["nodes"], model["materials"], e, num_eq
    )
    f = assemble_load_vector(model["loads"], e, num_eq)
    d = solve_displacements(k, f)
    forces = member_end_forces(d, g_map, cache)

    return {
        "num_eq": num_eq,
        "E": e,
        "G": g_map,
        "K_dense": k.to_dense(),
        "F": f.values,
        "D": d.values,
        "member_end_forces_local": {mid: vec.values for mid, vec in forces.items()},
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m structural_analysis.run_analysis <input.json>")

    result = run(sys.argv[1])
    print(json.dumps(result, indent=2))

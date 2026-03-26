"""parser.py
Purpose: Parse structural model input JSON.
Inputs: file path.
Outputs: dictionaries of model entities keyed by ID.
Assumptions: JSON schema follows docs/report.md.
"""

import json
from pathlib import Path

from structural_analysis.model import Material, Member, NodalLoad, Node, Support


def parse_input(input_path: str) -> dict:
    data = json.loads(Path(input_path).read_text())

    nodes = {n["node_id"]: Node(**n) for n in data["nodes"]}
    materials = {m["material_id"]: Material(**m) for m in data["materials"]}
    members = {c["member_id"]: Member(**c) for c in data["members"]}
    supports = [Support(**s) for s in data["supports"]]
    loads = [NodalLoad(**l) for l in data["loads"]]

    return {
        "nodes": nodes,
        "materials": materials,
        "members": members,
        "supports": supports,
        "loads": loads,
    }

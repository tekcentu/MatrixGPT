"""model.py
Purpose: Domain models for 2D frame analysis input.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    node_id: int
    x: float
    y: float


@dataclass(frozen=True)
class Material:
    material_id: int
    area: float
    inertia: float
    elastic_modulus: float


@dataclass(frozen=True)
class Member:
    member_id: int
    start_node: int
    end_node: int
    material_id: int


@dataclass(frozen=True)
class Support:
    support_id: int
    node_id: int
    tx: int
    ty: int
    rz: int


@dataclass(frozen=True)
class NodalLoad:
    load_id: int
    node_id: int
    fx: float
    fy: float
    mz: float

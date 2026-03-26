from matrixlib.banded import BandedLDLTSolver, SymmetricBandedMatrix
from matrixlib.vector import Vector
from structural_analysis.assembly import compute_half_bandwidth
from structural_analysis.element import element_matrices
from structural_analysis.model import Material, Member, Node
from structural_analysis.run_analysis import run


def test_banded_solver_small_system() -> None:
    # [4 1; 1 3] x = [1; 2] -> x = [1/11, 7/11]
    a = SymmetricBandedMatrix.create(2, 2)
    a.add(0, 0, 4.0)
    a.add(1, 0, 1.0)
    a.add(1, 1, 3.0)
    b = Vector.from_iterable([1.0, 2.0])
    x = BandedLDLTSolver.solve(a, b)
    assert abs(x[0] - (1.0 / 11.0)) < 1e-10
    assert abs(x[1] - (7.0 / 11.0)) < 1e-10


def test_half_bandwidth_from_g_vectors() -> None:
    gs = [
        [1, 2, 3, 4, 5, 6],
        [0, 0, 7, 8, 9, 10],
    ]
    assert compute_half_bandwidth(gs) == 6


def test_element_stiffness_is_symmetric() -> None:
    nodes = {1: Node(1, 0.0, 0.0), 2: Node(2, 4.0, 0.0)}
    mat = Material(1, 0.02, 0.0001, 210e9)
    m = Member(1, 1, 2, 1)
    _kl, _r, kg, _l, _c, _s = element_matrices(m, nodes, mat)
    for i in range(6):
        for j in range(6):
            assert abs(kg[i, j] - kg[j, i]) < 1e-6


def test_full_run_produces_shapes() -> None:
    result = run("examples/two_element_frame.json")
    assert result["num_eq"] == 6
    assert len(result["F"]) == 6
    assert len(result["D"]) == 6
    assert 1 in result["member_end_forces_local"]
    assert 2 in result["member_end_forces_local"]

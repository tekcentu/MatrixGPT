# Q1 & Q2 Report: Object-Oriented Matrix Library + Structural Analysis Program

## Q1) Matrix Library Design and Development

## 1. Analysis and Design Decisions

- **No external numeric libraries**: all operations are implemented using pure Python.
- **Two-level matrix strategy**:
  - `DenseMatrix` for small fixed-size element computations (6x6 transforms/stiffness).
  - `SymmetricBandedMatrix` for global structural stiffness where symmetry and profile can be exploited.
- **Symmetry usage**:
  - Only lower-triangular banded terms are stored inside the active half-bandwidth.
  - Memory reduction vs full dense matrix is significant for large sparse-like frames.
- **Linear solution scheme**:
  - Implemented **banded LDL^T** direct solver (`BandedLDLTSolver`).
  - This satisfies the requirement of implementing at least one of banded/skyline/sparse schemes (banded implemented here).

## 2. Matrix Library Components

- `Vector`: dense vector utility for load/displacement vectors.
- `DenseMatrix`: transpose, matrix-matrix multiply, matrix-vector multiply.
- `SymmetricBandedMatrix`:
  - Band storage keeps only entries within the computed half-bandwidth around the diagonal.
  - `add(i,j,v)` and `get(i,j)` respect symmetry.
- `BandedLDLTSolver`:
  - Performs LDL^T factorization considering half-bandwidth.
  - Solves via forward substitution, diagonal solve, backward substitution.

## 3. UML Class Diagram

See `docs/uml.md` for a Mermaid diagram.

---

## Q2) Structural Analysis Program Using Custom Matrix Library

## 1. Program Structure and Modularity

Each source file handles one task:

- `parser.py`: JSON input parsing.
- `numbering.py`: equation numbering matrix `E` and element mapping vector `G`.
- `element.py`: local stiffness, transformation, global element stiffness.
- `assembly.py`: half-bandwidth generation and global stiffness assembly.
- `loads.py`: reduced load vector assembly.
- `solver.py`: solve `K·D=F` using banded LDL^T.
- `postprocess.py`: recover local member end forces.
- `run_analysis.py`: orchestration of all steps.

## 2. Naming Convention

- Structural-analysis conventions are used for computational variables:
  - `k` stiffness, `f` force, `d` displacement, `e` equation numbering, `g` DOF map.
- Entity classes use explicit names (`Node`, `Material`, `Member`, `Support`, `NodalLoad`).

## 3. Subroutine Information Sections

Every module has a header section indicating purpose/inputs/outputs/assumptions/units where applicable.

## 4. Input Format

JSON with explicit IDs:

- `nodes`: `node_id`, `x`, `y`
- `materials`: `material_id`, `area`, `inertia`, `elastic_modulus`
- `members`: `member_id`, `start_node`, `end_node`, `material_id`
- `supports`: `support_id`, `node_id`, `tx`, `ty`, `rz` (1=restrained, 0=free)
- `loads`: `load_id`, `node_id`, `fx`, `fy`, `mz`

Example file: `examples/two_element_frame.json`.

## 5. Output Format

The driver prints JSON including:

- `num_eq`
- `E` equation numbering matrix (node-based dictionary)
- `G` vector for each member
- `K_dense` (dense visualization of global banded stiffness)
- `F` reduced load vector
- `D` solved active DOF displacements
- `member_end_forces_local`

## 6. Main Algorithm Steps

1. Parse input entities.
2. Build equation numbering `E` (`0` restrained, positive numbers active DOFs).
3. Build element `G` maps.
4. Compute each element `k_local`, `R`, `k_global`.
5. Assemble global banded stiffness `K`.
6. Assemble reduced load vector `F`.
7. Solve `K·D=F` with banded LDL^T.
8. Recover local element end forces using `d_local = R·d_global`, `f_local = k_local·d_local`.

## 7. Verification Results

### 7.1 Matrix solver verification (hand-checkable)

Test system:

\[
\begin{bmatrix}4 & 1\\1 & 3\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}=
\begin{bmatrix}1\\2\end{bmatrix}
\]

Exact solution: `x1=1/11`, `x2=7/11`.

Automated test confirms the banded solver reproduces this result.

### 7.2 Element matrix verification

Automated test verifies `k_global` symmetry (`k_ij = k_ji`) for a sample frame element.

### 7.3 End-to-end verification

Automated test confirms:
- Correct reduced equation count
- Consistent dimensions for `F` and `D`
- Member force recovery exists for each member

These checks validate key steps: element stiffness generation, assembly/numbering consistency, and global solution/recovery workflow.

## 8. Notes on Commercial/Hand Comparison

This submission includes reproducible hand-checkable matrix-solver verification and structural-step consistency checks. For classroom extension, the same example can be mirrored in a commercial package (SAP2000/ETABS/STAAD) and compared DOF-by-DOF for `D` and element end forces.

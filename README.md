# MatrixGPT - 2D Frame Structural Analysis (No NumPy)

This repository provides:
1. An object-oriented matrix library with a **symmetric banded storage and LDL^T solver**.
2. A modular 2D frame direct-stiffness solver that uses the custom matrix library for all matrix operations.

## Run

```bash
python -m structural_analysis.run_analysis examples/two_element_frame.json
```

## Test

```bash
python -m pytest -q
```

## Folder Structure

- `matrixlib/`: custom vector/matrix/banded classes.
- `structural_analysis/`: parser, numbering, element, assembly, loads, solver, postprocess, driver.
- `examples/`: JSON input sample.
- `tests/`: verification checks.
- `docs/`: UML and design report.

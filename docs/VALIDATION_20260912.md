# Validation record — 2026-09-12

Scope: `geometry_guard.py`, the callable same-grid copy path in
`simple_reorient.py`, and synthetic tests only. No weights, datasets, model
inference, or patient data were accessed.

Environment: Python 3.14.2 via `py -3 -B`; isolated dependency directory
`C:\Users\88692\.codex\visualizations\2026\09\07\01a07a41-fff5-72a0-8852-06efcbfafebb\workflow-test-deps-20260912`; nibabel 5.4.2; numpy 2.5.3; pytest 9.1.1.

Observed commands and results:

```powershell
$env:PYTHONPATH='C:\Users\88692\.codex\visualizations\2026\09\07\01a07a41-fff5-72a0-8852-06efcbfafebb\workflow-test-deps-20260912'; py -3 -B -c "import pytest; raise SystemExit(pytest.main(['-p','no:cacheprovider','tests_local/test_geometry_guard.py','tests_local/test_image_io.py']))"
# 10 passed in 0.27s

$env:PYTHONPATH='C:\Users\88692\.codex\visualizations\2026\09\07\01a07a41-fff5-72a0-8852-06efcbfafebb\workflow-test-deps-20260912'; py -3 -B -m unittest discover -s tests_local -v
# 10 tests, OK
```

The required module command was also run:

```powershell
$env:PYTHONPATH='C:\Users\88692\.codex\visualizations\2026\09\07\01a07a41-fff5-72a0-8852-06efcbfafebb\workflow-test-deps-20260912'; py -3 -B -m pytest -p no:cacheprovider tests_local/test_geometry_guard.py tests_local/test_image_io.py
# 10 passed in 0.28s
```

The first non-elevated attempt could not read the isolated dependency directory;
the commands above were then rerun with elevated access and passed. The direct
unittest command also passed after replacing non-ASCII progress output that
failed under the Windows cp950 console.

Guard limits: comparison is of finite numeric 4×4 image affines and matching
3D shapes. These tests do not establish qform/sform code consistency, orientation
conventions, registration correctness, voxel-spacing policy beyond the affine
comparison, dataset integrity, model performance, or clinical safety. Any
registration/resampling remains an explicit, separately validated workflow.

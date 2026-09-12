"""Conservative same-grid guard. This is not registration or reorientation."""
from math import isclose, isfinite


def _validated_affine(affine):
    """Return a finite numeric 4x4 affine or raise a stable ValueError."""
    try:
        matrix = tuple(tuple(float(value) for value in row) for row in affine)
    except (TypeError, ValueError, OverflowError):
        raise ValueError('Expected a numeric 4x4 affine') from None

    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise ValueError('Expected a 4x4 affine')
    if not all(isfinite(value) for row in matrix for value in row):
        raise ValueError('Non-finite geometry')
    if not all(isclose(value, expected, abs_tol=1e-8, rel_tol=0)
               for value, expected in zip(matrix[3], (0, 0, 0, 1))):
        raise ValueError('Invalid homogeneous affine row')

    a = matrix
    determinant = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                   - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                   + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    if abs(determinant) < 1e-12:
        raise ValueError('Singular spatial affine')
    return matrix


def require_same_grid(source_shape, source_affine, target_shape, target_affine):
    source_shape = tuple(source_shape)
    target_shape = tuple(target_shape)
    if source_shape != target_shape or len(source_shape) != 3:
        raise ValueError('Only matching 3D image shapes are supported')
    source_affine = _validated_affine(source_affine)
    target_affine = _validated_affine(target_affine)
    if not all(isclose(float(x), float(y), abs_tol=1e-5, rel_tol=0)
               for sr, tr in zip(source_affine, target_affine) for x, y in zip(sr, tr)):
        raise ValueError('Different grids: registration/resampling must be explicit; header replacement refused')

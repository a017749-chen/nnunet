import copy
import unittest
from geometry_guard import require_same_grid


class GeometryTests(unittest.TestCase):
    def affine(self):
        return [[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]]

    def test_matching_grid(self):
        a = self.affine(); require_same_grid((5,6,7), a, (5,6,7), a)

    def test_shape_mismatch(self):
        with self.assertRaises(ValueError): require_same_grid((5,6,7), self.affine(), (5,6,8), self.affine())

    def test_translation_refused(self):
        a = self.affine(); b = copy.deepcopy(a); b[0][3] = 10
        with self.assertRaises(ValueError): require_same_grid((5,6,7), a, (5,6,7), b)

    def test_flip_refused(self):
        a = self.affine(); b = copy.deepcopy(a); b[0][0] = -1
        with self.assertRaises(ValueError): require_same_grid((5,6,7), a, (5,6,7), b)

    def test_nonfinite_refused(self):
        a = self.affine(); a[0][0] = float('nan')
        with self.assertRaises(ValueError): require_same_grid((5,6,7), a, (5,6,7), a)

    def test_nonnumeric_affine_refused(self):
        a = self.affine(); a[0][0] = 'not-a-number'
        with self.assertRaises(ValueError): require_same_grid((5,6,7), a, (5,6,7), a)

    def test_singular_refused(self):
        a = self.affine(); a[0][0] = 0
        with self.assertRaises(ValueError): require_same_grid((5,6,7), a, (5,6,7), a)

import tempfile
import unittest
from pathlib import Path
import nibabel as nib
import numpy as np
from simple_reorient import copy_geometry


class ImageIOTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='synthetic-nifti-')
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.source, self.target, self.output = (root / n for n in ('source.nii.gz','target.nii.gz','output.nii.gz'))
        self.data = np.arange(60, dtype=np.int16).reshape(3,4,5)
        nib.save(nib.Nifti1Image(self.data, np.eye(4)), self.source)
        nib.save(nib.Nifti1Image(self.data, np.eye(4)), self.target)

    def test_roundtrip_preserves_values_dtype_and_affine(self):
        copy_geometry(self.source, self.target, self.output)
        image = nib.load(self.output)
        np.testing.assert_array_equal(np.asanyarray(image.dataobj), self.data)
        np.testing.assert_array_equal(image.affine, np.eye(4))
        self.assertEqual(image.get_data_dtype(), np.dtype('int16'))

    def test_mismatch_has_no_output(self):
        affine = np.eye(4); affine[0,3] = 20
        nib.save(nib.Nifti1Image(self.data, affine), self.target)
        with self.assertRaises(ValueError): copy_geometry(self.source, self.target, self.output)
        self.assertFalse(self.output.exists())

    def test_output_and_input_cannot_be_overwritten(self):
        source_original = self.source.read_bytes()
        with self.assertRaises(FileExistsError): copy_geometry(self.source, self.target, self.source)
        self.assertEqual(self.source.read_bytes(), source_original)

        self.output.write_bytes(b'existing synthetic output')
        output_original = self.output.read_bytes()
        with self.assertRaises(FileExistsError): copy_geometry(self.source, self.target, self.output)
        self.assertEqual(self.output.read_bytes(), output_original)

"""
Testing the utils modules.
"""
from __future__ import absolute_import, print_function
import os
import unittest
import tempfile
import shutil

from tellurium.tests.testdata import OMEX_SHOWCASE
from tellurium.utils import omex


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_omex_extractCombineArchive1(self):
        omex.extractCombineArchive(omex_path=OMEX_SHOWCASE, directory=self.test_dir, method="zip")

    def test_omex_extractCombineArchive2(self):
        omex.extractCombineArchive(omex_path=OMEX_SHOWCASE, directory=self.test_dir, method="omex")


    def test_omex_extractCombineArchive3(self):
        tmp_dir = tempfile.mkdtemp()
        omex.extractCombineArchive(omex_path=OMEX_SHOWCASE, directory=self.test_dir, method="zip")
        files = [f for f in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir, f))]
        self.assertIsNotNone(files)
        shutil.rmtree(tmp_dir)

    def test_omex_extractCombineArchive4(self):
        tmp_dir = tempfile.mkdtemp()
        omex.extractCombineArchive(omex_path=OMEX_SHOWCASE, directory=self.test_dir, method="omex")
        files = [f for f in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir, f))]
        self.assertIsNotNone(files)
        shutil.rmtree(tmp_dir)

    def test_getLocationsByFormat1(self):
        locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sed-ml")
        self.assertEqual(len(locations), 2)

    def test_getLocationsByFormat2(self):
        locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sbml")
        self.assertEqual(len(locations), 1)

    def test_getLocationsByFormat3(self):
        locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="cellml")
        self.assertEqual(len(locations), 1)


if __name__ == "__main__":
    unittest.main()

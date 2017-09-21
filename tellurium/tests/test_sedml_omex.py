"""
Test that Combine archives can be executed successfully.

    test_sedml_phrasedml.py : phrasedml based tests.
    test_sedml_kisao.py : SED-ML kisao support
    test_sedml_omex.py : SED-ML tests based on Combine Archives
    test_sedml_sedml.py : sed-ml tests
"""

from __future__ import absolute_import, print_function
import os
import unittest
import tempfile
import shutil

from tellurium.tests.testdata import OMEX_SHOWCASE
from tellurium.sedml import tesedml


class OmexSedmlTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_omex_extractCombineArchive3(self):
        tesedml.executeCombineArchive(omexPath=OMEX_SHOWCASE, workingDir=self.test_dir)


# TODO: implement the omex based tests, i.e. for full set of archives

if __name__ == "__main__":
    unittest.main()

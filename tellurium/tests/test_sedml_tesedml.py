
from __future__ import absolute_import, print_function
import os
import unittest
import tempfile
import shutil
from tellurium.sedml import tesedml
import matplotlib
from . import helpers

# -------------------------------------------------------------
# Combine Archive test files
# -------------------------------------------------------------
from tellurium.tests.testdata import OMEX_SHOWCASE


class OmexSedmlTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.backend = matplotlib.rcParams['backend']
        matplotlib.pyplot.switch_backend("Agg")

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
        matplotlib.pyplot.switch_backend(self.backend)
        matplotlib.pyplot.close('all')

    def test_omex_executeCombineArchive(self):
        tesedml.executeCombineArchive(omexPath=OMEX_SHOWCASE, workingDir=self.test_dir)

    def test_omex_combineArchiveToPython(self):
        pycode = tesedml.combineArchiveToPython(omexPath=OMEX_SHOWCASE)
        assert pycode is not None
        assert len(pycode) == 2


if __name__ == "__main__":
    unittest.main()

"""
Test that Combine archives can be executed successfully.
"""

from __future__ import absolute_import, print_function
import os
import unittest
import tempfile
import shutil
from tellurium.sedml import tesedml
import matplotlib
from tellurium.tests import helpers


# -------------------------------------------------------------
# Combine Archive test files
# -------------------------------------------------------------
from tellurium.tests.testdata import OMEX_TEST_DIR

def f_omex_filter(filename):
    return filename.endswith(".omex") or filename.endswith(".sedx")

OMEX_TESTCASES = helpers.filesInDirectoryFiltered(OMEX_TEST_DIR, f_filter=f_omex_filter)


# -------------------------------------------------------------
# Excluded combine archives
# -------------------------------------------------------------
# This are the archives failing due to
#  - bugs in the archives
#  - unsupported features (like cellml)
#  - tellurium bugs
OMEX_EXCLUDED = [
    # cellml models not supported: https://github.com/matthiaskoenig/tellurium-web/issues/62
    os.path.join(OMEX_TEST_DIR, 'specification', 'L1V3', 'L1V3_lorenz-cellml.omex'),
    os.path.join(OMEX_TEST_DIR, 'specification', 'L1V3', 'L1V3_vanderpol-cellml.omex'),
    os.path.join(OMEX_TEST_DIR, 'cellml', 'lorenz-cellml.omex'),

    # non-standard data implementation: FIXME: https:/github.com/matthiaskoenig/tellurium-web/issues/53
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'adlung2017_fig2g.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'adlung2017_fig2bto2e.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'adlung2017_fig2f.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'bachmann2011.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'kouril3_experiment-user.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'penkler2aa_experiment-user.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'perelson1996_fig1b_top.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'stafford2000_fig2.sedx'),

    # complex xpath expressions: FIXME: https://github.com/matthiaskoenig/tellurium-web/issues/52, https://github.com/sys-bio/tellurium/issues/114
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'levering2012_fig5-user.sedx'),
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'levering2012_fig2-user.sedx'),

    # negative start time: FIXME: https://github.com/sys-bio/roadrunner/issues/411
    os.path.join(OMEX_TEST_DIR, 'jws', 'omex', 'martins2016_fig4b.sedx'),
]

# ----------------------------------------------------------------
# Dynamic generation of tests from python files
# ----------------------------------------------------------------
class OmexTestCase(unittest.TestCase):
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


def ftest_generator(filePath):
    def test(self=None):
        """ Test failes if Exception in execution of f. """
        if self is not None:
            print(filePath)
            tesedml.executeCombineArchive(omexPath=filePath, workingDir=self.test_dir)
    return test


for k, f in enumerate(OMEX_TESTCASES):
    if f in OMEX_EXCLUDED:
        continue
    test_name = 'test_{:03d}_{}'.format(k, os.path.basename(f))
    test_name = test_name.replace('.', '_')
    test = ftest_generator(f)
    setattr(OmexTestCase, test_name, test)


if __name__ == "__main__":
    print(OMEX_TESTCASES)
    unittest.main()

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
from tellurium.sedml import tesedml
from . import helpers

# -------------------------------------------------------------
# Combine Archive test files
# -------------------------------------------------------------
from tellurium.tests.testdata import OMEX_SHOWCASE, OMEX_TEST_DIR

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

    # unclear error: FIXME: https://github.com/matthiaskoenig/tellurium-web/issues/60
    'specification/L1V3/L1V3_repeated-scan-oscli.omex',
    'specification/L1V3/L1V3_oscli-nested-pulse.omex',

    # data not supported: FIXME: https://github.com/sys-bio/tellurium/issues/225
    'specification/L1V3/L1V3_plotting-data.omex',
    'specification/L1V3/L1V3_reading-data-numl.omex',
    'specification/L1V3/L1V3_reading-data-csv.omex',

    # non-standard data implementation: FIXME: https://github.com/matthiaskoenig/tellurium-web/issues/53
    'jws/omex/adlung2017_fig2g.sedx',
    'jws/omex/adlung2017_fig2bto2e.sedx',
    'jws/omex/adlung2017_fig2f.sedx',
    'jws/omex/bachmann2011.sedx',
    'jws/omex/kouril3_experiment-user.sedx',
    'jws/omex/penkler2aa_experiment-user.sedx',
    'jws/omex/perelson1996_fig1b_top.sedx',
    'jws/omex/stafford2000_fig2.sedx',

    # complex xpath expressions: FIXME: https://github.com/matthiaskoenig/tellurium-web/issues/52, https://github.com/sys-bio/tellurium/issues/114
    'jws/omex/levering2012_fig5-user.sedx',
    'jws/omex/levering2012_fig2-user.sedx',

    # negative start time: FIXME: https://github.com/sys-bio/roadrunner/issues/411
    'jws/omex/martins2016_fig4b.sedx',

    # cellml models not supported: https://github.com/matthiaskoenig/tellurium-web/issues/62
    'specification/L1V3/L1V3_lorenz-cellml.omex',
    'cellml/lorenz-cellml.omex',

]
OMEX_EXCLUDED = [os.path.join(OMEX_TEST_DIR, p) for p in OMEX_EXCLUDED ]

# -------------------------------------------------------------


class OmexSedmlTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_omex_executeCombineArchive(self):
        tesedml.executeCombineArchive(omexPath=OMEX_SHOWCASE, workingDir=self.test_dir)


# ----------------------------------------------------------------
# Dynamic generation of tests from python files
# ----------------------------------------------------------------
class OmexTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)


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
    test_name = 'test_{:03d}_{}'.format(k, os.path.basename(f)[:-3])
    test_name = test_name.replace('.', '_')
    test = ftest_generator(f)
    setattr(OmexTestCase, test_name, test)


if __name__ == "__main__":
    print(OMEX_TESTCASES)
    unittest.main()

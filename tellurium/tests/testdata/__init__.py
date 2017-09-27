"""
Definition of test files and directories which can be used in the tests.
"""

from __future__ import absolute_import
import os

TESTDATA_DIR = os.path.dirname(os.path.realpath(__file__))
SEDML_TEST_DIR = os.path.join(TESTDATA_DIR, 'sedml', 'sed-ml')
OMEX_TEST_DIR = os.path.join(TESTDATA_DIR, 'sedml', 'omex')


OMEX_SHOWCASE = os.path.join(OMEX_TEST_DIR, "CombineArchiveShowCase.omex")
OMEX_REPRESSILATOR = os.path.join(OMEX_TEST_DIR, "tellurium/repressilator.omex")
FEEDBACK_SBML = os.path.join(TESTDATA_DIR, 'models/feedback.xml')

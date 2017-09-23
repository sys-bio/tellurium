"""
Test class to check issues with single archives.
"""

from __future__ import absolute_import, print_function
import os
import pytest
import unittest
import tempfile
import shutil
from tellurium.sedml import tesedml
import matplotlib
from . import helpers

from tellurium.tests.testdata import OMEX_TEST_DIR
from tellurium.utils import omex

# -------------------------------------------------------------
# Excluded combine archives
# -------------------------------------------------------------
# This are the archives failing due to
#  - bugs in the archives
#  - unsupported features (like cellml)
#  - tellurium bugs
OMEX_EXCLUDED = [

    # data not supported: FIXME: https://github.com/sys-bio/tellurium/issues/225
    'specification/L1V3/L1V3_plotting-data.omex',
    'specification/L1V3/L1V3_reading-data-numl.omex',
    'specification/L1V3/L1V3_reading-data-numl-simple.omex',
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

OMEX_RUN = [os.path.join(OMEX_TEST_DIR, p) for p in OMEX_EXCLUDED ]


def test_single_omex(tmpdir):


    omex_path = os.path.join(OMEX_TEST_DIR, 'specification/L1V3/L1V3_reading-data-numl-minimal.omex')
    omex_path = os.path.join(OMEX_TEST_DIR, 'specification/L1V3/L1V3_reading-data-csv-minimal.omex')
    contents = omex.listContents(omex_path)
    # print(contents[1])


    # TODO print generated code

    tesedml.executeCombineArchive(omexPath=omex_path, workingDir=tmpdir)



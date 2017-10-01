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

from tellurium.tests.testdata import OMEX_TEST_DIR
from tellurium.utils import omex

OMEX_EXCLUDED = [
    # data not supported: FIXME: https://github.com/sys-bio/tellurium/issues/225
    'specification/L1V3/L1V3_plotting-data.omex',
    'specification/L1V3/L1V3_reading-data-numl.omex',
    'specification/L1V3/L1V3_reading-data-numl-simple.omex',
    'specification/L1V3/L1V3_reading-data-csv.omex',

    # complex xpath expressions: FIXME: https://github.com/matthiaskoenig/tellurium-web/issues/52, https://github.com/sys-bio/tellurium/issues/114
    'jws/omex/levering2012_fig5-user.sedx',
    'jws/omex/levering2012_fig2-user.sedx',
]


@pytest.mark.skip
def test_single_omex(tmpdir):
    omex_path = os.path.join(OMEX_TEST_DIR, 'specification/L1V3/L1V3_reading-data-csv-minimal.omex')
    contents = omex.listContents(omex_path)
    # print(contents[1])

    # TODO print generated code
    tmp_dir = tempfile.mkdtemp()
    try:
        tesedml.executeCombineArchive(omexPath=omex_path, workingDir=tmp_dir)
    finally:
        shutil.rmtree(tmp_dir)



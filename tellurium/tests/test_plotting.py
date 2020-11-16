"""
Testing of the plotting engines.

Here we make sure the different plotting alternatives work.
"""
from __future__ import absolute_import, print_function
import os
import matplotlib
from tellurium.tests.testdata import OMEX_TEST_DIR
import tellurium as te

OMEX1 = os.path.join(OMEX_TEST_DIR, 'specification', 'L1V3', 'L1V3_plotting-data-numl.omex')

MPL_BACKEND = None


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    global MPL_BACKEND
    # Create a temporary directory
    MPL_BACKEND = matplotlib.rcParams['backend']
    matplotlib.pyplot.switch_backend("Agg")


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    matplotlib.pyplot.switch_backend(MPL_BACKEND)
    matplotlib.pyplot.close('all')
    te.setDefaultPlottingEngine("plotly")


def test_matplotlib1(tmpdir):
    te.setDefaultPlottingEngine("matplotlib")
    #dgs = te.executeCombineArchive(OMEX1, printPython=True, outputDir=str(tmpdir), saveOutputs=True)
    #assert dgs is not None


def test_plotly1(tmpdir):
    te.setDefaultPlottingEngine("plotly")
    #dgs = te.executeCombineArchive(OMEX1, printPython=True, outputDir=str(tmpdir), saveOutputs=True)
    #assert dgs is not None


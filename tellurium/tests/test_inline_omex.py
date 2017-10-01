"""
Tests for the inline omex functionality.
"""
from __future__ import absolute_import, print_function
import unittest
import pytest
import matplotlib

import tellurium as te
from tellurium.teconverters import inline_omex, convert_omex
from tellurium.tests.testdata import OMEX_REPRESSILATOR


class InlineOmexTestCase(unittest.TestCase):
    """ Testing execution and archives based on phrasedml input. """

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        self.backend = matplotlib.rcParams['backend']
        matplotlib.pyplot.switch_backend("Agg")

    def tearDown(self):
        matplotlib.pyplot.switch_backend(self.backend)
        matplotlib.pyplot.close('all')

    @pytest.mark.skip
    def test_repressilatorToInlineOmex(self):
        importer = convert_omex.inlineOmexImporter.fromFile(OMEX_REPRESSILATOR)
        assert importer is not None

        inline_omex = importer.toInlineOmex()
        assert inline_omex is not None
        print(inline_omex)
        te.executeInlineOmex(inline_omex)

if __name__ == "__main__":
    unittest.main()

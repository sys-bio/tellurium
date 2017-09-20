"""
Testing phrasedml.

    test_phrasedml.py : phrasedml based tests.
    test_kisao.py : SED-ML kisao support
    test_omex.py : SED-ML tests based on Combine Archives
    test_tesedml.py : tests for the `tesedml.py` module
"""
from __future__ import absolute_import, print_function

import tempfile
import unittest
import pytest

import matplotlib
import os
import shutil
import tellurium as te
try:
    import tesedml as libsedml
except ImportError:
    import libsedml
import phrasedml

# from tellurium.sedml.tephrasedml import experiment
# import tellurium.sedml.tephrasedml as tephrasedml

from tellurium.sedml import tesedml


class PhrasedmlTestCase(unittest.TestCase):

    def tearDown(self):
        matplotlib.pyplot.switch_backend(self.backend)

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        self.backend = matplotlib.rcParams['backend']
        matplotlib.pyplot.switch_backend("Agg")

        # create a test instance
        self.antimony = '''
        model myModel
          S1 -> S2; k1*S1;
          S1 = 10; S2 = 0;
          k1 = 1;
        end
        '''
        self.phrasedml = '''
          model1 = model "myModel"
          sim1 = simulate uniform(0, 5, 100)
          task1 = run sim1 on model1
          plot "Figure 1" time vs S1, S2
        '''
        # self.tep = tephrasedml.experiment(self.antimony, self.phrasedml)

        self.a1 = """
        model m1()
            J0: S1 -> S2; k1*S1;
            S1 = 10.0; S2=0.0;
            k1 = 0.1;
        end
        """
        self.a2 = """
        model m2()
            v0: X1 -> X2; p1*X1;
            X1 = 5.0; X2 = 20.0;
            p1 = 0.2;
        end
        """

    def tearDown(self):
        self.tep = None

    def test_execute(self):
        """Test execute."""
        inline_omex = '\n'.join([self.antimony, self.phrasedml])
        te.executeInlineOmex(inline_omex)

    def test_exportAsCombine(self):
        """ Test exportAsCombine. """
        inline_omex = '\n'.join([self.antimony, self.phrasedml])
        tmpdir = tempfile.mkdtemp()
        te.exportInlineOmex(inline_omex, os.path.join(tmpdir, 'archive.omex'))
        shutil.rmtree(tmpdir)

    def test_1Model1PhrasedML(self):
        """ Minimal example which should work. """
        antimony_str = """
        model test
            J0: S1 -> S2; k1*S1;
            S1 = 10.0; S2=0.0;
            k1 = 0.1;
        end
        """
        phrasedml_str = """
            model0 = model "test"
            sim0 = simulate uniform(0, 10, 100)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([antimony_str, phrasedml_str])
        te.executeInlineOmex(inline_omex)

    def test_1Model2PhrasedML(self):
        """ Test multiple models and multiple phrasedml files. """
        p1 = """
            model1 = model "m1"
            sim1 = simulate uniform(0, 6, 100)
            task1 = run sim1 on model1
            plot task1.time vs task1.S1, task1.S2
        """

        p2 = """
            model1 = model "m1"
            model2 = model model1 with S1=S2+20
            sim1 = simulate uniform(0, 6, 100)
            task1 = run sim1 on model2
            plot task1.time vs task1.S1, task1.S2
        """
        inline_omex = '\n'.join([self.a1, p1])
        te.executeInlineOmex(inline_omex)

        inline_omex = '\n'.join([self.a1, p2])
        te.executeInlineOmex(inline_omex)

        inline_omex = '\n'.join([self.a1, p1, p2])
        te.executeInlineOmex(inline_omex)

    def test_2Model1PhrasedML(self):
        """ Test multiple models and multiple phrasedml files. """
        p1 = """
            model1 = model "m1"
            model2 = model "m2"
            model3 = model model1 with S1=S2+20
            sim1 = simulate uniform(0, 6, 100)
            task1 = run sim1 on model1
            task2 = run sim1 on model2
            plot "Timecourse test1" task1.time vs task1.S1, task1.S2
            plot "Timecourse test2" task2.time vs task2.X1, task2.X2
        """
        inline_omex = '\n'.join([self.a1, self.a2, p1])
        te.executeInlineOmex(inline_omex)

    def test_2Model2PhrasedML(self):
        """ Test multiple models and multiple phrasedml files. """
        p1 = """
            model1 = model "m1"
            model2 = model "m2"
            sim1 = simulate uniform(0, 6, 100)
            task1 = run sim1 on model1
            task2 = run sim1 on model2
            plot task1.time vs task1.S1, task1.S2, task2.time vs task2.X1, task2.X2
        """
        p2 = """
            model1 = model "m1"
            model2 = model "m2"
            sim1 = simulate uniform(0, 20, 20)
            task1 = run sim1 on model1
            task2 = run sim1 on model2
            plot task1.time vs task1.S1, task1.S2, task2.time vs task2.X1, task2.X2
        """
        inline_omex = '\n'.join([self.a1, self.a2, p1, p2])
        te.executeInlineOmex(inline_omex)




if __name__ == '__main__':
    unittest.main()

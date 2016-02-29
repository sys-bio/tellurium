"""
Testing tephrasedml.
"""
from __future__ import print_function

import tempfile
import unittest

import tellurium.sedml.tephrasedml as tephrasedml


@unittest.skipIf(tephrasedml.phrasedml is None, "only run tests if phrasedml is available")
class tePhrasedMLTestCase(unittest.TestCase):

    def setUp(self):
        # create a test instance
        self.antimony = '''
        model myModel
          S1 -> S2; k1*S1
          S1 = 10; S2 = 0
          k1 = 1
        end
        '''
        self.phrasedml = '''
          model1 = model "myModel"
          sim1 = simulate uniform(0, 5, 100)
          task1 = run sim1 on model1
          plot "Figure 1" time vs S1, S2
        '''
        self.tep = tephrasedml.experiment(self.antimony, self.phrasedml)

    def tearDown(self):
        self.tep = None

    def test_execute(self):
        """Test execute."""
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        exp.execute(self.phrasedml)

    def test_createpython(self):
        """Test createpython."""
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        pstr = exp.createpython(self.phrasedml)
        self.assertIsNotNone(pstr)

    def test_printpython(self):
        """Test printpython."""
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        exp.printpython(self.phrasedml)

    def test_experiment(self):
        """Test experiment."""
        import tellurium as te
        exp = te.experiment(self.antimony, self.phrasedml)
        pstr = exp.createpython(self.phrasedml)
        self.assertIsNotNone(pstr)

    def test_exportAsCombine(self):
        """ Test exportAsCombine. """
        import tellurium as te
        import os
        exp = te.experiment(self.antimony, self.phrasedml)
        tmpdir = tempfile.mkdtemp()
        tmparchive = os.path.join(tmpdir, 'test.zip')
        exp.exportAsCombine(tmparchive)
        # try to re
        import zipfile
        zip = zipfile.ZipFile(tmparchive)

    def test_minimalExperiment(self):
        """ Minimal example which should work. """
        import tellurium as te
        antimonyStr = """
        model test
            J0: S1 -> S2; k1*S1;
            S1 = 10.0; S2=0.0;
            k1 = 0.1;
        end
        """
        phrasedmlStr = """
            model0 = model "test"
            sim0 = simulate uniform(0, 10, 100)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(antimonyStr, phrasedmlStr)
        exp.execute(phrasedmlStr)

    def test_kisao(self):
        import tellurium as te
        antimonyStr = """
        model test
            J0: S1 -> S2; k1*S1;
            S1 = 10.0; S2=0.0;
            k1 = 0.1;
        end
        """
        phrasedmlStr = """
            model0 = model "test"
            sim0 = simulate uniform(0, 10, 100)
            sim1.algorithm = rk4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(antimonyStr, phrasedmlStr)
        pystr = exp.createpython(phrasedmlStr)
        self.assertTrue('rk4' in pystr)

if __name__ == '__main__':
    unittest.main()

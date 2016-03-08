"""
Testing tephrasedml.
"""
from __future__ import print_function

import tempfile
import unittest
import matplotlib
import os
import shutil

import tellurium.sedml.tephrasedml as tephrasedml
import tellurium as te
import libsedml


class tePhrasedMLTestCase(unittest.TestCase):

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
        self.tep = tephrasedml.experiment(self.antimony, self.phrasedml)

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
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        exp.execute(self.phrasedml)

    def test_createpython(self):
        """Test createpython."""
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        pstr = exp._toPython(self.phrasedml)
        self.assertIsNotNone(pstr)

    def test_printpython(self):
        """Test printpython."""
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        exp.printPython(self.phrasedml)

    def test_experiment(self):
        """Test experiment."""
        exp = te.experiment(self.antimony, self.phrasedml)
        pstr = exp._toPython(self.phrasedml)
        self.assertIsNotNone(pstr)

    def test_exportAsCombine(self):
        """ Test exportAsCombine. """
        exp = te.experiment(self.antimony, self.phrasedml)
        tmpdir = tempfile.mkdtemp()
        tmparchive = os.path.join(tmpdir, 'test.zip')
        exp.exportAsCombine(tmparchive)
        # try to re
        import zipfile
        zip = zipfile.ZipFile(tmparchive)
        zip.close()
        shutil.rmtree(tmpdir)
        
    def test_update(self):
        """Test update."""
        exp = te.experiment([self.antimony], [self.phrasedml])
        tmpdir = tempfile.mkdtemp()
        tmparchive = os.path.join(tmpdir, 'test.zip')
        exp.exportAsCombine(tmparchive)
        exp.updateCombine(tmparchive)
        # try to re
        import zipfile
        zip = zipfile.ZipFile(tmparchive)
        zip.close()
        shutil.rmtree(tmpdir)

    def test_1Model1PhrasedML(self):
        """ Minimal example which should work. """
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
        exp = te.experiment(self.a1, [p1, p2])
        # execute first
        exp.execute(p1)
        # execute second
        exp.execute(p2)
        # execute all
        exp.execute()

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
        exp = te.experiment([self.a1, self.a2], p1)
        exp.execute(p1)

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
        exp = te.experiment([self.a1, self.a2], [p1, p2])
        # execute first
        exp.execute(p1)
        # execute second
        exp.execute(p2)
        # execute all
        exp.execute()

    def test_ModelAsURN(self):
        """ Provide model via urn. """
        # TODO: implement
        pass

    def test_ModelAsPath(self):
        """ Provide model as path. """
        # TODO: implement
        pass

    ###################################################################################
    # Testing Kisao Terms
    ###################################################################################
    def test_kisao(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = rk4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        # check that properly set in SEDML

        # check that string is in python
        pystr = exp._toPython(p)
        self.assertTrue('rk4' in pystr)

if __name__ == '__main__':
    unittest.main()

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
import phrasedml
from tellurium.sedml.tesedml import SEDMLCodeFactory


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
    def checkKisaoIntegrator(self, exp, kisao, name):
        """ Helper function for checking kisao integrator. """
        p = exp.phrasedmlList[0]

        # check that set Kisao set correctly in SedDocument
        phrasedml.clearReferencedSBML()
        exp._setReferencedSBML(p)
        sedml = exp._phrasedmlToSEDML(p)
        doc = libsedml.readSedMLFromString(sedml)
        algorithm = doc.getSimulation('sim0').getAlgorithm()
        self.assertEqual(algorithm.getKisaoID(), kisao)

        # check that integrator is set in python code
        pystr = exp._toPython(p)
        self.assertTrue(".setIntegrator('{}')".format(name) in pystr)

    def test_kisao_cvode_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = CVODE
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000019', 'cvode')
        exp.execute()

    def test_kisao_cvode_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.19
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000019', 'cvode')
        exp.execute()

    def test_kisao_cvode_3(self):
        """ Default of uniform is cvode. """
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000019', 'cvode')
        exp.execute()

    def test_kisao_cvode_4(self):
        """ Default of onestep is cvode. """
        p = """
            model0 = model "m1"
            sim0 = simulate onestep(10)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000019', 'cvode')
        exp.execute()

    def test_kisao_gillespie_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = gillespie
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000241', 'gillespie')
        exp.execute()

    def test_kisao_gillespie_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.241
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000241', 'gillespie')
        exp.execute()

    def test_kisao_gillespie_3(self):
        """ Default of uniform_stochastic is gillespie."""
        p = """
            model0 = model "m1"
            sim0 = simulate uniform_stochastic(0, 10, 100)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000241', 'gillespie')
        exp.execute()

    def test_kisao_rk4_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = rk4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000032', 'rk4')
        exp.execute()

    def test_kisao_rk4_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.32
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000032', 'rk4')
        exp.execute()

    # Fails due to : https://github.com/sys-bio/roadrunner/issues/307
    '''
    def test_kisao_rk45_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = rk45
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000435', 'rk45')
        exp.execute()

    def test_kisao_rk45_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.435
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoIntegrator(exp, 'KISAO:0000435', 'rk45')
        exp.execute()
    '''

    def checkKisaoAlgorithmParameter(self, exp, kisao, name, value):
        """ Helper function for checking kisao parameter. """
        p = exp.phrasedmlList[0]

        # check that set AlgorithmParameter set correctly in SED-ML
        phrasedml.clearReferencedSBML()
        exp._setReferencedSBML(p)
        sedml = exp._phrasedmlToSEDML(p)
        doc = libsedml.readSedMLFromString(sedml)
        algorithm = doc.getSimulation('sim0').getAlgorithm()
        pdict = {p.getKisaoID(): p for p in algorithm.getListOfAlgorithmParameters()}

        self.assertTrue(kisao in pdict)
        pkey = SEDMLCodeFactory.algorithmParameterToParameterKey(pdict[kisao])

        if pkey.dtype == str:
            self.assertEqual(pkey.value, value)
        else:
            # numerical parameter
            self.assertAlmostEqual(float(pkey.value), value)

        # check that integrator is set in python code
        pystr = exp._toPython(p)
        if pkey.dtype == str:
            self.assertTrue("getIntegrator().setValue('{}', '{}')".format(name, value) in pystr)
        else:
            # numerical parameter
            self.assertTrue("getIntegrator().setValue('{}', {})".format(name, value) in pystr)

    def test_kisao_relative_tolerance_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.relative_tolerance = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000209', 'relative_tolerance', 1E-8)
        exp.execute()

    def test_kisao_relative_tolerance_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.209 = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000209', 'relative_tolerance', 1E-8)
        exp.execute()

    def test_kisao_absolute_tolerance_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.absolute_tolerance = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000211', 'absolute_tolerance', 1E-8)
        exp.execute()

    def test_kisao_absolute_tolerance_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.211 = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000211', 'absolute_tolerance', 1E-8)
        exp.execute()

    def test_kisao_maximum_bdf_order_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.maximum_bdf_order = 4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000220', 'maximum_bdf_order', 4)
        exp.execute()

    def test_kisao_maximum_bdf_order_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.220 = 4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000220', 'maximum_bdf_order', 4)
        exp.execute()

    def test_kisao_maximum_adams_order_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.maximum_adams_order = 4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000219', 'maximum_adams_order', 4)
        exp.execute()

    def test_kisao_maximum_bdf_order_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.219 = 4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        exp = te.experiment(self.a1, p)
        self.checkKisaoAlgorithmParameter(exp, 'KISAO:0000220', 'maximum_bdf_order', 4)
        exp.execute()


if __name__ == '__main__':
    unittest.main()

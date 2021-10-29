"""
Testing the support of KISAO terms for SED-ML simulations.

    test_sedml_phrasedml.py : phrasedml based tests.
    test_sedml_kisao.py : SED-ML kisao support
    test_sedml_omex.py : SED-ML tests based on Combine Archives
    test_sedml_sedml.py : sed-ml tests
"""
from __future__ import absolute_import, print_function

import os
import shutil
import tempfile
import unittest
import pytest
import six
import matplotlib

import tellurium as te
try:
    import libsedml
except ImportError:
    import tesedml as libsedml

from tellurium.sedml import tesedml
from tellurium.utils import omex


class KisaoSedmlTestCase(unittest.TestCase):

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        self.test_dir = tempfile.mkdtemp()
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
        matplotlib.pyplot.switch_backend(self.backend)
        shutil.rmtree(self.test_dir)
        matplotlib.pyplot.close('all')


    def checkKisaoIntegrator(self, inline_omex, kisao, name):
        """ Helper function for checking kisao integrator. """

        omex_file = os.path.join(self.test_dir, "test.omex")
        te.exportInlineOmex(inline_omex, omex_file)
        omex.extractCombineArchive(omex_file, directory=self.test_dir, method="zip")

        locations = omex.getLocationsByFormat(omex_file, "sed-ml")
        sedml_files = [os.path.join(self.test_dir, loc) for loc in locations]
        sedml_file = sedml_files[0]
        # check the SED-ML
        doc = libsedml.readSedMLFromFile(sedml_file)
        # test_str = libsedml.writeSedMLToString(doc)
        # print(test_str)

        simulation = doc.getSimulation('sim0')
        algorithm = simulation.getAlgorithm()
        assert algorithm.getKisaoID() == kisao

        # check the generated code
        pystr = tesedml.sedmlToPython(sedml_file, workingDir=self.test_dir)

        # is integrator/solver set in python code
        if simulation.getTypeCode() is libsedml.SEDML_SIMULATION_STEADYSTATE:
            assert ".setSteadyStateSolver('{}')".format(name) in pystr
        else:
            assert ".setIntegrator('{}')".format(name) in pystr


    def checkKisaoAlgorithmParameter(self, inline_omex, kisao, name, value):
        """ Helper function for checking kisao parameter. """

        # check that set AlgorithmParameter set correctly in SED-ML
        omex_file = os.path.join(self.test_dir, "test.omex")
        te.exportInlineOmex(inline_omex, omex_file)
        omex.extractCombineArchive(omex_file, directory=self.test_dir, method="zip")

        locations = omex.getLocationsByFormat(omex_file, "sed-ml")
        sedml_files = [os.path.join(self.test_dir, loc) for loc in locations]
        sedml_file = sedml_files[0]

        doc = libsedml.readSedMLFromFile(sedml_file)
        simulation = doc.getSimulation('sim0')
        algorithm = simulation.getAlgorithm()
        pdict = {p.getKisaoID(): p for p in algorithm.getListOfAlgorithmParameters()}

        self.assertTrue(kisao in pdict)
        pkey = tesedml.SEDMLCodeFactory.algorithmParameterToParameterKey(pdict[kisao])

        if pkey.dtype == str:
            self.assertEqual(pkey.value, value)
        else:
            # numerical parameter
            self.assertAlmostEqual(float(pkey.value), value)

        # check that integrator is set in python code
        pystr = tesedml.sedmlToPython(sedml_file, workingDir=self.test_dir)

        print(simulation.getElementName())
        print(pystr)
        if simulation.getTypeCode() is libsedml.SEDML_SIMULATION_STEADYSTATE:
            if pkey.dtype == str:
                self.assertTrue(".steadyStateSolver.setValue('{}', '{}')".format(name, value) in pystr)
            else:
                # numerical parameter
                self.assertTrue(".steadyStateSolver.setValue('{}', {})".format(name, value) in pystr)
        else:
            if pkey.dtype == str:
                self.assertTrue(".integrator.setValue('{}', '{}')".format(name, value) in pystr)
            else:
                # numerical parameter
                self.assertTrue(".integrator.setValue('{}', {})".format(name, value) in pystr)

    def test_kisao_cvode_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = CVODE
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000019', 'cvode')
        te.executeInlineOmex(inline_omex)

    def test_kisao_cvode_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.19
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000019', 'cvode')
        te.executeInlineOmex(inline_omex)

    def test_kisao_cvode_3(self):
        """ Default of uniform is cvode. """
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000019', 'cvode')
        te.executeInlineOmex(inline_omex)

    def test_kisao_cvode_4(self):
        """ Default of onestep is cvode. """
        p = """
            model0 = model "m1"
            sim0 = simulate onestep(10)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000019', 'cvode')
        te.executeInlineOmex(inline_omex)

    def test_kisao_gillespie_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = gillespie
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000241', 'gillespie')
        te.executeInlineOmex(inline_omex)

    def test_kisao_gillespie_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.241
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000241', 'gillespie')
        te.executeInlineOmex(inline_omex)

    def test_kisao_gillespie_3(self):
        """ Default of uniform_stochastic is gillespie."""
        p = """
            model0 = model "m1"
            sim0 = simulate uniform_stochastic(0, 10, 100)
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000241', 'gillespie')
        te.executeInlineOmex(inline_omex)

    def test_kisao_rk4_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = rk4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000032', 'rk4')
        te.executeInlineOmex(inline_omex)

    def test_kisao_rk4_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.32
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000032', 'rk4')
        te.executeInlineOmex(inline_omex)


    def test_kisao_bdf(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = stiff
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000288', 'cvode')
        te.executeInlineOmex(inline_omex)

        omex_file = os.path.join(self.test_dir, "test.omex")
        te.exportInlineOmex(inline_omex, omex_file)
        pycode_dict = tesedml.combineArchiveToPython(omex_file)
        pycode = six.next(six.itervalues(pycode_dict))
        print(pycode)
        self.assertTrue("integrator.setValue('stiff', True)" in pycode)


    def test_kisao_adams(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = nonstiff
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000280', 'cvode')
        te.executeInlineOmex(inline_omex)

        omex_file = os.path.join(self.test_dir, "test.omex")
        te.exportInlineOmex(inline_omex, omex_file)
        pycode_dict = tesedml.combineArchiveToPython(omex_file)
        pycode = six.next(six.itervalues(pycode_dict))
        print(pycode)
        self.assertTrue("integrator.setValue('stiff', False)" in pycode)


    def test_kisao_euler_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.30
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000030', 'euler')
        te.executeInlineOmex(inline_omex)

        omex_file = os.path.join(self.test_dir, "test.omex")
        te.exportInlineOmex(inline_omex, omex_file)
        pycode_dict = tesedml.combineArchiveToPython(omex_file)
        pycode = six.next(six.itervalues(pycode_dict))
        print(pycode)
        self.assertTrue("model0.setIntegrator('euler')" in pycode)


    def test_kisao_euler_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.261
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000261', 'euler')
        te.executeInlineOmex(inline_omex)

        omex_file = os.path.join(self.test_dir, "test.omex")
        te.exportInlineOmex(inline_omex, omex_file)
        pycode_dict = tesedml.combineArchiveToPython(omex_file)
        pycode = six.next(six.itervalues(pycode_dict))
        print(pycode)
        self.assertTrue("model0.setIntegrator('euler')" in pycode)


    @pytest.mark.skip(reason="bug in roadrunner")
    def test_kisao_rk45_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = rk45
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000435', 'rk45')
        te.executeInlineOmex(inline_omex)


    @pytest.mark.skip(reason="bug in roadrunner")
    def test_kisao_rk45_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm = kisao.435
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoIntegrator(inline_omex, 'KISAO:0000435', 'rk45')
        te.executeInlineOmex(inline_omex)

    def test_kisao_relative_tolerance_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.relative_tolerance = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000209', 'relative_tolerance', 1E-8)
        te.executeInlineOmex(inline_omex)

    def test_kisao_relative_tolerance_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.209 = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000209', 'relative_tolerance', 1E-8)
        te.executeInlineOmex(inline_omex)

    def test_kisao_absolute_tolerance_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.absolute_tolerance = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000211', 'absolute_tolerance', 1E-8)
        te.executeInlineOmex(inline_omex)

    def test_kisao_absolute_tolerance_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.211 = 1E-8
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000211', 'absolute_tolerance', 1E-8)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_bdf_order_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.maximum_bdf_order = 4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000220', 'maximum_bdf_order', 4)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_bdf_order_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.220 = 4
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000220', 'maximum_bdf_order', 4)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_adams_order_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.maximum_adams_order = 5
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000219', 'maximum_adams_order', 5)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_adams_order_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.219 = 5
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000219', 'maximum_adams_order', 5)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_num_steps_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.maximum_num_steps = 10000
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000415', 'maximum_num_steps', 10000)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_num_steps_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.415 = 10000
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000415', 'maximum_num_steps', 10000)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_time_step_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.maximum_time_step = 1.0
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000467', 'maximum_time_step', 1.0)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_time_step_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.467 = 1.0
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000467', 'maximum_time_step', 1.0)
        te.executeInlineOmex(inline_omex)

    # @pytest.mark.skip(reason="bug in roadrunner")
    def test_kisao_minimum_time_step_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.minimum_time_step = 1E-6
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000485', 'minimum_time_step', 1E-6)
        te.executeInlineOmex(inline_omex)

    # @pytest.mark.skip(reason="bug in roadrunner")
    def test_kisao_minimum_time_step_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.485 = 1E-6
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000485', 'minimum_time_step', 1E-6)
        te.executeInlineOmex(inline_omex)

    def test_kisao_nonnegative(self):
        """ Check nonnegative setting."""
        p = """
            model0 = model "m1"
            sim0 = simulate uniform_stochastic(0, 10, 100)
            sim0.algorithm.673 = true
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000673', 'nonnegative', True)
        te.executeInlineOmex(inline_omex)
        omex_file = os.path.join(self.test_dir, "test.omex")
        te.exportInlineOmex(inline_omex, omex_file)
        pycode_dict = tesedml.combineArchiveToPython(omex_file)
        pycode = six.next(six.itervalues(pycode_dict))
        print(pycode)
        self.assertTrue("model0.integrator.setValue('nonnegative', True)" in pycode)

    def test_kisao_initial_time_step_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.initial_time_step = 0.01
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000559', 'initial_time_step', 0.01)
        te.executeInlineOmex(inline_omex)

    def test_kisao_initial_time_step_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.559 = 0.01
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000559', 'initial_time_step', 0.01)
        te.executeInlineOmex(inline_omex)

    def test_kisao_variable_step_size_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.variable_step_size = true
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000107', 'variable_step_size', True)
        te.executeInlineOmex(inline_omex)

    def test_kisao_variable_step_size_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform(0, 10, 100)
            sim0.algorithm.107 = true
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000107', 'variable_step_size', True)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_iterations_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate steadystate
            sim0.algorithm.maximum_iterations = 10
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000486', 'maximum_iterations', 10)
        te.executeInlineOmex(inline_omex)

    def test_kisao_maximum_iterations_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate steadystate
            sim0.algorithm.486 = 10
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000486', 'maximum_iterations', 10)
        te.executeInlineOmex(inline_omex)

    def test_kisao_minimum_damping_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate steadystate
            sim0.algorithm.minimum_damping = 1.0
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000487', 'minimum_damping', 1.0)
        te.executeInlineOmex(inline_omex)

    def test_kisao_minimum_damping_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate steadystate
            sim0.algorithm.487 = 1
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000487', 'minimum_damping', 1.0)
        te.executeInlineOmex(inline_omex)

    def test_kisao_seed_1(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform_stochastic(0, 10, 100)
            sim0.algorithm.seed = 1234
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000488', 'seed', 1234)
        te.executeInlineOmex(inline_omex)

    def test_kisao_seed_2(self):
        p = """
            model0 = model "m1"
            sim0 = simulate uniform_stochastic(0, 10, 100)
            sim0.algorithm.488 = 1234
            task0 = run sim0 on model0
            plot task0.time vs task0.S1
        """
        inline_omex = '\n'.join([self.a1, p])
        self.checkKisaoAlgorithmParameter(inline_omex, 'KISAO:0000488', 'seed', 1234)
        te.executeInlineOmex(inline_omex)

if __name__ == "__main__":
    import unittest
    unittest.main()

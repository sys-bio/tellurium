"""
Testing phrasedml.

    test_sedml_phrasedml.py : phrasedml based tests.
    test_sedml_kisao.py : SED-ML kisao support
    test_sedml_omex.py : SED-ML tests based on Combine Archives
    test_sedml_sedml.py : sed-ml tests
"""
from __future__ import absolute_import, print_function, division

import os
import shutil
import tempfile
import unittest
import pytest
import matplotlib

import tellurium as te
try:
    import tesedml as libsedml
except ImportError:
    import libsedml
import phrasedml

from tellurium.sedml.utils import run_case
from tellurium import temiriam
from tellurium.utils import omex
from tellurium.sedml.tesedml import executeSEDML, executeCombineArchive


class PhrasedmlTestCase(unittest.TestCase):
    """ Testing execution and archives based on phrasedml input. """

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
        matplotlib.pyplot.switch_backend(self.backend)
        matplotlib.pyplot.close('all')

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

    ############################################
    # Real world tests
    ############################################

    def run_example(self, a_str, p_str):
        # execute
        tmpdir = tempfile.mkdtemp()
        try:
            run_case(
                call_file=os.path.realpath(__file__),
                antimony_str=a_str,
                phrasedml_str=p_str,
                working_dir=tmpdir
            )
        finally:
            shutil.rmtree(tmpdir)

    def test_case_01(self):
        a_str = """
        model case_01
            J0: S1 -> S2; k1*S1;
            S1 = 10.0; S2=0.0;
            k1 = 0.1;
        end
        """
        p_str = """
            model0 = model "case_01"
            sim0 = simulate uniform(0, 10, 100)
            task0 = run sim0 on model0
            plot "UniformTimecourse" task0.time vs task0.S1
            report task0.time vs task0.S1
        """
        self.run_example(a_str, p_str)

    def test_case_02(self):
        a_str = """
        model case_02
            J0: S1 -> S2; k1*S1;
            S1 = 10.0; S2=0.0;
            k1 = 0.1;
        end
        """
        p_str = """
            model0 = model "case_02"
            model1 = model model0 with S1=5.0
            sim0 = simulate uniform(0, 6, 100)
            task0 = run sim0 on model1
            task1 = repeat task0 for k1 in uniform(0.0, 5.0, 5), reset = true
            plot "Repeated task with reset" task1.time vs task1.S1, task1.S2
            report task1.time vs task1.S1, task1.S2
            plot "Repeated task varying k1" task1.k1 vs task1.S1
            report task1.k1 vs task1.S1
        """
        self.run_example(a_str, p_str)

    def test_case_03(self):
        a_str = '''
        model case_03()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_03"
          mod2 = model mod1 with S2=S1+4
          sim1 = simulate uniform(0, 10, 100)
          task1 = run sim1 on mod1
          task2 = run sim1 on mod2
          plot "ComputeChanges" task1.time vs task1.S1, task1.S2, task2.S1, task2.S2
          report task1.time vs task1.S1, task1.S2, task2.S1, task2.S2
        '''
        self.run_example(a_str, p_str)

    def test_case_04(self):
        a_str = '''
        model case_04()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_04"
          mod2 = model mod1 with S2=S1+4
          mod3 = model mod2 with S1=20.0
          sim1 = simulate uniform(0, 10, 100)
          task1 = run sim1 on mod1
          task2 = run sim1 on mod2
          task3 = run sim1 on mod3
          plot "Example plot" task1.time vs task1.S1, task1.S2, task2.S1, task2.S2, task3.S1, task3.S2
          report task1.time vs task1.S1, task1.S2, task2.S1, task2.S2, task3.S1, task3.S2
        '''
        self.run_example(a_str, p_str)

    def test_case_05(self):
        a_str = '''
        model case_05()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_05"
          sim1 = simulate uniform(0, 10, 100)
          task1 = run sim1 on mod1
          plot "Example plot" task1.time vs task1.S1, task1.S2, task1.S1/task1.S2
          report task1.time vs task1.S1, task1.S2, task1.S1/task1.S2
          plot "Normalized plot" task1.S1/max(task1.S1) vs task1.S2/max(task1.S2)
          report task1.S1/max(task1.S1) vs task1.S2/max(task1.S2)
        '''
        self.run_example(a_str, p_str)

    def test_case_06(self):
        a_str = '''
        model case_06()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_06"
          sim1 = simulate uniform(0, 10, 100)
          task1 = run sim1 on mod1
          repeat1 = repeat task1 for S1 in [1, 3, 5], S2 in uniform(0, 10, 2), reset=True
          repeat2 = repeat task1 for S1 in [1, 3, 5], S2 in uniform(0, 10, 2), reset=False
          plot "Example plot" repeat1.time vs repeat1.S1, repeat1.S2
          report repeat1.time vs repeat1.S1, repeat1.S2
          plot "Example plot" repeat2.time vs repeat2.S1, repeat2.S2
          report repeat2.time vs repeat2.S1, repeat2.S2
        '''
        self.run_example(a_str, p_str)

    def test_case_07(self):
        a_str = '''
        model case_07()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_07"
          sim1 = simulate uniform(0, 10, 100)
          task1 = run sim1 on mod1
          repeat1 = repeat task1 for S1 in [1, 3, 5], reset=True
          report task1.time, task1.S1, task1.S2, task1.S1/task1.S2
          report repeat1.time, repeat1.S1, repeat1.S2, repeat1.S1/repeat1.S2
        '''
        self.run_example(a_str, p_str)

    def test_case_08(self):
        a_str = '''
        model case_08()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_08"
          mod2 = model "case_08"
          sim1 = simulate uniform(0, 10, 20)
          sim2 = simulate uniform(0, 3, 10)
          task1 = run sim1 on mod1
          task2 = run sim2 on mod1
          repeat1 = repeat [task1, task2] for S2 in uniform(0, 10, 9), mod1.S1 = S2+3, reset=False
          plot "Repeated Multiple Subtasks" repeat1.mod1.time vs repeat1.mod1.S1, repeat1.mod1.S2
          # plot "Repeated Multiple Subtasks" repeat1.mod2.time vs repeat1.mod2.S1, repeat1.mod2.S2
        '''
        self.run_example(a_str, p_str)

    def test_case_09(self):
        a_str = '''
        // Created by libAntimony v2.9
        model *case_09()

        // Compartments and Species:
        compartment compartment_;
        species MKKK in compartment_, MKKK_P in compartment_, MKK in compartment_;
        species MKK_P in compartment_, MKK_PP in compartment_, MAPK in compartment_;
        species MAPK_P in compartment_, MAPK_PP in compartment_;

        // Reactions:
        J0: MKKK => MKKK_P; (J0_V1*MKKK)/((1 + (MAPK_PP/J0_Ki)^J0_n)*(J0_K1 + MKKK));
        J1: MKKK_P => MKKK; (J1_V2*MKKK_P)/(J1_KK2 + MKKK_P);
        J2: MKK => MKK_P; (J2_k3*MKKK_P*MKK)/(J2_KK3 + MKK);
        J3: MKK_P => MKK_PP; (J3_k4*MKKK_P*MKK_P)/(J3_KK4 + MKK_P);
        J4: MKK_PP => MKK_P; (J4_V5*MKK_PP)/(J4_KK5 + MKK_PP);
        J5: MKK_P => MKK; (J5_V6*MKK_P)/(J5_KK6 + MKK_P);
        J6: MAPK => MAPK_P; (J6_k7*MKK_PP*MAPK)/(J6_KK7 + MAPK);
        J7: MAPK_P => MAPK_PP; (J7_k8*MKK_PP*MAPK_P)/(J7_KK8 + MAPK_P);
        J8: MAPK_PP => MAPK_P; (J8_V9*MAPK_PP)/(J8_KK9 + MAPK_PP);
        J9: MAPK_P => MAPK; (J9_V10*MAPK_P)/(J9_KK10 + MAPK_P);

        // Species initializations:
        MKKK = 90;
        MKKK_P = 10;
        MKK = 280;
        MKK_P = 10;
        MKK_PP = 10;
        MAPK = 280;
        MAPK_P = 10;
        MAPK_PP = 10;

        // Compartment initializations:
        compartment_ = 1;

        // Variable initializations:
        J0_V1 = 2.5;
        J0_Ki = 9;
        J0_n = 1;
        J0_K1 = 10;
        J1_V2 = 0.25;
        J1_KK2 = 8;
        J2_k3 = 0.025;
        J2_KK3 = 15;
        J3_k4 = 0.025;
        J3_KK4 = 15;
        J4_V5 = 0.75;
        J4_KK5 = 15;
        J5_V6 = 0.75;
        J5_KK6 = 15;
        J6_k7 = 0.025;
        J6_KK7 = 15;
        J7_k8 = 0.025;
        J7_KK8 = 15;
        J8_V9 = 0.5;
        J8_KK9 = 15;
        J9_V10 = 0.5;
        J9_KK10 = 15;

        // Other declarations:
        const compartment_, J0_V1, J0_Ki, J0_n, J0_K1, J1_V2, J1_KK2, J2_k3, J2_KK3;
        const J3_k4, J3_KK4, J4_V5, J4_KK5, J5_V6, J5_KK6, J6_k7, J6_KK7, J7_k8;
        const J7_KK8, J8_V9, J8_KK9, J9_V10, J9_KK10;
        end
        '''
        p_str = '''
          mod1 = model "case_09"
          # sim1 = simulate uniform_stochastic(0, 4000, 1000)
          sim1 = simulate uniform(0, 4000, 1000)
          task1 = run sim1 on mod1
          repeat1 = repeat task1 for local.x in uniform(0, 10, 10), reset=true
          plot "MAPK oscillations" repeat1.MAPK vs repeat1.time vs repeat1.MAPK_P, repeat1.MAPK vs repeat1.time vs repeat1.MAPK_PP, repeat1.MAPK vs repeat1.time vs repeat1.MKK
          report repeat1.MAPK vs repeat1.time vs repeat1.MAPK_P, repeat1.MAPK vs repeat1.time vs repeat1.MAPK_PP, repeat1.MAPK vs repeat1.time vs repeat1.MKK
        '''
        self.run_example(a_str, p_str)

    def test_case_10(self):
        a_str = '''
        model case_10()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_10"
          mod2 = model "case_10"
          sim1 = simulate uniform(0, 10, 100)
          sim2 = simulate uniform(0, 3, 10)
          task1 = run sim1 on mod1
          task2 = run sim2 on mod2
          repeat1 = repeat [task1, task2] for local.X in uniform(0, 10, 9), mod1.S1 = X, mod2.S1 = X+3
          plot repeat1.mod1.time vs repeat1.mod1.S1, repeat1.mod1.S2, repeat1.mod2.time vs repeat1.mod2.S1, repeat1.mod2.S2
        '''
        self.run_example(a_str, p_str)

    def test_case_11(self):
        a_str = '''
        model case_11()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.5; k2=0.4
        end
        '''
        p_str = '''
          mod1 = model "case_11"
          sim1 = simulate uniform(0, 10, 100)
          task1 = run sim1 on mod1
          rtask1 = repeat task1 for k1 in uniform(0, 1, 2)
          rtask2 = repeat rtask1 for k2 in uniform(0, 1, 3)
          rtask3 = repeat rtask2 for S1 in [5, 10], reset=true
          plot "RepeatedTask of RepeatedTask" rtask3.time vs rtask3.S1, rtask3.S2
          plot rtask3.k1 vs rtask3.k2 vs rtask3.S1
        '''
        self.run_example(a_str, p_str)

    def test_case_12(self):
        a_str = '''
        model case_12()
          J0: S1 -> S2; k1*S1-k2*S2
          S1 = 10.0; S2 = 0.0;
          k1 = 0.2; k2=0.01
        end
        '''
        p_str = '''
          mod1 = model "case_12"
          sim1 = simulate uniform(0, 2, 10, 49)
          sim2 = simulate uniform(0, 15, 49)
          task1 = run sim1 on mod1
          task2 = run sim2 on mod1
          repeat1 = repeat task1 for S1 in uniform(0, 10, 4), S2 = S1+20, reset=true
          repeat2 = repeat task2 for S1 in uniform(0, 10, 4), S2 = S1+20, reset=true
          plot "Offset simulation" repeat2.time vs repeat2.S1, repeat2.S2, repeat1.time vs repeat1.S1, repeat1.S2
          report repeat2.time vs repeat2.S1, repeat2.S2, repeat1.time vs repeat1.S1, repeat1.S2
        '''
        self.run_example(a_str, p_str)

    def test_lorenz(self):
        a_str = '''
        model lorenz
          x' = sigma*(y - x);
          y' = x*(rho - z) - y;
          z' = x*y - beta*z;
          x = 0.96259;  y = 2.07272;  z = 18.65888;
          sigma = 10;  rho = 28; beta = 2.67;
        end
        '''

        p_str = '''
        model1 = model "lorenz"
        sim1 = simulate uniform(0,15,2000)
        task1 = run sim1 on model1
        plot task1.z vs task1.x
        '''
        self.run_example(a_str, p_str)

    def test_oneStep(self):
        a_str = '''
        // Created by libAntimony v2.9
        model *oneStep()

        // Compartments and Species:
        compartment compartment_;
        species S1 in compartment_, S2 in compartment_, $X0 in compartment_, $X1 in compartment_;
        species $X2 in compartment_;

        // Reactions:
        J0: $X0 => S1; J0_v0;
        J1: S1 => $X1; J1_k3*S1;
        J2: S1 => S2; (J2_k1*S1 - J2_k_1*S2)*(1 + J2_c*S2^J2_q);
        J3: S2 => $X2; J3_k2*S2;

        // Species initializations:
        S1 = 0;
        S2 = 1;
        X0 = 1;
        X1 = 0;
        X2 = 0;

        // Compartment initializations:
        compartment_ = 1;

        // Variable initializations:
        J0_v0 = 8;
        J1_k3 = 0;
        J2_k1 = 1;
        J2_k_1 = 0;
        J2_c = 1;
        J2_q = 3;
        J3_k2 = 5;

        // Other declarations:
        const compartment_, J0_v0, J1_k3, J2_k1, J2_k_1, J2_c, J2_q, J3_k2;
        end
        '''
        p_str = '''
        model1 = model "oneStep"
        stepper = simulate onestep(0.1)
        task0 = run stepper on model1
        task1 = repeat task0 for local.x in uniform(0, 10, 100), J0_v0 = piecewise(8, x<4, 0.1, 4<=x<6, 8)
        plot "One Step Simulation" task1.time vs task1.S1, task1.S2, task1.J0_v0
        report task1.time vs task1.S1, task1.S2, task1.J0_v0
        '''
        self.run_example(a_str, p_str)

    def test_parameterScan1D(self):
        a_str = '''
        // Created by libAntimony v2.9
        model *parameterScan1D()

        // Compartments and Species:
        compartment compartment_;
        species S1 in compartment_, S2 in compartment_, $X0 in compartment_, $X1 in compartment_;
        species $X2 in compartment_;

        // Reactions:
        J0: $X0 => S1; J0_v0;
        J1: S1 => $X1; J1_k3*S1;
        J2: S1 => S2; (J2_k1*S1 - J2_k_1*S2)*(1 + J2_c*S2^J2_q);
        J3: S2 => $X2; J3_k2*S2;

        // Species initializations:
        S1 = 0;
        S2 = 1;
        X0 = 1;
        X1 = 0;
        X2 = 0;

        // Compartment initializations:
        compartment_ = 1;

        // Variable initializations:
        J0_v0 = 8;
        J1_k3 = 0;
        J2_k1 = 1;
        J2_k_1 = 0;
        J2_c = 1;
        J2_q = 3;
        J3_k2 = 5;

        // Other declarations:
        const compartment_, J0_v0, J1_k3, J2_k1, J2_k_1, J2_c, J2_q, J3_k2;
        end
        '''
        p_str = '''
        model1 = model "parameterScan1D"
        timecourse1 = simulate uniform(0, 20, 1000)
        task0 = run timecourse1 on model1
        task1 = repeat task0 for J0_v0 in [8, 4, 0.4], reset=true
        plot task1.time vs task1.S1, task1.S2
        '''
        self.run_example(a_str, p_str)

    def test_parameterScan2D(self):
        a_str = '''
        // Created by libAntimony v2.9
        model *parameterScan2D()

          // Compartments and Species:
          compartment compartment_;
          species MKKK in compartment_, MKKK_P in compartment_, MKK in compartment_;
          species MKK_P in compartment_, MKK_PP in compartment_, MAPK in compartment_;
          species MAPK_P in compartment_, MAPK_PP in compartment_;

          // Reactions:
          J0: MKKK => MKKK_P; (J0_V1*MKKK)/((1 + (MAPK_PP/J0_Ki)^J0_n)*(J0_K1 + MKKK));
          J1: MKKK_P => MKKK; (J1_V2*MKKK_P)/(J1_KK2 + MKKK_P);
          J2: MKK => MKK_P; (J2_k3*MKKK_P*MKK)/(J2_KK3 + MKK);
          J3: MKK_P => MKK_PP; (J3_k4*MKKK_P*MKK_P)/(J3_KK4 + MKK_P);
          J4: MKK_PP => MKK_P; (J4_V5*MKK_PP)/(J4_KK5 + MKK_PP);
          J5: MKK_P => MKK; (J5_V6*MKK_P)/(J5_KK6 + MKK_P);
          J6: MAPK => MAPK_P; (J6_k7*MKK_PP*MAPK)/(J6_KK7 + MAPK);
          J7: MAPK_P => MAPK_PP; (J7_k8*MKK_PP*MAPK_P)/(J7_KK8 + MAPK_P);
          J8: MAPK_PP => MAPK_P; (J8_V9*MAPK_PP)/(J8_KK9 + MAPK_PP);
          J9: MAPK_P => MAPK; (J9_V10*MAPK_P)/(J9_KK10 + MAPK_P);

          // Species initializations:
          MKKK = 90;
          MKKK_P = 10;
          MKK = 280;
          MKK_P = 10;
          MKK_PP = 10;
          MAPK = 280;
          MAPK_P = 10;
          MAPK_PP = 10;

          // Compartment initializations:
          compartment_ = 1;

          // Variable initializations:
          J0_V1 = 2.5;
          J0_Ki = 9;
          J0_n = 1;
          J0_K1 = 10;
          J1_V2 = 0.25;
          J1_KK2 = 8;
          J2_k3 = 0.025;
          J2_KK3 = 15;
          J3_k4 = 0.025;
          J3_KK4 = 15;
          J4_V5 = 0.75;
          J4_KK5 = 15;
          J5_V6 = 0.75;
          J5_KK6 = 15;
          J6_k7 = 0.025;
          J6_KK7 = 15;
          J7_k8 = 0.025;
          J7_KK8 = 15;
          J8_V9 = 0.5;
          J8_KK9 = 15;
          J9_V10 = 0.5;
          J9_KK10 = 15;

          // Other declarations:
          const compartment_, J0_V1, J0_Ki, J0_n, J0_K1, J1_V2, J1_KK2, J2_k3, J2_KK3;
          const J3_k4, J3_KK4, J4_V5, J4_KK5, J5_V6, J5_KK6, J6_k7, J6_KK7, J7_k8;
          const J7_KK8, J8_V9, J8_KK9, J9_V10, J9_KK10;
        end
        '''
        p_str = '''
          model_3 = model "parameterScan2D"
          sim_repeat = simulate uniform(0,3000,100)
          task_1 = run sim_repeat on model_3
          repeatedtask_1 = repeat task_1 for J1_KK2 in [1, 5, 10, 50, 60, 70, 80, 90, 100], reset=true
          repeatedtask_2 = repeat repeatedtask_1 for J4_KK5 in uniform(1, 40, 10), reset=true
          plot repeatedtask_2.J4_KK5 vs repeatedtask_2.J1_KK2
          plot repeatedtask_2.time vs repeatedtask_2.MKK, repeatedtask_2.MKK_P
        '''
        self.run_example(a_str, p_str)

    def test_repeatedStochastic(self):
        a_str = '''
        // Created by libAntimony v2.9
        model *repeatedStochastic()

        // Compartments and Species:
        compartment compartment_;
        species MKKK in compartment_, MKKK_P in compartment_, MKK in compartment_;
        species MKK_P in compartment_, MKK_PP in compartment_, MAPK in compartment_;
        species MAPK_P in compartment_, MAPK_PP in compartment_;

        // Reactions:
        J0: MKKK => MKKK_P; (J0_V1*MKKK)/((1 + (MAPK_PP/J0_Ki)^J0_n)*(J0_K1 + MKKK));
        J1: MKKK_P => MKKK; (J1_V2*MKKK_P)/(J1_KK2 + MKKK_P);
        J2: MKK => MKK_P; (J2_k3*MKKK_P*MKK)/(J2_KK3 + MKK);
        J3: MKK_P => MKK_PP; (J3_k4*MKKK_P*MKK_P)/(J3_KK4 + MKK_P);
        J4: MKK_PP => MKK_P; (J4_V5*MKK_PP)/(J4_KK5 + MKK_PP);
        J5: MKK_P => MKK; (J5_V6*MKK_P)/(J5_KK6 + MKK_P);
        J6: MAPK => MAPK_P; (J6_k7*MKK_PP*MAPK)/(J6_KK7 + MAPK);
        J7: MAPK_P => MAPK_PP; (J7_k8*MKK_PP*MAPK_P)/(J7_KK8 + MAPK_P);
        J8: MAPK_PP => MAPK_P; (J8_V9*MAPK_PP)/(J8_KK9 + MAPK_PP);
        J9: MAPK_P => MAPK; (J9_V10*MAPK_P)/(J9_KK10 + MAPK_P);

        // Species initializations:
        MKKK = 90;
        MKKK_P = 10;
        MKK = 280;
        MKK_P = 10;
        MKK_PP = 10;
        MAPK = 280;
        MAPK_P = 10;
        MAPK_PP = 10;

        // Compartment initializations:
        compartment_ = 1;

        // Variable initializations:
        J0_V1 = 2.5;
        J0_Ki = 9;
        J0_n = 1;
        J0_K1 = 10;
        J1_V2 = 0.25;
        J1_KK2 = 8;
        J2_k3 = 0.025;
        J2_KK3 = 15;
        J3_k4 = 0.025;
        J3_KK4 = 15;
        J4_V5 = 0.75;
        J4_KK5 = 15;
        J5_V6 = 0.75;
        J5_KK6 = 15;
        J6_k7 = 0.025;
        J6_KK7 = 15;
        J7_k8 = 0.025;
        J7_KK8 = 15;
        J8_V9 = 0.5;
        J8_KK9 = 15;
        J9_V10 = 0.5;
        J9_KK10 = 15;

        // Other declarations:
        const compartment_, J0_V1, J0_Ki, J0_n, J0_K1, J1_V2, J1_KK2, J2_k3, J2_KK3;
        const J3_k4, J3_KK4, J4_V5, J4_KK5, J5_V6, J5_KK6, J6_k7, J6_KK7, J7_k8;
        const J7_KK8, J8_V9, J8_KK9, J9_V10, J9_KK10;
        end
        '''

        p_str = '''
        model1 = model "repeatedStochastic"
        timecourse1 = simulate uniform_stochastic(0, 4000, 1000)
        timecourse1.algorithm.seed = 1003
        timecourse2 = simulate uniform_stochastic(0, 4000, 1000)
        task1 = run timecourse1 on model1
        task2 = run timecourse2 on model1
        repeat1 = repeat task1 for local.x in uniform(0, 10, 10), reset=true
        repeat2 = repeat task2 for local.x in uniform(0, 10, 10), reset=true
        plot "Repeats with SEED" repeat1.time vs repeat1.MAPK, repeat1.MAPK_P, repeat1.MAPK_PP, repeat1.MKK, repeat1.MKK_P, repeat1.MKKK, repeat1.MKKK_P
        plot "Repeats without SEED" repeat2.time vs repeat2.MAPK, repeat2.MAPK_P, repeat2.MAPK_PP, repeat2.MKK, repeat2.MKK_P, repeat2.MKKK, repeat2.MKKK_P
        '''
        self.run_example(a_str, p_str)


    def test_repressilator(self):

        # Get SBML from URN and set for phrasedml
        urn = "urn:miriam:biomodels.db:BIOMD0000000012"
        sbml_str = temiriam.getSBMLFromBiomodelsURN(urn=urn)
        return_code = phrasedml.setReferencedSBML(urn, sbml_str)
        assert return_code  # valid SBML

        # <SBML species>
        #   PX - LacI protein
        #   PY - TetR protein
        #   PZ - cI protein
        #   X - LacI mRNA
        #   Y - TetR mRNA
        #   Z - cI mRNA

        # <SBML parameters>
        #   ps_a - tps_active: Transcription from free promotor in transcripts per second and promotor
        #   ps_0 - tps_repr: Transcription from fully repressed promotor in transcripts per second and promotor
        phrasedml_str = """
            model1 = model "{}"
            model2 = model model1 with ps_0=1.3E-5, ps_a=0.013
            sim1 = simulate uniform(0, 1000, 1000)
            task1 = run sim1 on model1
            task2 = run sim1 on model2

            # A simple timecourse simulation
            plot "Timecourse of repressilator" task1.time vs task1.PX, task1.PZ, task1.PY

            # Applying preprocessing
            plot "Timecourse after pre-processing" task2.time vs task2.PX, task2.PZ, task2.PY

            # Applying postprocessing
            plot "Timecourse after post-processing" task1.PX/max(task1.PX) vs task1.PZ/max(task1.PZ), \
                                                               task1.PY/max(task1.PY) vs task1.PX/max(task1.PX), \
                                                               task1.PZ/max(task1.PZ) vs task1.PY/max(task1.PY)
        """.format(urn)

        # convert to sedml
        print(phrasedml_str)
        sedml_str = phrasedml.convertString(phrasedml_str)
        if sedml_str is None:
            print(phrasedml.getLastError())
            raise IOError("sedml could not be generated")

        # run SEDML directly
        try:
            tmp_dir = tempfile.mkdtemp()
            executeSEDML(sedml_str, workingDir=tmp_dir)
        finally:
            shutil.rmtree(tmp_dir)

        # create combine archive and execute
        try:
            tmp_dir = tempfile.mkdtemp()
            sedml_location = "repressilator_sedml.xml"
            sedml_path = os.path.join(tmp_dir, sedml_location)
            omex_path = os.path.join(tmp_dir, "repressilator.omex")
            with open(sedml_path, "w") as f:
                f.write(sedml_str)

            entries = [
                omex.Entry(location=sedml_location, formatKey="sedml", master=True)
            ]
            omex.combineArchiveFromEntries(omexPath=omex_path, entries=entries, workingDir=tmp_dir)
            executeCombineArchive(omex_path, workingDir=tmp_dir)
        finally:
            shutil.rmtree(tmp_dir)


    def test_simpletimecourse(self):
        a_str = '''
        // Created by libAntimony v2.9
        model MAPKcascade()

          // Compartments and Species:
          compartment compartment_;
          species MKKK in compartment_, MKKK_P in compartment_, MKK in compartment_;
          species MKK_P in compartment_, MKK_PP in compartment_, MAPK in compartment_;
          species MAPK_P in compartment_, MAPK_PP in compartment_;

          // Reactions:
          J0: MKKK => MKKK_P; (J0_V1*MKKK)/((1 + (MAPK_PP/J0_Ki)^J0_n)*(J0_K1 + MKKK));
          J1: MKKK_P => MKKK; (J1_V2*MKKK_P)/(J1_KK2 + MKKK_P);
          J2: MKK => MKK_P; (J2_k3*MKKK_P*MKK)/(J2_KK3 + MKK);
          J3: MKK_P => MKK_PP; (J3_k4*MKKK_P*MKK_P)/(J3_KK4 + MKK_P);
          J4: MKK_PP => MKK_P; (J4_V5*MKK_PP)/(J4_KK5 + MKK_PP);
          J5: MKK_P => MKK; (J5_V6*MKK_P)/(J5_KK6 + MKK_P);
          J6: MAPK => MAPK_P; (J6_k7*MKK_PP*MAPK)/(J6_KK7 + MAPK);
          J7: MAPK_P => MAPK_PP; (J7_k8*MKK_PP*MAPK_P)/(J7_KK8 + MAPK_P);
          J8: MAPK_PP => MAPK_P; (J8_V9*MAPK_PP)/(J8_KK9 + MAPK_PP);
          J9: MAPK_P => MAPK; (J9_V10*MAPK_P)/(J9_KK10 + MAPK_P);

          // Species initializations:
          MKKK = 90;
          MKKK_P = 10;
          MKK = 280;
          MKK_P = 10;
          MKK_PP = 10;
          MAPK = 280;
          MAPK_P = 10;
          MAPK_PP = 10;

          // Compartment initializations:
          compartment_ = 1;

          // Variable initializations:
          J0_V1 = 2.5;
          J0_Ki = 9;
          J0_n = 1;
          J0_K1 = 10;
          J1_V2 = 0.25;
          J1_KK2 = 8;
          J2_k3 = 0.025;
          J2_KK3 = 15;
          J3_k4 = 0.025;
          J3_KK4 = 15;
          J4_V5 = 0.75;
          J4_KK5 = 15;
          J5_V6 = 0.75;
          J5_KK6 = 15;
          J6_k7 = 0.025;
          J6_KK7 = 15;
          J7_k8 = 0.025;
          J7_KK8 = 15;
          J8_V9 = 0.5;
          J8_KK9 = 15;
          J9_V10 = 0.5;
          J9_KK10 = 15;

          // Other declarations:
          const compartment_, J0_V1, J0_Ki, J0_n, J0_K1, J1_V2, J1_KK2, J2_k3, J2_KK3;
          const J3_k4, J3_KK4, J4_V5, J4_KK5, J5_V6, J5_KK6, J6_k7, J6_KK7, J7_k8;
          const J7_KK8, J8_V9, J8_KK9, J9_V10, J9_KK10;
        end
        '''
        p_str = '''
        model1 = model "MAPKcascade"
        sim1 = simulate uniform(0,4000,1000)
        task1 = run sim1 on model1
        plot task1.time vs task1.MAPK, task1.MAPK_P, task1.MAPK_PP
        '''
        self.run_example(a_str, p_str)


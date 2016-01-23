# -*- coding: utf-8 -*-
"""
Unittests for tellurium.py
Main module for tests.
"""
# TODO: handle the plots, i.e. use the show=False option.
from __future__ import print_function, division
import unittest
import tellurium as te


class TelluriumTestCase(unittest.TestCase):

    def test_roadrunner(self):
        # load test model as SBML
        sbml = te.getTestModel('feedback.xml')
        rr = te.loadSBMLModel(sbml)
        # simulate
        s = rr.simulate(0, 100.0, 200)
        # FIXME: test plots
        # te.setHold(True)
        # te.plot(s)

        self.assertIsNotNone(rr)
        self.assertIsNotNone(s)
        self.assertEqual(s.shape[0], 200)
        self.assertEqual(s["time"][0], 0)
        self.assertAlmostEqual(s["time"][-1], 100.0)

    def test_roadrunner_tests(self):
        """ Run the roadrunner tests. """
        import roadrunner.testing
        Nfailed = roadrunner.testing.runTester()
        self.assertEqual(Nfailed, 0)

    def test_README_example(self):
        """ Tests the source example in the main README.md. """
        import tellurium as te
        rr = te.loada('''
            model example0
              S1 -> S2; k1*S1
              S1 = 10
              S2 = 0
              k1 = 0.1
            end
        ''')
        result = rr.simulate(0, 40, 500)
        # FIXME: test the plotting
        # te.plotArray(result)

    # def test_w_te_1(self):
    #     """
    #     Created on Fri Mar 14 09:46:33 2014
    #
    #     @author: mgaldzic
    #     """
    #     import tellurium as te
    #     modelStr = '''
    #     model feedback()
    #        // Reactions:
    #        J0: $X0 -> S1; (VM1 * (X0 - S1/Keq1))/(1 + X0 + S1 + S4^h);
    #        J1: S1 -> S2; (10 * S1 - 2 * S2) / (1 + S1 + S2);
    #        J2: S2 -> S3; (10 * S2 - 2 * S3) / (1 + S2 + S3);
    #        J3: S3 -> S4; (10 * S3 - 2 * S4) / (1 + S3 + S4);
    #        J4: S4 -> $X1; (V4 * S4) / (KS4 + S4);
    #
    #       // Species initializations:
    #       S1 = 0; S2 = 0; S3 = 0;
    #       S4 = 0; X0 = 10; X1 = 0;
    #
    #       // Variable initialization:
    #       VM1 = 10; Keq1 = 10; h = 10; V4 = 2.5; KS4 = 0.5;
    #     end'''
    #
    #     rr = roadrunner.RoadRunner(antStr)
    #     result = rr.simulate(0, 40, 500)
    #     te.plotWithLegend (rr, result)
    #     r = te.RoadRunner(antStr)
    #     result = r.simulate(0, 40, 500)
    #     te.plotWithLegend (r, result)
    #
    # def test_wo_te_0(self):
    #     antStr = '''
    #     model feedback()
    #        // Reactions:
    #        J0: $X0 -> S1; (VM1 * (X0 - S1/Keq1))/(1 + X0 + S1 +   S4^h);
    #        J1: S1 -> S2; (10 * S1 - 2 * S2) / (1 + S1 + S2);
    #        J2: S2 -> S3; (10 * S2 - 2 * S3) / (1 + S2 + S3);
    #        J3: S3 -> S4; (10 * S3 - 2 * S4) / (1 + S3 + S4);
    #        J4: S4 -> $X1; (V4 * S4) / (KS4 + S4);
    #
    #       // Species initializations:
    #       S1 = 0; S2 = 0; S3 = 0;
    #       S4 = 0; X0 = 10; X1 = 0;
    #
    #       // Variable initialization:
    #       VM1 = 10; Keq1 = 10; h = 10; V4 = 2.5; KS4 = 0.5;
    #     end'''
    #
    #     import libantimony
    #
    #     libantimony.loadAntimonyString (antStr)
    #     Id = libantimony.getMainModuleName()
    #     sbmlStr = libantimony.getSBMLString(Id)
    #
    #     import roadrunner
    #     r = roadrunner.RoadRunner()
    #     r.load(sbmlStr)
    #     r.simulateOptions.structuredResult = False
    #     res = r.simulate(0, 40, 500)
    #     import matplotlib.pyplot as plt
    #     plt.plot (res[:,0],res[:,1:])
    #     plt.show()

    def test_getTelluriumVersionInfo(self):
        version = te.getTelluriumVersion()
        self.assertTrue(isinstance(version, str))
        self.assertTrue(len(version) > 0)
        self.assertEqual(version, te.__version__)


if __name__ == '__main__':
    unittest.main()

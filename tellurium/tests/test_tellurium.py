# -*- coding: utf-8 -*-
"""
Unittests for tellurium.py
Main module for tests.
"""
# TODO: handle the plots, i.e. use the show=False option.
from __future__ import print_function, division
import unittest
import tellurium as te

import os
test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')


class TelluriumTestCase(unittest.TestCase):
    def setUp(self):

        self.ant_str = '''
        model pathway()
             S1 -> S2; k1*S1

             # Initialize values
             S1 = 10; S2 = 0
             k1 = 1
        end
        '''
        self.sbml_str = '''<?xml version="1.0" encoding="UTF-8"?>
        <!-- Created by libAntimony version v2.8.1 on 2016-02-02 11:45 with libSBML version 5.12.1. -->
        <sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" xmlns:comp="http://www.sbml.org/sbml/level3/version1/comp/version1" level="3" version="1" comp:required="true">
          <model id="pathway" name="pathway">
            <listOfCompartments>
              <compartment sboTerm="SBO:0000410" id="default_compartment" spatialDimensions="3" size="1" constant="true"/>
            </listOfCompartments>
            <listOfSpecies>
              <species id="S1" compartment="default_compartment" initialConcentration="10" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
              <species id="S2" compartment="default_compartment" initialConcentration="0" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
            </listOfSpecies>
            <listOfParameters>
              <parameter id="k1" value="1" constant="true"/>
            </listOfParameters>
            <listOfReactions>
              <reaction id="_J0" reversible="true" fast="false">
                <listOfReactants>
                  <speciesReference species="S1" stoichiometry="1" constant="true"/>
                </listOfReactants>
                <listOfProducts>
                  <speciesReference species="S2" stoichiometry="1" constant="true"/>
                </listOfProducts>
                <kineticLaw>
                  <math xmlns="http://www.w3.org/1998/Math/MathML">
                    <apply>
                      <times/>
                      <ci> k1 </ci>
                      <ci> S1 </ci>
                    </apply>
                  </math>
                </kineticLaw>
              </reaction>
            </listOfReactions>
          </model>
        </sbml>
        '''

        self.cellml_str = '''<?xml version="1.0"?>
        <model xmlns:cellml="http://www.cellml.org/cellml/1.1#" xmlns="http://www.cellml.org/cellml/1.1#" name="pathway">
        <component name="pathway">
        <variable initial_value="10" name="S1" units="dimensionless"/>
        <variable initial_value="0" name="S2" units="dimensionless"/>
        <variable initial_value="1" name="k1" units="dimensionless"/>
        <variable name="_J0" units="dimensionless"/>
        <math xmlns="http://www.w3.org/1998/Math/MathML">
        <apply>
        <eq/>
        <ci>_J0</ci>
        <apply>
        <times/>
        <ci>k1</ci>
        <ci>S1</ci>
        </apply>
        </apply>
        </math>
        <variable name="time" units="dimensionless"/>
        <math xmlns="http://www.w3.org/1998/Math/MathML">
        <apply>
        <eq/>
        <apply>
        <diff/>
        <bvar>
        <ci>time</ci>
        </bvar>
        <ci>S1</ci>
        </apply>
        <apply>
        <minus/>
        <ci>_J0</ci>
        </apply>
        </apply>
        </math>
        <math xmlns="http://www.w3.org/1998/Math/MathML">
        <apply>
        <eq/>
        <apply>
        <diff/>
        <bvar>
        <ci>time</ci>
        </bvar>
        <ci>S2</ci>
        </apply>
        <ci>_J0</ci>
        </apply>
        </math>
        </component>
        <group>
        <relationship_ref relationship="encapsulation"/>
        <component_ref component="pathway"/>
        </group>
        </model>
        '''

        self.ant_file = os.path.join(test_dir, 'models', 'example1')
        self.sbml_file = os.path.join(test_dir, 'models', 'example1.xml')
        self.cellml_file = os.path.join(test_dir, 'models', 'example1.cellml')

    # ---------------------------------------------------------------------
    # Loading Models Methods
    # ---------------------------------------------------------------------
    def test_loada_file(self):
        r = te.loada(self.ant_file)
        self.assertIsNotNone(r)

    def test_loada_str(self):
        r = te.loada(self.ant_str)
        self.assertIsNotNone(r)

    def loadAntimonyModel_file(self):
        r = te.loadAntimonyModel(self.ant_file)
        self.assertIsNotNone(r)

    def loadAntimonyModel_str(self):
        r = te.loadAntimonyModel(self.ant_str)
        self.assertIsNotNone(r)

    def test_loadSBMLModel_file(self):
        r = te.loadSBMLModel(self.sbml_file)
        self.assertIsNotNone(r)

    def test_loadSBMLModel_str(self):
        r = te.loadSBMLModel(self.sbml_str)
        self.assertIsNotNone(r)

    def loadCellMLModel_file(self):
        r = te.loadCellMLModel(self.cellml_file)
        self.assertIsNotNone(r)

    def loadCellMLModel_str(self):
        r = te.loadCellMLModel(self.cellml_str)
        self.assertIsNotNone(r)

    # ---------------------------------------------------------------------
    # Interconversion Methods
    # ---------------------------------------------------------------------
    def test_antimonyToSBML_file(self):
        sbml = te.antimonyToSBML(self.ant_file)
        self.assertIsNotNone(sbml)

    def test_antimonyToSBML_str(self):
        sbml = te.antimonyToSBML(self.ant_str)
        self.assertIsNotNone(sbml)

    def test_sbmlToAntimony_file(self):
        ant = te.sbmlToAntimony(self.sbml_file)
        self.assertIsNotNone(ant)

    def test_sbmlToAntimony_str(self):
        ant = te.sbmlToAntimony(self.sbml_str)
        self.assertIsNotNone(ant)

    def test_cellmlToAntimony_file(self):
        ant = te.cellmlToAntimony(self.cellml_file)
        self.assertIsNotNone(ant)

    def test_cellmlToAntimony_str(self):
        ant = te.cellmlToAntimony(self.cellml_str)
        self.assertIsNotNone(ant)

    def test_cellmlToSBML_file(self):
        sbml = te.cellmlToSBML(self.cellml_file)
        self.assertIsNotNone(sbml)

    def test_cellmlToSBML_str(self):
        sbml = te.cellmlToSBML(self.cellml_str)
        self.assertIsNotNone(sbml)

    # ---------------------------------------------------------------------
    # Roadrunner tests
    # ---------------------------------------------------------------------
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

    def test_loada(self):
        rr = te.loada('''
            model example0
              S1 -> S2; k1*S1
              S1 = 10
              S2 = 0
              k1 = 0.1
            end
        ''')
        self.assertIsNotNone(rr.getModel())

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

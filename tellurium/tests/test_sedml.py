"""
Testing tesedml.
"""
from __future__ import print_function
import unittest

import os
import tellurium.tesedml as tesedml
import tempfile

test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'testdata', 'sedml')


class tesedmlTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def single_check(self, f_sedml):
        print(f_sedml)
        python_str = tesedml.sedml_to_python(f_sedml)
        self.assertIsNotNone(python_str)

    def test_app2sim(self):
        self.single_check(os.path.join(test_dir, 'app2sim', 'app2sim.sedml'))

    def test_asedml3repeat(self):
        self.single_check(os.path.join(test_dir, 'asedml3repeat', 'asedml3repeat.sedml'))

    def test_asedmlComplex(self):
        self.single_check(os.path.join(test_dir, 'asedmlComplex', 'asedmlComplex.sedml'))

    def test_constant_maybe(self):
        self.single_check(os.path.join(test_dir, 'constant_maybe', 'BioModel1.sedml'))

    def test_via_sedml_string(self):
        sedml_string = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- Created by phraSED-ML version v0.5beta on 2016-01-31 22:02 with libSBML version 5.12.1. -->
        <sedML xmlns="http://sed-ml.org/sed-ml/level1/version2" level="1" version="2">
          <listOfSimulations>
            <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="5" numberOfPoints="100">
              <algorithm kisaoID="KISAO:0000019"/>
            </uniformTimeCourse>
          </listOfSimulations>
          <listOfModels>
            <model id="model1" language="urn:sedml:language:sbml.level-3.version-1" source="myModel"/>
          </listOfModels>
          <listOfTasks>
            <task id="task1" modelReference="model1" simulationReference="sim1"/>
          </listOfTasks>
          <listOfDataGenerators>
            <dataGenerator id="plot_0_0_0" name="time">
              <listOfVariables>
                <variable id="time" symbol="urn:sedml:symbol:time" taskReference="task1"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <ci> time </ci>
              </math>
            </dataGenerator>
            <dataGenerator id="plot_0_0_1" name="S1">
              <listOfVariables>
                <variable id="S1" target="/sbml:sbml/sbml:model/descendant::*[@id='S1']" taskReference="task1" modelReference="model1"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <ci> S1 </ci>
              </math>
            </dataGenerator>
            <dataGenerator id="plot_0_1_1" name="S2">
              <listOfVariables>
                <variable id="S2" target="/sbml:sbml/sbml:model/descendant::*[@id='S2']" taskReference="task1" modelReference="model1"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <ci> S2 </ci>
              </math>
            </dataGenerator>
          </listOfDataGenerators>
          <listOfOutputs>
            <plot2D id="plot_0" name="Figure 1">
              <listOfCurves>
                <curve logX="false" logY="false" xDataReference="plot_0_0_0" yDataReference="plot_0_0_1"/>
                <curve logX="false" logY="false" xDataReference="plot_0_0_0" yDataReference="plot_0_1_1"/>
              </listOfCurves>
            </plot2D>
          </listOfOutputs>
        </sedML>
        """
        python_str = tesedml.sedml_to_python(inputstring=sedml_string)
        self.assertIsNotNone(python_str)

if __name__ == "__main__":
    unittest.main()

"""
Testing tesedml.
"""
from __future__ import print_function

import unittest
import matplotlib
import tellurium.sedml.tesedml as tesedml


class TesedmlTestCase(unittest.TestCase):

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        self.backend = matplotlib.rcParams['backend']
        matplotlib.pyplot.switch_backend("Agg")

    def tearDown(self):
        matplotlib.pyplot.switch_backend(self.backend)

    def test_via_sedml_string(self):
        """Test SED-ML from string."""
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
        python_str = tesedml.sedmlToPython(sedml_string)
        self.assertIsNotNone(python_str)

if __name__ == "__main__":
    unittest.main()



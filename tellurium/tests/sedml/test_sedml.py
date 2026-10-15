"""
Test all the SED-ML files if code can be generated,

    test_sedml_phrasedml.py : phrasedml based tests.
    test_sedml_kisao.py : SED-ML kisao support
    test_sedml_omex.py : SED-ML tests based on Combine Archives
    test_sedml_sedml.py : sed-ml tests
"""
from __future__ import print_function, absolute_import
import unittest

import os
import matplotlib
import tellurium.sedml.tesedml as tesedml
from tellurium.tests.testdata import SEDML_TEST_DIR

from tellurium.tests.helpers import filesInDirectory

# ----------------------------------------------------------------
# List of SED-ML files to test
# ----------------------------------------------------------------
sedml_files = filesInDirectory(SEDML_TEST_DIR, suffix='.sedml')


# ----------------------------------------------------------------
# Test class
# ----------------------------------------------------------------
class SEDMLTestCase(unittest.TestCase):

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        self.backend = matplotlib.rcParams['backend']
        matplotlib.pyplot.switch_backend("Agg")

    def tearDown(self):
        matplotlib.pyplot.switch_backend(self.backend)

    def single_check(self, f_sedml):
        """ Test if python code can be generated from the
        SED-ML file.

        :param f_sedml:
        :type f_sedml:
        :return:
        :rtype:
        """
        directory = os.path.dirname(f_sedml)
        basename = os.path.basename(f_sedml)
        dir_results = os.path.join(directory, 'results')

        python_str = tesedml.sedmlToPython(f_sedml)
        
        self.assertIsNotNone(python_str)
        # create the python code file

        if not os.path.exists(dir_results):
            os.mkdir(dir_results)

        file_py = os.path.join(dir_results, basename + '.py')
        with open(file_py, 'w') as f_py:
            f_py.write(python_str)


    # TODO: run single_check for all sedml files !

    def test_app2sim(self):
        """Test app2sim SED-ML example."""
        self.single_check(os.path.join(SEDML_TEST_DIR, 'app2sim.sedml'))

    def test_asedml3repeat(self):
        """Test asedml3repeat SED-ML example."""
        self.single_check(os.path.join(SEDML_TEST_DIR, 'asedml3repeat.sedml'))

    def test_asedmlComplex(self):
        """Test asedmlComplex SED-ML example."""
        self.single_check(os.path.join(SEDML_TEST_DIR, 'asedmlComplex.sedml'))

    def test_constant_maybe(self):
        """Test constant_maybe SED-ML example."""
        self.single_check(os.path.join(SEDML_TEST_DIR, 'BioModel1_repressor_activator_oscillations.sedml'))

    def test_repeated_task_preserves_standalone_subtask_issue_603(self):
        """Regression test for Issue #603: a standalone uniformTimeCourse task
        that is also used as a subtask of a repeatedTask (including a nested
        repeatedTask) must retain its own standalone output."""
        import numpy as np
        from tellurium.tests.testdata import FEEDBACK_SBML

        working_dir = os.path.dirname(FEEDBACK_SBML)
        sedml_str = """<?xml version="1.0" encoding="UTF-8"?>
        <sedML xmlns="http://sed-ml.org/sed-ml/level1/version4" level="1" version="4">
          <listOfModels>
            <model id="model" language="urn:sedml:language:sbml" source="feedback.xml"/>
          </listOfModels>
          <listOfSimulations>
            <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="2" numberOfSteps="10">
              <algorithm kisaoID="KISAO:0000019"/>
            </uniformTimeCourse>
          </listOfSimulations>
          <listOfTasks>
            <task id="task1" modelReference="model" simulationReference="sim1"/>
            <repeatedTask id="inner_rep" range="r_in" resetModel="true">
              <listOfRanges>
                <vectorRange id="r_in">
                  <value> 2.0 </value>
                  <value> 4.0 </value>
                </vectorRange>
              </listOfRanges>
              <listOfChanges>
                <setValue modelReference="model" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" range="r_in">
                  <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> r_in </ci></math>
                </setValue>
              </listOfChanges>
              <listOfSubTasks>
                <subTask order="1" task="task1"/>
              </listOfSubTasks>
            </repeatedTask>
            <repeatedTask id="outer_rep" range="r_out" resetModel="true">
              <listOfRanges>
                <vectorRange id="r_out">
                  <value> 6.0 </value>
                  <value> 8.0 </value>
                </vectorRange>
              </listOfRanges>
              <listOfChanges>
                <setValue modelReference="model" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S2']" range="r_out">
                  <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> r_out </ci></math>
                </setValue>
              </listOfChanges>
              <listOfSubTasks>
                <subTask order="1" task="inner_rep"/>
              </listOfSubTasks>
            </repeatedTask>
          </listOfTasks>
          <listOfDataGenerators>
            <dataGenerator id="dg_s1_single">
              <listOfVariables>
                <variable id="v_s1" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" taskReference="task1" modelReference="model"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> v_s1 </ci></math>
            </dataGenerator>
            <dataGenerator id="dg_s2_inner">
              <listOfVariables>
                <variable id="v_s2_in" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S2']" taskReference="inner_rep" modelReference="model"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> v_s2_in </ci></math>
            </dataGenerator>
            <dataGenerator id="dg_s2_outer">
              <listOfVariables>
                <variable id="v_s2_out" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S2']" taskReference="outer_rep" modelReference="model"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> v_s2_out </ci></math>
            </dataGenerator>
          </listOfDataGenerators>
        </sedML>
        """
        factory = tesedml.SEDMLCodeFactory(
            sedml_str, workingDir=working_dir, createOutputs=False, saveOutputs=False
        )
        res = factory.executePython()["dataGenerators"]
        self.assertEqual(res["dg_s1_single"].shape, (11, 1))
        self.assertAlmostEqual(float(res["dg_s1_single"][0, 0]), 0.0)
        self.assertEqual(res["dg_s2_inner"].shape, (11, 2))
        self.assertTrue(np.allclose(res["dg_s2_inner"][0, :], [0.0, 0.0]))
        self.assertEqual(res["dg_s2_outer"].shape, (11, 4))
        self.assertTrue(np.allclose(res["dg_s2_outer"][0, :], [6.0, 6.0, 8.0, 8.0]))

    def test_repeated_task_subtask_id_collision_issue_603(self):
        """Guard for the __subtask__ naming scheme: ensure internal subtask
        variable allocation does not collide when a SED-ML repeatedTask or CSV
        dataSource uses id='__subtask__task1'."""
        import shutil
        import tempfile
        import numpy as np
        from tellurium.tests.testdata import FEEDBACK_SBML

        with tempfile.TemporaryDirectory() as tmp_dir:
            shutil.copy(FEEDBACK_SBML, os.path.join(tmp_dir, "feedback.xml"))
            with open(os.path.join(tmp_dir, "observations.csv"), "w") as f:
                f.write("measurement\n11\n22\n")

            sedml_str = """<?xml version="1.0" encoding="UTF-8"?>
            <sedML xmlns="http://sed-ml.org/sed-ml/level1/version4" level="1" version="4">
              <listOfDataDescriptions>
                <dataDescription id="observations" source="observations.csv" format="urn:sedml:format:csv">
                  <listOfDataSources>
                    <dataSource id="__subtask__task1">
                      <listOfSlices>
                        <slice reference="ColumnIds" value="measurement"/>
                      </listOfSlices>
                    </dataSource>
                  </listOfDataSources>
                </dataDescription>
              </listOfDataDescriptions>
              <listOfModels>
                <model id="model" language="urn:sedml:language:sbml" source="feedback.xml"/>
              </listOfModels>
              <listOfSimulations>
                <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="1" numberOfSteps="5">
                  <algorithm kisaoID="KISAO:0000019"/>
                </uniformTimeCourse>
              </listOfSimulations>
              <listOfTasks>
                <task id="task1" modelReference="model" simulationReference="sim1"/>
                <repeatedTask id="__subtask_1__task1" range="r1" resetModel="true">
                  <listOfRanges>
                    <vectorRange id="r1">
                      <value> 1.5 </value>
                      <value> 3.5 </value>
                    </vectorRange>
                  </listOfRanges>
                  <listOfChanges>
                    <setValue modelReference="model" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" range="r1">
                      <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> r1 </ci></math>
                    </setValue>
                  </listOfChanges>
                  <listOfSubTasks>
                    <subTask order="1" task="task1"/>
                  </listOfSubTasks>
                </repeatedTask>
              </listOfTasks>
              <listOfDataGenerators>
                <dataGenerator id="dg_scan">
                  <listOfVariables>
                    <variable id="v_s1" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" taskReference="__subtask_1__task1" modelReference="model"/>
                  </listOfVariables>
                  <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> v_s1 </ci></math>
                </dataGenerator>
                <dataGenerator id="dg_csv">
                  <listOfVariables>
                    <variable id="csv_val" target="#__subtask__task1" modelReference="model"/>
                  </listOfVariables>
                  <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> csv_val </ci></math>
                </dataGenerator>
              </listOfDataGenerators>
            </sedML>
            """
            factory = tesedml.SEDMLCodeFactory(
                sedml_str, workingDir=tmp_dir, createOutputs=False, saveOutputs=False
            )
            res = factory.executePython()["dataGenerators"]
            self.assertEqual(res["dg_scan"].shape, (6, 2))
            self.assertTrue(np.allclose(res["dg_scan"][0, :], [1.5, 3.5]))
            self.assertIsInstance(res["dg_csv"], np.ndarray)
            self.assertEqual(res["dg_csv"].shape, (2, 1))
            self.assertTrue(np.allclose(res["dg_csv"], [[11.0], [22.0]]))

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

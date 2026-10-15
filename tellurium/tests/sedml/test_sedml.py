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
import numpy as np
import tellurium.sedml.tesedml as tesedml
from tellurium.tests.testdata import SEDML_TEST_DIR, FEEDBACK_SBML

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

    def test_change_attribute_reordering_issue_604(self):
        """Regression test for Issue #604: reordering <changeAttribute> of
        parameters vs. species must not reset parameter changes."""
        working_dir = os.path.dirname(FEEDBACK_SBML)
        sedml_template = """<?xml version="1.0" encoding="UTF-8"?>
        <sedML xmlns="http://sed-ml.org/sed-ml/level1/version4" level="1" version="4">
          <listOfModels>
            <model id="model" language="urn:sedml:language:sbml" source="feedback.xml">
              <listOfChanges>
                {changes}
              </listOfChanges>
            </model>
          </listOfModels>
          <listOfSimulations>
            <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="10" numberOfSteps="20">
              <algorithm kisaoID="KISAO:0000019"/>
            </uniformTimeCourse>
          </listOfSimulations>
          <listOfTasks>
            <task id="task1" modelReference="model" simulationReference="sim1"/>
          </listOfTasks>
          <listOfDataGenerators>
            <dataGenerator id="dg_s1">
              <listOfVariables>
                <variable id="S1" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" taskReference="task1" modelReference="model"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> S1 </ci></math>
            </dataGenerator>
          </listOfDataGenerators>
        </sedML>
        """
        c_s1 = '<changeAttribute target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id=\'S1\']/@initialConcentration" newValue="1.0"/>'
        c_s2 = '<changeAttribute target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id=\'S2\']/@initialConcentration" newValue="2.0"/>'
        c_vm1 = '<changeAttribute target="/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id=\'J0_VM1\']/@value" newValue="2.5"/>'

        sedml_param_last = sedml_template.format(changes="\n".join([c_s1, c_s2, c_vm1]))
        sedml_param_middle = sedml_template.format(changes="\n".join([c_s1, c_vm1, c_s2]))

        results = []
        for sedml_str in (sedml_param_last, sedml_param_middle):
            factory = tesedml.SEDMLCodeFactory(
                sedml_str, workingDir=working_dir, createOutputs=False, saveOutputs=False
            )
            py_code = factory.toPython()
            self.assertIn("model['init(J0_VM1)'] = 2.5", py_code)
            ns = {}
            exec(compile(py_code, "<sedml_604>", "exec"), ns)
            self.assertAlmostEqual(ns["model"]["J0_VM1"], 2.5)
            results.append(ns["task1"][0])

        self.assertTrue(np.allclose(results[0], results[1]))

    def test_compute_change_and_repeated_task_issue_604(self):
        """Ensure <computeChange> uses init(...) so subsequent species changes do not
        reset it, while <repeatedTask resetModel="false"> <setValue> uses runtime
        assignment and preserves continuous state across steps."""
        working_dir = os.path.dirname(FEEDBACK_SBML)
        sedml_compute_template = """<?xml version="1.0" encoding="UTF-8"?>
        <sedML xmlns="http://sed-ml.org/sed-ml/level1/version4" level="1" version="4">
          <listOfModels>
            <model id="model" language="urn:sedml:language:sbml" source="feedback.xml">
              <listOfChanges>
                {changes}
              </listOfChanges>
            </model>
          </listOfModels>
          <listOfSimulations>
            <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="10" numberOfSteps="20">
              <algorithm kisaoID="KISAO:0000019"/>
            </uniformTimeCourse>
          </listOfSimulations>
          <listOfTasks>
            <task id="task1" modelReference="model" simulationReference="sim1"/>
          </listOfTasks>
          <listOfDataGenerators>
            <dataGenerator id="dg_s1">
              <listOfVariables>
                <variable id="S1" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" taskReference="task1" modelReference="model"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> S1 </ci></math>
            </dataGenerator>
          </listOfDataGenerators>
        </sedML>
        """
        comp_vm1 = """
        <computeChange target="/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='J0_VM1']/@value">
          <listOfVariables>
            <variable id="v_vm1" target="/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='J0_VM1']/@value" modelReference="model"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply><times/><cn> 0.25 </cn><ci> v_vm1 </ci></apply>
          </math>
        </computeChange>
        """
        c_s2 = '<changeAttribute target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id=\'S2\']/@initialConcentration" newValue="2.0"/>'

        comp_results = []
        for changes_str in (comp_vm1 + "\n" + c_s2, c_s2 + "\n" + comp_vm1):
            factory = tesedml.SEDMLCodeFactory(
                sedml_compute_template.format(changes=changes_str),
                workingDir=working_dir,
                createOutputs=False,
                saveOutputs=False,
            )
            py_code = factory.toPython()
            self.assertIn("model['init(J0_VM1)'] =", py_code)
            ns = {}
            exec(compile(py_code, "<sedml_604_comp>", "exec"), ns)
            self.assertAlmostEqual(ns["model"]["J0_VM1"], 2.5)
            comp_results.append(ns["task1"][0])

        self.assertTrue(np.allclose(comp_results[0], comp_results[1]))

        sedml_repeated = """<?xml version="1.0" encoding="UTF-8"?>
        <sedML xmlns="http://sed-ml.org/sed-ml/level1/version4" level="1" version="4">
          <listOfModels>
            <model id="model" language="urn:sedml:language:sbml" source="feedback.xml"/>
          </listOfModels>
          <listOfSimulations>
            <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="2" numberOfSteps="5">
              <algorithm kisaoID="KISAO:0000019"/>
            </uniformTimeCourse>
          </listOfSimulations>
          <listOfTasks>
            <task id="task1" modelReference="model" simulationReference="sim1"/>
            <repeatedTask id="rt1" range="r1" resetModel="false">
              <listOfRanges>
                <vectorRange id="r1">
                  <value> 5.0 </value>
                  <value> 2.5 </value>
                </vectorRange>
              </listOfRanges>
              <listOfChanges>
                <setValue modelReference="model" target="/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='J0_VM1']/@value" range="r1">
                  <math xmlns="http://www.w3.org/1998/Math/MathML">
                    <ci> r1 </ci>
                  </math>
                </setValue>
              </listOfChanges>
              <listOfSubTasks>
                <subTask order="1" task="task1"/>
              </listOfSubTasks>
            </repeatedTask>
          </listOfTasks>
          <listOfDataGenerators>
            <dataGenerator id="dg_rt_s1">
              <listOfVariables>
                <variable id="S1" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" taskReference="rt1" modelReference="model"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML"><ci> S1 </ci></math>
            </dataGenerator>
          </listOfDataGenerators>
        </sedML>
        """
        rt_factory = tesedml.SEDMLCodeFactory(
            sedml_repeated, workingDir=working_dir, createOutputs=False, saveOutputs=False
        )
        rt_code = rt_factory.toPython()
        self.assertIn("model['J0_VM1'] =", rt_code)
        self.assertNotIn("model['init(J0_VM1)'] =", rt_code)
        rt_ns = {}
        exec(compile(rt_code, "<sedml_604_rt>", "exec"), rt_ns)
        step0, step1 = rt_ns["rt1"][0], rt_ns["rt1"][1]
        self.assertEqual(step0.colnames, ["[S1]"])
        self.assertEqual(step1.colnames, ["[S1]"])
        self.assertGreater(np.ptp(step0["[S1]"]), 0.0)
        self.assertTrue(np.allclose(step0["[S1]"][-1], step1["[S1]"][0]))


if __name__ == "__main__":
    unittest.main()

"""
Test all the SED-ML files if code can be generated,

    test_phrasedml.py : phrasedml based tests.
    test_kisao.py : SED-ML kisao support
    test_omex.py : SED-ML tests based on Combine Archives
    test_tesedml.py : tests for the `tesedml.py` module
"""
from __future__ import print_function, absolute_import
import unittest

import os
import matplotlib
import tellurium.sedml.tesedml as tesedml
from tellurium.tests.testdata import sedmlDir

from tellurium.tests.helpers import filesInDirectory

# ----------------------------------------------------------------
# List of SED-ML files to test
# ----------------------------------------------------------------
sedml_files = filesInDirectory(sedmlDir, suffix='.sedml')

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
        self.single_check(os.path.join(sedmlDir, 'app2sim.sedml'))

    def test_asedml3repeat(self):
        """Test asedml3repeat SED-ML example."""
        self.single_check(os.path.join(sedmlDir, 'asedml3repeat.sedml'))

    def test_asedmlComplex(self):
        """Test asedmlComplex SED-ML example."""
        self.single_check(os.path.join(sedmlDir, 'asedmlComplex.sedml'))

    def test_constant_maybe(self):
        """Test constant_maybe SED-ML example."""
        self.single_check(os.path.join(sedmlDir, 'BioModel1_repressor_activator_oscillations.sedml'))


# ----------------------------------------------------------------
# Dynamic generation of tests from python files
# # ----------------------------------------------------------------
# def ftest_generator(filePath):
#     def test(self=None):
#         """ Test failes if Exception in execution of f. """
#         if self is not None:
#             print(filePath)
#             imp.load_source(os.path.basename(filePath)[:-3], filePath)
#     return test
#
# for k, f in enumerate(py_files):
#     test_name = 'test_{:03d}_{}'.format(k, os.path.basename(f)[:-3])
#     test_name = test_name.replace('.', '_')
#     test = ftest_generator(f)
#     setattr(PythonExampleTestCase, test_name, test)
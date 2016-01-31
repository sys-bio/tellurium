"""
Testing tesedml.
"""
from __future__ import print_function
import unittest

import os
import tellurium.SedmlToRr as tesedml
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


if __name__ == "__main__":
    unittest.main()

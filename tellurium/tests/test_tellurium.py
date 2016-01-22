"""
Test tellurium.py
"""
from __future__ import print_function, division
import matplotlib
matplotlib.use('Agg')

import unittest
import tellurium as te



class TelluriumTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_README_example(self):
        """ Testing the README example. """
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
        te.plotArray(result)

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


if __name__ == '__main__':
    unittest.main()

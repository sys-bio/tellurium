"""
Testing temiriam module
"""
from __future__ import print_function, absolute_import
import unittest
from six import string_types
import roadrunner
from tellurium import temiriam


class TemiriamTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getSBMLFromBiomodelsURN1(self):
        """ Check that string is returned.

        :return:
        """
        urn = 'urn:miriam:biomodels.db:BIOMD0000000139'
        sbml = temiriam.getSBMLFromBiomodelsURN(urn)
        self.assertIsNotNone(sbml)
        # check that string
        self.assertTrue(isinstance(sbml, string_types))

    def test_getSBMLFromBiomodelsURN1(self):
        """ Check that model can be loaded in roadrunner.

        :return:
        """
        urn = 'urn:miriam:biomodels.db:BIOMD0000000139'
        sbml = temiriam.getSBMLFromBiomodelsURN(urn)

        print("*" * 80)
        print(type(sbml))
        print("*" * 80)
        print(sbml)
        print("*" * 80)

        r = roadrunner.RoadRunner(sbml)
        self.assertIsNotNone(r)


if __name__ == "__main__":
    unittest.main()
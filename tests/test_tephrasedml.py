"""
Testing tephrasedml.
"""
import unittest

import tellurium.tephrasedml as tephrasedml


@unittest.skipIf(tephrasedml.phrasedml is None, "only run tests if phrasedml is available")
class tePhrasedMLTestCase(unittest.TestCase):

    def setUp(self):
        # create a test instance
        self.antimonyStr = '''

        '''
        self.phrasedmlStr = '''

        '''
        self.tep = tephrasedml.tePhrasedml(self.antimonyStr, self.phrasedmlStr)

        self.tep.getSbmlString()
        self.tep.getSedmlString()

    def tearDown(self):
        self.tep = None

    def test_getAntimonyString(self):
        astr = self.tep.getAntimonyString()
        self.assertNotNone(astr)
        self.assertEqual(self.antimonyStr, astr)

    def test_getPhrasedmlString(self):
        pstr = self.tep.getPhrasedmlString()
        self.assertNotNone(pstr)
        self.assertEqual(self.phrasedmlStr, pstr)

    def test_getSbmlString(self):
        sstr = self.tep.getSbmlString()
        self.assertNotNone(sstr)

    def test_getSedmlString(self):
        sstr = self.tep.getSedmlString()
        self.assertNotNone(sstr)

    def test_execute(self):
        self.assertEqual(True, False)

    def test_createpython(self):
        self.assertEqual(True, False)

    def test_printpython(self):
        self.assertEqual(True, False)

    @unittest.skipIf(tephrasedml.combine is None, "only run tests if combine is available")
    def test_exportAsCombine(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()

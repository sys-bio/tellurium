"""
Testing tephrasedml.
"""
from __future__ import print_function
import unittest
import tellurium.tephrasedml as tephrasedml
import tempfile


@unittest.skipIf(tephrasedml.phrasedml is None, "only run tests if phrasedml is available")
class tePhrasedMLTestCase(unittest.TestCase):

    def setUp(self):
        # create a test instance
        self.antimony = '''
        model myModel
          S1 -> S2; k1*S1
          S1 = 10; S2 = 0
          k1 = 1
        end
        '''
        self.phrasedml = '''
          model1 = model "myModel"
          sim1 = simulate uniform(0, 5, 100)
          task1 = run sim1 on model1
          plot "Figure 1" time vs S1, S2
        '''
        self.tep = tephrasedml.tePhrasedml(self.antimony, self.phrasedml)

        self.tep.getSbmlString()
        self.tep.getSedmlString()

    def tearDown(self):
        self.tep = None

    def test_getAntimonyString(self):
        astr = self.tep.getAntimonyString()
        self.assertIsNotNone(astr)
        self.assertEqual(self.antimony, astr)

    def test_getPhrasedmlString(self):
        pstr = self.tep.getPhrasedmlString()
        self.assertIsNotNone(pstr)
        self.assertEqual(self.phrasedml, pstr)

    def test_getSbmlString(self):
        sstr = self.tep.getSbmlString()
        self.assertIsNotNone(sstr)

    def test_getSedmlString(self):
        sstr = self.tep.getSedmlString()
        self.assertIsNotNone(sstr)

    def test_execute(self):
        exp = tephrasedml.tePhrasedml(self.antimony, self.phrasedml)
        # FIXME: handle plots in tests
        # exp.execute()

    def test_createpython(self):
        exp = tephrasedml.tePhrasedml(self.antimony, self.phrasedml)
        pstr = exp.createpython()
        self.assertIsNotNone(pstr)

    def test_printpython(self):
        exp = tephrasedml.tePhrasedml(self.antimony, self.phrasedml)
        exp.printpython()

    def test_experiment(self):
        import tellurium as te
        exp = te.experiment(self.antimony, self.phrasedml)
        pstr = exp.createpython()
        self.assertIsNotNone(pstr)

    def test_exportAsCombine(self):
        import tellurium as te
        exp = te.experiment(self.antimony, self.phrasedml)
        f = tempfile.NamedTemporaryFile()
        exp.exportAsCombine(f.name)
        # try to re
        import zipfile
        zip=zipfile.ZipFile(f.name)


if __name__ == '__main__':
    unittest.main()

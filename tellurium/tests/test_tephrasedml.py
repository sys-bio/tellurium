"""
Testing tephrasedml.
"""
from __future__ import print_function

import tempfile
import unittest

import tellurium.sedml.tephrasedml as tephrasedml


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
<<<<<<< HEAD
        self.tep = tephrasedml.experiment(self.antimony, self.phrasedml)

        self.tep.getSbmlString()
        self.tep.getSedmlString()
=======
        self.tep = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])
>>>>>>> master

    def tearDown(self):
        self.tep = None

    def test_execute(self):
        """Test execute."""
<<<<<<< HEAD
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        exp.execute()

    def test_createpython(self):
        """Test createpython."""
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        pstr = exp.createpython()
=======
        exp = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])
        exp.execute(self.phrasedml)

    def test_createpython(self):
        """Test createpython."""
        exp = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])
        pstr = exp.createpython(self.phrasedml)
>>>>>>> master
        self.assertIsNotNone(pstr)

    def test_printpython(self):
        """Test printpython."""
<<<<<<< HEAD
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        exp.printpython()
=======
        exp = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])
        exp.printpython(self.phrasedml)
>>>>>>> master

    def test_experiment(self):
        """Test experiment."""
        import tellurium as te
<<<<<<< HEAD
        exp = tephrasedml.experiment(self.antimony, self.phrasedml)
        pstr = exp.createpython()
=======
        exp = te.experiment([self.antimony], [self.phrasedml])
        pstr = exp.createpython(self.phrasedml)
>>>>>>> master
        self.assertIsNotNone(pstr)

    def test_exportAsCombine(self):
        """Test exportAsCombine."""
        import tellurium as te
        import os
        exp = te.experiment([self.antimony], [self.phrasedml])
        tmpdir = tempfile.mkdtemp()
        tmparchive = os.path.join(tmpdir, 'test.zip')
        exp.exportAsCombine(tmparchive)
        # try to re
        import zipfile
        zip = zipfile.ZipFile(tmparchive)


if __name__ == '__main__':
    unittest.main()

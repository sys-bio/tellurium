"""
Testing tephrasedml.
"""
from __future__ import print_function
import unittest
import tellurium.tephrasedml as tephrasedml
import tempfile
import tellurium as te
import os
import shutil


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
        self.tep = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])

    def tearDown(self):
        self.tep = None

    def test_execute(self):
        """Test execute."""
        exp = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])
        exp.execute(self.phrasedml)

    def test_createpython(self):
        """Test createpython."""
        exp = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])
        pstr = exp.createpython(self.phrasedml)
        self.assertIsNotNone(pstr)

    def test_printpython(self):
        """Test printpython."""
        exp = tephrasedml.tePhrasedml([self.antimony], [self.phrasedml])
        exp.printpython(self.phrasedml)

    def test_experiment(self):
        """Test experiment."""
        import tellurium as te
        exp = te.experiment([self.antimony], [self.phrasedml])
        pstr = exp.createpython(self.phrasedml)
        self.assertIsNotNone(pstr)

    def test_exportAsCombine(self):
        """Test exportAsCombine."""
        exp = te.experiment([self.antimony], [self.phrasedml])
        tmpdir = tempfile.mkdtemp()
        tmparchive = os.path.join(tmpdir, 'test.zip')
        exp.exportAsCombine(tmparchive)
        # try to re
        import zipfile
        zip = zipfile.ZipFile(tmparchive)
        zip.close()
        shutil.rmtree(tmpdir)
        
    def test_update(self):
        """Test update."""
        exp = te.experiment([self.antimony], [self.phrasedml])
        tmpdir = tempfile.mkdtemp()
        tmparchive = os.path.join(tmpdir, 'test.zip')
        exp.exportAsCombine(tmparchive)
        exp.update(tmparchive)
        # try to re
        import zipfile
        zip = zipfile.ZipFile(tmparchive)
        zip.close()
        shutil.rmtree(tmpdir)


if __name__ == '__main__':
    unittest.main()

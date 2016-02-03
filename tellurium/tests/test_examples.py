"""
Unittests for examples.
All examples are executed to check against latest code base.
"""
from __future__ import print_function, division
import unittest
import tellurium as te

import os
examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'examples')


class ExamplesTestCase(unittest.TestCase):
    def _pyFilesInFolder(self, dir):
        from os import walk
        files = []
        for (dirpath, dirnames, filenames) in walk(dir):
            files.extend([os.path.join(dirpath, name) for name in filenames])
        return [f for f in files if f.endswith('.py')]


    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        import matplotlib
        matplotlib.pyplot.switch_backend("Agg")

    def testTelluriumExamples(self):
        tedir = os.path.join(examples_dir, 'tellurium-files')
        py_files = self._pyFilesInFolder(tedir)

        import imp
        for f in py_files:
            print(f)
            imp.load_source(os.path.basename(f)[:-3], f)

    def testNotebookExamples(self):
        notebookdir = os.path.join(examples_dir, 'notebooks-py')
        py_files = self._pyFilesInFolder(notebookdir)

        import imp
        for f in py_files:
            print(f)
            imp.load_source(os.path.basename(f)[:-3], f)

        self.assertEqual(0, 1)


if __name__ == '__main__':
    unittest.main()

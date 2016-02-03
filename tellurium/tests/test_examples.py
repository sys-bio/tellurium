"""
Unittests for examples.
All examples are executed to check against latest code base.
"""
from __future__ import print_function, division
import unittest

import os
import imp
examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'examples')

def _pyFilesInFolder(dir):
    from os import walk
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend([os.path.join(dirpath, name) for name in filenames])
    return [f for f in files if f.endswith('.py')]


class ExamplesTestCase(unittest.TestCase):

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        import matplotlib
        matplotlib.pyplot.switch_backend("Agg")

    def test_python_example(self):
        tedir = os.path.join(examples_dir, 'tellurium-files')
        py_files = _pyFilesInFolder(tedir)
        for f in py_files:
            yield self.check_pyfile, f

    def test_notebook_example(self):
        notebookdir = os.path.join(examples_dir, 'notebooks-py')
        py_files = _pyFilesInFolder(notebookdir)
        for f in py_files:
            yield self.check_pyfile, f

    def check_pyfile(self, f):
        """ Test failes if Exception in execution of f.
        :param f:
        :type f:
        """
        print(f)
        imp.load_source(os.path.basename(f)[:-3], f)


if __name__ == '__main__':
    unittest.main()

"""
Test utilities for tellurium.
"""
from __future__ import print_function, division
import unittest
import fnmatch
import os

# test directory is the directory of this module
test_dir = os.path.dirname(os.path.abspath(__file__))


class TestRunner(object):
    """
    Test modules have the pattern `test_*.py`
    and must be located in the directory of this module.
    """
    def __init__(self):
        self.results = None

    @staticmethod
    def find_test_modules():
        matches = []
        for root, dirnames, filenames in os.walk(test_dir):
            for filename in fnmatch.filter(filenames, 'test_*.py'):
                # matches.append(os.path.join(root, filename))
                matches.append(filename[:-3])

        return ['tellurium.tests.{}'.format(mstr) for mstr in matches]


    @staticmethod
    def run_all():
        """ Run all unittests of tellurium.

        :return: results of unittest
        :rtype: unittest.TextTestResult
        """
        # get the test modules and add to test suite
        modules = TestRunner.find_test_modules()

        print(modules)
        suites = [unittest.defaultTestLoader.loadTestsFromName(s) for s in modules]
        testSuite = unittest.TestSuite(suites)
        return unittest.TextTestRunner(verbosity=2).run(testSuite)

    def te_passes_tests(self):
        """ Did tellurium pass the tests?
        ::
            import tellurium.tests.test_runner as tetest
            runner = tetest.TestRunner()
            runner.te_passes_tests()

        :return: True if passed
        :rtype: bool
        """
        # run tests if no test results
        if self.results is None:
            self.results = TestRunner.run_all()
        print(self.results)
        return len(self.results.errors) + len(self.results.failures) == 0


if __name__ == "__main__":
    test_runner = TestRunner()
    print("tellurium passes tests: ", test_runner.te_passes_tests())

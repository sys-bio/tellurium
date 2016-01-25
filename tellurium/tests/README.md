# unit tests for tellurium
Tests are implemented with `nose` and `coverage` and are available in the tests folder `tellurium/tests`.
The requirements can be installed via
```
pip install nose coverage 
```
## Run tests
### tellurium
To run the test suite in tellurium do
```{python}
import tellurium.tests.test_runner as tetest
runner = tetest.TestRunner()
runner.te_passes_tests()
```
which returns `True` if all tests passed.

### console
Tests are run in the `tellurium/tests` folder and can be executed on the console via
```
nosetests
```
If all tests passed you see a message
```
----------------------------------------------------------------------
Ran 4 tests in 1.534s

OK
```

To run the tests with a coverage report use
```{shell}
nosetests --with-coverage --cover-erase --cover-package=tellurium
# coverage report
firefox cover/index.html
```

## Add test
To add a test write a test function in one of the `tests/test_*.py` modules. Assert the test results with the `assert*` functions.
``` {python}
    def test_roadrunner(self):
        sbml = te.getTestModel('feedback.xml')
        rr = te.loadSBMLModel(sbml)
        s = rr.simulate(0, 100.0, 200)

        self.assertIsNotNone(rr)
        self.assertIsNotNone(s)
        self.assertEqual(s.shape[0], 200)
        self.assertEqual(s["time"][0], 0)
        self.assertAlmostEqual(s["time"][-1], 100.0)
```

## Open issues
* plot suppression of ipython (if test plots results the tests are interrupted)
* webhook for automatically running tests on commit

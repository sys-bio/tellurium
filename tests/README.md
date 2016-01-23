# tests for tellurium
Unit tests for tellurium. To add a test write a test function in one of 
the `tests/test_*.py` modules. Assert the test results with the `assert*` functions.

## Run tests
Tests are run with coverage using `nose` and `coverage` in the tests folder `tellurium/tests`.
```
pip install nose coverage 
```
Tests should be run in the `tests` folder.
**run tests**
```
nosetest
```
**run tests with coverage**
A shell script is available which runs the tests `run_tests.sh`
```
nosetests --with-coverage --cover-erase --cover-package=tellurium
# coverage report
firefox cover/index.html
```

## Open issues
* plot suppression of ipython (if test plots results the tests are interrupted)
* webhook for automatically running tests on commit

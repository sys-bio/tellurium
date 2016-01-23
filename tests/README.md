# unit tests for tellurium
Tests are implemented with `nose` and `coverage` and are available in the tests folder `tellurium/tests`.
The requirements can be installed via
```
pip install nose coverage 
```
## Run tests
Tests should be run in the `tellurium/tests` folder and can be executed via
```
nosetest
```
If all tests passed you see a message
```
----------------------------------------------------------------------
Ran 4 tests in 1.534s

OK
```

To run the tests with a coverage report use
```
nosetests --with-coverage --cover-erase --cover-package=tellurium
# coverage report
firefox cover/index.html
```

## Add test
To add a test write a test function in one of the `tests/test_*.py` modules. Assert the test results with the `assert*` functions.


## Open issues
* plot suppression of ipython (if test plots results the tests are interrupted)
* webhook for automatically running tests on commit

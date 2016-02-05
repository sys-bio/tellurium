#!/bin/bash
############################################################
# Run all the unittests in the tests subdirectory
# and create coverage report.
#
# Usage: 
#	./run_tests.sh 2>&1 | tee ./run_tests.log
#
############################################################
nosetests --with-coverage --cover-erase --cover-inclusive --cover-package=../../tellurium --cover-html

# coverage report
firefox cover/index.html

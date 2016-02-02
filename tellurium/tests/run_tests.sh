#!/bin/bash
############################################################
# Run all the unittests in the tests subdirectory
# and create coverage report.
############################################################
nosetests --with-coverage --cover-erase --cover-inclusive --cover-package=../../tellurium --cover-html

# coverage report
firefox cover/index.html

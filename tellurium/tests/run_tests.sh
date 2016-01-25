#!/bin/bash
############################################################
# Run all the unittests in the tests subdirectory
############################################################
nosetests --with-coverage --cover-erase --cover-package=tellurium --cover-html
# coverage report
firefox cover/index.html

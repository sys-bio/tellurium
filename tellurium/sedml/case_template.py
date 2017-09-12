"""
Template functions to run the example cases.
"""
from __future__ import print_function
import tellurium as te
from tellurium.sedml.tephrasedml import experiment
import os


def run_case(call_file, antimonyStr, phrasedmlStr, py_code=True):
    """ Run one of the example phrasedml cases.

    :param case_id:
    :param antimonyStr:
    :param phrasedmlStr:
    :return:
    """
    # phrasedml experiment
    exp = experiment(antimonyStr, phrasedmlStr)

    # output dir relative to call file
    workingDir = os.path.join(os.path.dirname(call_file), './results')
    if not os.path.exists(workingDir):
        os.makedirs(workingDir)

    # write python code

    if py_code:
        fname = os.path.basename(call_file)
        py_file = os.path.join(workingDir, fname + 'code.py')
        print(py_file)
        with open(py_file, 'w') as f:
            f.write(exp._toPython(phrasedmlStr, workingDir=workingDir))

    # execute python
    exp.execute(phrasedmlStr, workingDir=workingDir)






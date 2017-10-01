"""
Template functions to run the example cases.
"""
from __future__ import print_function
import tellurium as te
import os




def run_case(call_file, antimony_str, phrasedml_str, py_code=False, working_dir=None):
    """ Run one of the example phrasedml cases.

    :param case_id:
    :param antimony_str:
    :param phrasedml_str:
    :return:
    """
    # run as omex
    # FIXME: convert to combine archive
    inline_omex = '\n'.join([antimony_str, phrasedml_str])

    # output dir relative to call file
    if not working_dir:
        working_dir = os.path.join(os.path.dirname(call_file), './results')
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

    # FIXME: not working
    # write python code
    if py_code:
        fname = os.path.basename(call_file)
        py_file = os.path.join(working_dir, fname + 'code.py')
        print(py_file)
        with open(py_file, 'w') as f:
            f.write(exp._toPython(phrasedml_str, workingDir=working_dir))

    # execute python
    te.executeInlineOmex(inline_omex)

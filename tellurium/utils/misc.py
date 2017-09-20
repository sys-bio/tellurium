from __future__ import print_function, division, absolute_import

import functools
import os
import sys
import warnings

# ---------------------------------------------------------------------
# Simple File Read and Store Utilities
# ---------------------------------------------------------------------
def saveToFile(filePath, str):
    """ Save string to file.

    see also: :func:`readFromFile`

    :param filePath: file path to save to
    :param str: string to save
    """
    with open(filePath, 'w') as f:
        f.write(str)


def readFromFile(filePath):
    """ Load a file and return contents as a string.

    see also: :func:`saveToFile`

    :param filePath: file path to read from
    :returns: string representation of the contents of the file
    """
    with open(filePath, 'r') as f:
        string = f.read()
    return string


# ---------------------------------------------------------------------
# Deprecated warning
# ---------------------------------------------------------------------
def deprecated(func):
    """This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1
        )
        return func(*args, **kwargs)
    return new_func

# ---------------------------------------------------------------------
# Running external tools
# ---------------------------------------------------------------------
def runTool (toolFileName):
    """ Call an external application called toolFileName.
        Note that .exe extension may be omitted for windows applications.

        Include any arguments in arguments parameter.

        Example:
        returnString = te.runTool (['myplugin', 'arg1', 'arg2'])

              If the external tool writes to stdout, this will be captured and returned.

        :param arguments to external tool
        :return String return by external tool, if any.
        """
    import subprocess
    try:
        p = os.path.dirname(sys.executable)
        root, waste = os.path.split(p)
        toolFileName[0] = root + '\\telluriumTools\\' + toolFileName[0] + '\\' + toolFileName[0] + '.exe'
        return subprocess.check_output(toolFileName)
    except subprocess.CalledProcessError as e:
        raise Exception('Tool failed to run correctly or could not be found')

"""
Helper functions for tests.
"""
import os

def filesInDirectory(directory, suffix):
    """ Find files with given suffix in directory.

    :param directory:
    :param suffix:
    :return:
    :rtype:
    """
    # FIXME: callable filter function
    from os import walk
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend([os.path.join(dirpath, name) for name in filenames])
    return [f for f in files if f.endswith(suffix)]



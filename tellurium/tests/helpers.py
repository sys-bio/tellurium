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
    def f_filter(filename):
        return filename.endswith(suffix)

    return filesInDirectoryFiltered(directory, f_filter=f_filter)


def filesInDirectoryFiltered(directory, f_filter):
    """ Find finds where the filename passes filter.

    :param directory:
    :param f_filter: filter function which returns true or false.
    :return:
    """
    files = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        files.extend([os.path.join(dirpath, name) for name in filenames])
    return [f for f in files if f_filter(f)]

"""
Combine Archive helper functions based on libcombine.
"""
from __future__ import absolute_import
import os
import zipfile
try:
    import libcombine
except ImportError:
    import tecombine as libcombine


def extractCombineArchive(omex_path, directory, method="zip"):
    """ Extracts combine archive at given path to directory.

    The zip method extracts all entries in the zip, the omex method
    only extracts the entries listed in the manifest.
    In some archives not all content is listed in the manifest.

    :param omex_path:
    :param directory:
    :param method: method to extract content, either 'zip' or 'omex'
    :return:
    """
    if method not in ["zip", "omex"]:
        raise ValueError("Method is not supported: {}".format(method))

    if method is "zip":
        zip_ref = zipfile.ZipFile(omex_path, 'r')
        zip_ref.extractall(directory)
        zip_ref.close()

    elif method is "omex":
        omex = libcombine.CombineArchive()
        if omex.initializeFromArchive(omex_path) is None:
            raise IOError("Invalid Combine Archive: {}", omex_path)

        for i in range(omex.getNumEntries()):
            entry = omex.getEntry(i)
            location = entry.getLocation()
            filename = os.path.join(directory, location)
            omex.extractEntry(location, filename)

        omex.cleanUp()


def getLocationsByFormat(omexPath, formatKey=None):
    """ Returns locations to files with given format in the archive.

    Uses the libcombine KnownFormats for formatKey, e.g., 'sed-ml' or 'sbml'.

    :param omexPath:
    :param formatKey:
    :return:
    """
    if not formatKey:
        raise ValueError("Format must be specified.")

    locations = []
    omex = libcombine.CombineArchive()
    if omex.initializeFromArchive(omexPath) is None:
        raise IOError("Invalid Combine Archive: {}", omexPath)

    for i in range(omex.getNumEntries()):
        entry = omex.getEntry(i)
        format = entry.getFormat()
        if libcombine.KnownFormats.isFormat(formatKey, format):
            locations.append(entry.getLocation())
    omex.cleanUp()

    return locations

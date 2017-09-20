"""
Creates the omex files from the given SED-ML files.
"""

from __future__ import print_function, absolute_import
import os
import libcombine

EXAMPLES_DIR = os.path.dirname(os.path.realpath(__file__))
SEDML_DIR = os.path.join(EXAMPLES_DIR, "./sedml")
OMEX_DIR = os.path.join(EXAMPLES_DIR, "./omex")


def create_omex_from_sedml(sedml_file, omex_file):
    """ Creates a combine archive from folder

    :param folder:
    :param omex_file:
    :return:
    """
    print('*' * 100)
    print('Create OMEX:')
    print('\t', sedml_file)
    print('*' * 100)
    time_now = libcombine.OmexDescription.getCurrentDateAndTime()
    archive = libcombine.CombineArchive()

    # add the sedml file
    location = os.path.relpath(sedml_file)
    format = "http://identifiers.org/combine.specifications/sed-ml"
    master = True
    archive.addFile(path, location, format, master)

    omex_d = libcombine.OmexDescription()
    omex_d.setAbout(location)
    omex_d.setCreated(time_now)

    archive.addMetadata(location, omex_d)

    # delete the old omex file
    if os.path.exists(omex_file):
        os.remove(omex_file)

    archive.writeToFile(omex_file)
    print('Archive created:', omex_file)


def printMetaDataFor(archive, location):
    """ Prints metadata for given location.

    :param archive: CombineArchive instance
    :param location:
    :return:
    """
    desc = archive.getMetadataForLocation(location)
    if desc.isEmpty():
        print("  no metadata for '{0}'".format(location))
        return None

    print("  metadata for '{0}':".format(location))
    print("     Created : {0}".format(desc.getCreated().getDateAsString()))
    for i in range(desc.getNumModified()):
        print("     Modified : {0}".format(desc.getModified(i).getDateAsString()))

    print("     # Creators: {0}".format(desc.getNumCreators()))
    for i in range(desc.getNumCreators()):
        creator = desc.getCreator(i)
        print("       {0} {1}".format(creator.getGivenName(), creator.getFamilyName()))


def printArchive(fileName):
    """ Prints content of combine archive

    :param fileName: path of archive
    :return: None
    """
    archive = libcombine.CombineArchive()
    if archive.initializeFromArchive(fileName) is None:
        print("Invalid Combine Archive")
        return None

    print('*'*80)
    print('Print archive:', fileName)
    print('*' * 80)
    printMetaDataFor(archive, ".")
    print("Num Entries: {0}".format(archive.getNumEntries()))

    for i in range(archive.getNumEntries()):
        entry = archive.getEntry(i)
        print(" {0}: location: {1} format: {2}".format(i, entry.getLocation(), entry.getFormat()))
        printMetaDataFor(archive, entry.getLocation())
    archive.cleanUp()


if __name__ == "__main__":
    # get sedml files

    sedml_files = []
    for subdir, dirs, files in os.walk(SEDML_DIR):
        for file in files:
            path = os.path.join(subdir, file)
            if os.path.isfile(path) and path.endswith('.xml'):
                sedml_files.append(path)

    for path in sorted(sedml_files):
        basename = os.path.basename(path)
        name = basename[:-4]  # name without extension

        sedml_file = os.path.abspath(path)
        omex_file = os.path.join(OMEX_DIR, "{}.omex".format(name))

        create_omex_from_sedml(sedml_file=sedml_file, omex_file=omex_file)
        printArchive(omex_file)
        print('\n\n')

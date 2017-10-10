"""
Creates all zip files.
Manifest exists in folder, so creating combine archives.
"""

from __future__ import print_function, absolute_import
import os
import shutil

from tellurium.utils import omex


def create_all_zip(base_dir, out_dir, extension):
    """Creates zip for all folders.

    :param base_dir:
    :param out_dir: output directory
    :param extension: file extension for zip file
    :return:
    """

    if not os.path.exists(base_dir):
        raise IOError

    # only in base dir, otherwise use os.walk for recursive subdirectories
    for directory in [f for f in os.listdir(base_dir) if os.path.isdir(f)]:

        if "_te_" in directory or directory == ".":
            continue

        omexName = os.path.basename(directory) + ".omex"
        omexPath = os.path.join(out_dir, omexName)
        print(directory, "-->", omexPath)

        omex.combineArchiveFromDirectory(directory=directory, omexPath=omexPath)


if __name__ == "__main__":
    print("*" * 80)
    print("Creating OMEX archives from folders")
    # TODO: infer the data types and create real omex

    print("*" * 80)
    create_all_zip(base_dir=".", out_dir=".", extension="omex")

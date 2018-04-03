"""
Testing the omex module.
"""
from __future__ import absolute_import, print_function
import os
import tempfile
import shutil
import pytest

from tellurium.tests.testdata import TESTDATA_DIR
from tellurium.tests.testdata import OMEX_SHOWCASE
from tellurium.utils import omex


def test_omex_extractCombineArchive1(tmpdir):
    omex.extractCombineArchive(omexPath=OMEX_SHOWCASE, directory=str(tmpdir), method="zip")


def test_omex_extractCombineArchive2(tmpdir):
    omex.extractCombineArchive(omexPath=OMEX_SHOWCASE, directory=str(tmpdir), method="omex")


def test_omex_extractCombineArchive3(tmpdir):
    tmp_dir = tempfile.mkdtemp()
    omex.extractCombineArchive(omexPath=OMEX_SHOWCASE, directory=str(tmpdir), method="zip")
    files = [f for f in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir, f))]
    assert files is not None


def test_omex_extractCombineArchive4(tmpdir):
    tmp_dir = tempfile.mkdtemp()
    omex.extractCombineArchive(omexPath=OMEX_SHOWCASE, directory=str(tmpdir), method="omex")
    files = [f for f in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir, f))]
    assert files is not None


# testing the omex based methods
def test_getLocationsByFormat1():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sed-ml")
    assert len(locations) == 2


def test_getLocationsByFormat2():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sbml")
    assert len(locations) == 1


def test_getLocationsByFormat3():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="cellml")
    assert len(locations) == 1


def test_getLocationsByFormat4():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sed-ml")
    assert len(locations) == 2
    # master=True file first
    assert locations[0].endswith("Calzone2007-simulation-figure-1B.xml")
    # master=False afterwards
    assert locations[1].endswith("Calzone2007-default-simulation.xml")


# test the zip based methods
def test_getLocationsByFormat1_zip():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sed-ml", method="zip")
    assert len(locations) == 2


def test_getLocationsByFormat2_zip():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sbml", method="zip")
    assert len(locations) == 1


def test_getLocationsByFormat3_zip():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="cellml", method="zip")
    assert len(locations) == 1


def test_getLocationsByFormat4_zip():
    locations = omex.getLocationsByFormat(omexPath=OMEX_SHOWCASE, formatKey="sed-ml", method="zip")
    assert len(locations) == 2
    # in case of zip files no master file exists, so the order of the entries depends on
    # filenames and how they are returned from the zip
    assert "experiment/Calzone2007-simulation-figure-1B.xml" in locations
    assert "experiment/Calzone2007-default-simulation.xml" in locations


def test_listContents():
    contents = omex.listContents(omexPath=OMEX_SHOWCASE, method="omex")
    assert len(contents) == 20


def test_printContents():
    omex.printContents(omexPath=OMEX_SHOWCASE)


def test_createCombineArchiveFromDirectory():
    """ Testing if COMBINE archive can be created from directory."""
    omexPath = tempfile.NamedTemporaryFile(suffix="omex")
    directory = os.path.join(TESTDATA_DIR, "utils", "omex_from_zip")
    omex.combineArchiveFromDirectory(omexPath=omexPath.name, directory=directory)
    assert omexPath is not None
    # TODO: additional checks via extracting information from the archive again








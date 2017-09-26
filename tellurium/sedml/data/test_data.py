from __future__ import print_function, absolute_import

import os
import pytest

from tellurium.sedml.data.datahandler import DataDescriptionParser
from tellurium.sedml.tesedml import SEDMLTools

try:
    import libsedml
except ImportError:
    import tesedml as libsedml


# ---------------------------------------------------------------------------------
BASE_DIR = "./examples"

SOURCE_CSV = os.path.join(BASE_DIR, "oscli.csv")
SOURCE_TSV = os.path.join(BASE_DIR, "oscli.tsv")
SOURCE_NUML = os.path.join(BASE_DIR, "./oscli.numl")
SOURCE_NUML_1D = os.path.join(BASE_DIR, "./OneDimensionalNuMLData.xml")
SOURCE_NUML_2D = os.path.join(BASE_DIR, "./TwoDimensionalNuMLData.xml")
SOURCE_NUML_2DRC = os.path.join(BASE_DIR, "./TwoDimensionTwoRCNuMLData.xml")

SEDML_READ_CSV = os.path.join(BASE_DIR, "reading-oscli-csv.xml")
SEDML_READ_TSV = os.path.join(BASE_DIR, "reading-oscli-tsv.xml")
SEDML_READ_NUML = os.path.join(BASE_DIR, "reading-oscli-numl.xml")
SEDML_READ_NUML_1D = os.path.join(BASE_DIR, "reading-oscli-numlData1D.xml.xml")
SEDML_READ_NUML_2D = os.path.join(BASE_DIR, "reading-oscli-numlData2D.xml")
SEDML_READ_NUML_2DRC = os.path.join(BASE_DIR, "reading-oscli-numlData2DRC.xml")

SEDML_EXPERIMENTAL_DATA = os.path.join(BASE_DIR, "experimental-data.xml")

# ---------------------------------------------------------------------------------

# Test data loading functions
def test_load_csv():
    data = DataDescriptionParser._load_csv(SOURCE_CSV)
    assert data is not None
    assert data.shape[0] == 200
    assert data.shape[1] == 3


def test_load_tsv():
    data = DataDescriptionParser._load_tsv(SOURCE_TSV)
    assert data is not None
    assert data.shape[0] == 200
    assert data.shape[1] == 3


def test_load_numl():
    data = DataDescriptionParser._load_csv(SOURCE_NUML)
    assert data is not None


def test_load_numl_1D():
    data = DataDescriptionParser._load_numl(SOURCE_NUML_1D)
    assert data is not None


def test_load_numl_2D():
    data = DataDescriptionParser._load_numl(SOURCE_NUML_2D)
    assert data is not None


def test_load_numl_2DRC():
    data = DataDescriptionParser._load_numl(SOURCE_NUML_2D)
    assert data is not None


def parseDataDescriptions(sedml_path):
    """ Test helper functions.

    Tries to parse all DataDescriptions in the SED-ML file.
    """
    print('parseDataDescriptions:', sedml_path)
    # load sedml document
    doc_sedml = libsedml.readSedMLFromFile(sedml_path)
    SEDMLTools.checkSEDMLDocument(doc_sedml)

    # parse DataDescriptions
    list_dd = doc_sedml.getListOfDataDescriptions()
    print(list_dd)
    print(len(list_dd))

    assert len(list_dd) > 0

    for dd in list_dd:
        data_sources = DataDescriptionParser.parse(dd, workingDir=BASE_DIR)
        assert data_sources is not None
        assert type(data_sources) == dict
        assert len(data_sources) > 0

def test_parse_csv():
    parseDataDescriptions(SEDML_READ_CSV)

def test_parse_tsv():
    parseDataDescriptions(SEDML_READ_TSV)

def test_parse_numl():
    parseDataDescriptions(SEDML_READ_NUML)

def test_parse_numl_1D():
    parseDataDescriptions(SEDML_READ_NUML_1D)

def test_parse_numl_2D():
    parseDataDescriptions(SEDML_READ_NUML_2D)

def test_parse_numl_2DRC():
    parseDataDescriptions(SEDML_READ_NUML_2DRC)


if __name__ == "__main__":
    pass

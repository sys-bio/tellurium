"""
Testing of SED-ML data support, i.e., DataDescription.
"""
from __future__ import print_function, absolute_import

import os
import pytest
import matplotlib

from tellurium.tests.testdata import TESTDATA_DIR

from tellurium.sedml.data import DataDescriptionParser
from tellurium.sedml.tesedml import SEDMLTools

try:
    import libsedml
except ImportError:
    import tesedml as libsedml

from tellurium.sedml import tesedml

# ---------------------------------------------------------------------------------
BASE_DIR = os.path.join(TESTDATA_DIR, 'sedml', 'data')

SOURCE_CSV = os.path.join(BASE_DIR, "oscli.csv")
SOURCE_TSV = os.path.join(BASE_DIR, "oscli.tsv")
SOURCE_NUML = os.path.join(BASE_DIR, "./oscli.xml")
SOURCE_NUML_1D = os.path.join(BASE_DIR, "./numlData1D.xml")
SOURCE_NUML_2D = os.path.join(BASE_DIR, "./numlData2D.xml")
SOURCE_NUML_2DRC = os.path.join(BASE_DIR, "./numlData2DRC.xml")

SEDML_READ_CSV = os.path.join(BASE_DIR, "reading-oscli-csv.xml")
SEDML_READ_TSV = os.path.join(BASE_DIR, "reading-oscli-tsv.xml")
SEDML_READ_NUML = os.path.join(BASE_DIR, "reading-oscli-numl.xml")
SEDML_READ_NUML_1D = os.path.join(BASE_DIR, "reading-numlData1D.xml")
SEDML_READ_NUML_2D = os.path.join(BASE_DIR, "reading-numlData2D.xml")
SEDML_READ_NUML_2DRC = os.path.join(BASE_DIR, "reading-numlData2DRC.xml")

OMEX_PLOT_CSV = os.path.join(BASE_DIR, 'omex', "plot_csv.omex")
OMEX_PLOT_CSV_WITH_MODEL = os.path.join(BASE_DIR, 'omex', "plot_csv_with_model.omex")
OMEX_PLOT_NUML = os.path.join(BASE_DIR, 'omex', "plot_numl.omex")
OMEX_PLOT_NUML_WITH_MODEL = os.path.join(BASE_DIR, 'omex', "plot_numl_with_model.omex")

SOURCE_CSV_PARAMETERS = os.path.join(BASE_DIR, "parameters.csv")
SEDML_CSV_PARAMETERS = os.path.join(BASE_DIR, "parameter-from-data-csv.xml")
OMEX_CSV_PARAMETERS = os.path.join(BASE_DIR, 'omex', "parameter_from_data_csv.omex")

OMEX_CSV_JWS_ADLUNG2017_FIG2G = os.path.join(BASE_DIR, 'omex', "jws_adlung2017_fig2g.omex")


# ---------------------------------------------------------------------------------
MPL_BACKEND = None


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    global MPL_BACKEND
    # Create a temporary directory
    MPL_BACKEND = matplotlib.rcParams['backend']
    matplotlib.pyplot.switch_backend("Agg")


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    matplotlib.pyplot.switch_backend(MPL_BACKEND)
    matplotlib.pyplot.close('all')


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
    data = DataDescriptionParser._load_numl(SOURCE_NUML)
    assert data is not None


def test_load_csv_parameters():
    data = DataDescriptionParser._load_csv(SOURCE_CSV_PARAMETERS)
    assert data is not None
    assert data.shape[0] == 10
    assert data.shape[1] == 1


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
    assert os.path.exists(sedml_path)

    doc_sedml = libsedml.readSedMLFromFile(sedml_path)
    SEDMLTools.checkSEDMLDocument(doc_sedml)

    # parse DataDescriptions
    list_dd = doc_sedml.getListOfDataDescriptions()
    # print(list_dd)
    # print(len(list_dd))

    assert len(list_dd) > 0

    for dd in list_dd:
        data_sources = DataDescriptionParser.parse(dd, workingDir=BASE_DIR)
        assert data_sources is not None
        assert type(data_sources) == dict
        assert len(data_sources) > 0
    return data_sources


def test_parse_csv():
    data_sources = parseDataDescriptions(SEDML_READ_CSV)
    assert "dataTime" in data_sources
    assert "dataS1" in data_sources
    assert len(data_sources["dataTime"]) == 200
    assert len(data_sources["dataS1"]) == 200


def test_parse_csv_parameters():
    data_sources = parseDataDescriptions(SEDML_CSV_PARAMETERS)
    assert "dataIndex" in data_sources
    assert "dataMu" in data_sources
    assert len(data_sources["dataIndex"]) == 10
    assert len(data_sources["dataMu"]) == 10



def test_parse_tsv():
    data_sources = parseDataDescriptions(SEDML_READ_TSV)
    assert "dataTime" in data_sources
    assert "dataS1" in data_sources
    assert len(data_sources["dataTime"]) == 200
    assert len(data_sources["dataS1"]) == 200


def test_parse_numl():
    data_sources = parseDataDescriptions(SEDML_READ_NUML)
    assert "dataTime" in data_sources
    assert "dataS1" in data_sources
    assert len(data_sources["dataTime"]) == 200
    assert len(data_sources["dataS1"]) == 200


def test_parse_numl_1D():
    data_sources = parseDataDescriptions(SEDML_READ_NUML_1D)
    assert data_sources is not None
    assert len(data_sources) == 6
    assert 'data_s_glu' in data_sources
    assert 'data_s_pyr' in data_sources
    assert 'data_s_acetate' in data_sources
    assert 'data_s_acetald' in data_sources
    assert 'data_s_EtOH' in data_sources
    assert 'data_x' in data_sources
    assert len(data_sources['data_s_glu']) == 1


def test_parse_numl_2D():
    data_sources = parseDataDescriptions(SEDML_READ_NUML_2D)
    assert data_sources is not None
    assert len(data_sources) == 4
    assert 'dataBL' in data_sources
    assert 'dataB' in data_sources
    assert 'dataS1' in data_sources
    assert 'dataTime' in data_sources
    assert len(data_sources['dataB']) == 6


def test_parse_numl_2DRC():
    data_sources = parseDataDescriptions(SEDML_READ_NUML_2DRC)
    assert data_sources is not None
    assert len(data_sources) == 4
    assert 'dataBL' in data_sources
    assert 'dataB' in data_sources
    assert 'dataS1' in data_sources
    assert 'dataTime' in data_sources
    assert len(data_sources['dataB']) == 6


def test_omex_plot_csv(tmpdir):
    results = tesedml.executeCombineArchive(OMEX_PLOT_CSV, workingDir=str(tmpdir))
    result = list(results.values())[0]
    dg_dict = result['dataGenerators']
    assert len(dg_dict) == 2
    assert "dgDataS1" in dg_dict
    assert "dgDataTime" in dg_dict
    assert len(dg_dict["dgDataS1"]) == 200
    assert len(dg_dict["dgDataTime"]) == 200


def test_omex_plot_csv_with_model(tmpdir):
    results = tesedml.executeCombineArchive(OMEX_PLOT_CSV_WITH_MODEL, workingDir=str(tmpdir))
    result = list(results.values())[0]
    dg_dict = result['dataGenerators']
    assert len(dg_dict) == 5
    assert "dgDataS1" in dg_dict
    assert "dgDataTime" in dg_dict
    assert len(dg_dict["dgDataS1"]) == 200
    assert len(dg_dict["dgDataTime"]) == 200


def test_omex_plot_numl(tmpdir):
    results = tesedml.executeCombineArchive(OMEX_PLOT_NUML, workingDir=str(tmpdir))
    result = list(results.values())[0]
    dg_dict = result['dataGenerators']
    assert len(dg_dict) == 2
    assert "dgDataS1" in dg_dict
    assert "dgDataTime" in dg_dict
    assert len(dg_dict["dgDataS1"]) == 200
    assert len(dg_dict["dgDataTime"]) == 200


def test_omex_plot_numl_with_model(tmpdir):
    results = tesedml.executeCombineArchive(OMEX_PLOT_NUML_WITH_MODEL, workingDir=str(tmpdir))
    result = list(results.values())[0]
    dg_dict = result['dataGenerators']
    assert len(dg_dict) == 5
    assert "dgDataS1" in dg_dict
    assert "dgDataTime" in dg_dict
    assert len(dg_dict["dgDataS1"]) == 200
    assert len(dg_dict["dgDataTime"]) == 200

def test_omex_jws_adlung2017_fig2gl(tmpdir):
    results = tesedml.executeCombineArchive(OMEX_CSV_JWS_ADLUNG2017_FIG2G, workingDir=str(tmpdir))
    result = list(results.values())[0]
    dg_dict = result['dataGenerators']
    assert len(dg_dict) == 40


@pytest.mark.skip("Not supported in L1V3, will be part of L1V4")
def test_omex_csv_parameters(tmpdir):
    results = tesedml.executeCombineArchive(OMEX_CSV_PARAMETERS, workingDir=str(tmpdir))
    result = list(results.values())[0]
    dgs = result['dataGenerators']

    dg_dict = list(dgs.values())[0]
    assert len(dg_dict) == 2
    assert "dgDataIndex" in dg_dict
    assert "dgDataMu" in dg_dict
    assert len(dg_dict["dgDataIndex"]) == 10
    assert len(dg_dict["dgDataMu"]) == 10

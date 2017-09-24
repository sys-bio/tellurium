from __future__ import print_function, absolute_import

import os
import pytest

from tellurium.sedml.data import data


# ---------------------------------------------------------------------------------
BASE_DIR = "./examples"

SOURCE_CSV = os.path.join(BASE_DIR, "oscli.csv")
SOURCE_TSV = os.path.join(BASE_DIR, "oscli.tsv")
SOURCE_NUML = os.path.join(BASE_DIR, "./oscli.numl")

SOURCE_NUML_1D = os.path.join(BASE_DIR, "./OneDimensionalNuMLData.xml")
SOURCE_NUML_2D = os.path.join(BASE_DIR, "./TwoDimensionalNuMLData.xml")
SOURCE_NUML_2DRC = os.path.join(BASE_DIR, "./TwoDimensionTwoRCNuMLData.xml")
# ---------------------------------------------------------------------------------


def test_csv():
    data_slices = data.load_data(SOURCE_CSV, format=data.FORMAT_CSV, slices=["time", "S1", "S2"])
    assert data_slices is not None
    assert len(data_slices) == 3
    print(data_slices)


def test_tsv():
    data_slices = data.load_data_slices(SOURCE_TSV, format=data.FORMAT_TSV, slices=["time", "S1", "S2"])
    assert data_slices is not None
    assert len(data_slices) == 3
    print(data_slices)


def test_numl():
    data_sources = data.load_data(SOURCE_NUML, format=data.FORMAT_NUML)
    assert data_sources is not None
    print(data_sources)


'''
def test_numl_1d():
    data_sources = data.load_data(SOURCE_NUML_1D, format=data.FORMAT_NUML)
    assert data_sources is not None
    print(data_sources)


def test_numl_2d():
    data_sources = data.load_data(SOURCE_NUML_2D, format=data.FORMAT_NUML)
    assert data_sources is not None
    print(data_sources)


def test_numl_2drc():
    data_sources = data.load_data(SOURCE_NUML_2DRC, format=data.FORMAT_NUML)
    assert data_sources is not None
    print(data_sources)
'''


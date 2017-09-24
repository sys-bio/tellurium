"""
Reading CSV and TSV data.
"""
from __future__ import print_function, absolute_import
import pandas as as pd
import tempfile

FORMAT_URN = "urn:sedml:format:"
NUML_URN = "urn:sedml:format:numl"
CSV_URN = "urn:sedml:format:csv"
TSV_URN = "urn:sedml:format:tsv"
FORMATS = [NUML_URN, CSV_URN, TSV_URN]


# py2 / py3
try:
    import httplib
except ImportError:
    import http.client as httplib


def isHttp(source):
    return source.startswith('http') or source.startswith('HTTP')

def load_data(source, format):

    # TODO: get data from source
    file = source
    if source.startswith('http') or source.startswith('HTTP'):
        conn = httplib.HTTPConnection(url)
        conn.request("GET", "")
        r1 = conn.getresponse()
        # print(r1.status, r1.reason)
        data = r1.read()
        conn.close()

        try:
            data_str = str(data.decode("utf-8"))
        except:
            data_str = str(data)

    # Find the format
    if format is None:
        # defaults to numl
        format = NUML_URN

    # only interested in base format
    if format.startswith(NUML_URN):
        format = NUML_URN

    # check supported formats
    if format not in FORMATS:
        raise NotImplementedError("Only the following data formats are supported: {}".format(FORMATS))




def getFileFrom(url):
    """ Get SBML string from given BioModels URN.

    Searches for a BioModels identifier in the given urn and retrieves the SBML from biomodels.
    For example:
        urn:miriam:biomodels.db:BIOMD0000000003.xml

    :param urn:
    :return: SBML string for given model urn
    """





    return sbml_str


def load_csv_data(source):
    """ Helper function for loading data file from given source.

    CSV files must have a header.

    :param source: source information from the SED-ML file
    :return: data matrix
    """
    # FIXME: handle urn/url sources
    # FIXME: figure out the separator for data reading based on the dimension
    sep = ","
    df = pd.read_csv(source, sep=sep)
    return df




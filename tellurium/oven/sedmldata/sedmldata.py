"""
Testing reading data form the libsedml.

Necessary to compile the latest version.

- not able to load CompositeDescription from DataDescription
- only 2D data, or also higher dimensional data supported?

"""
from __future__ import absolute_import, print_function
import warnings
import numpy as np
import pandas as pd

try:
    import libsedml
except ImportError:
    import tesedml as libsedml
print('Version:', libsedml.getLibSEDMLDottedVersion())


def load_csv_data(source):
    """ Helper function for loading data file from given source.
    :param source: source information from the SED-ML file
    :return: data matrix
    """
    raise NotImplemented


def load_numl_data(source):
    """ Helper function for loading data files from given source.
    :param source: 
    :return: data matrix
    """
    raise NotImplemented



# load numl document
doc_numl = libsedml.readNUMLFromFile('./oscil.numl')
print(doc_numl)


# --------------------------------------
# Sedml document
# --------------------------------------

# load sedml document
doc_sedml = libsedml.readSedMLFromFile('data_plot_numl.xml')
print(doc_sedml)

# --------------------------------------
# ListOfDataDescriptions
# --------------------------------------
list_dd = doc_sedml.getListOfDataDescriptions()
print(list_dd)
print(len(list_dd))

for dd in list_dd:
    # There can be multiple DataDescription
    print('-' * 80)
    print('DataDescription')
    print('-' * 80)

    print('dd:', dd)
    print('id:', dd.getId())
    print('name:', dd.getId())
    print('source', dd.getSource())

    print('\n*** DataSources ***')
    '''
    The DataSource class extracts chunks out of the data 
    file provided by the outer DataDescription element.
    '''

    for ds in dd.getListOfDataSources():
        print('\nds:', ds)
        print('id:', ds.getId())
        print('name:', ds.getName())
        print('indexSet:', ds.getIndexSet())
        print('slices')
        for slice in ds.getListOfSlices():
            print(slice)
            print('\treference:', slice.getReference())
            print('\tvalue:', slice.getValue())

    print('*** DimensionDescriptions ***')
    '''
    The dimensionDescription element is the data description from an NuML file.
    '''
    dim_description = dd.getDimensionDescription()
    print('Dimension description:', dim_description)

    cd_top = dim_description.getCompositeDescription()
    print(cd_top, type(cd_top))
    # TODO: read the compositeDescription


if __name__ == "__main__":
    pass
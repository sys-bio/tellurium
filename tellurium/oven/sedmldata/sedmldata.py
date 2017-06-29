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
import libnuml

try:
    import libsedml
except ImportError:
    import tesedml as libsedml
print('Version:', libsedml.getLibSEDMLDottedVersion())


SOURCE_CSV = "./oscli.csv"
SOURCE_NUML = "./oscli.numl"


#####################################
# NUML PARSING
#####################################
def parse_dimension_description(dd):
    """ Parses the dimension information from the dimension description.

          <dimensionDescription>
            <compositeDescription indexType="double" name="time">
              <compositeDescription indexType="string" name="SpeciesIds">
                <atomicDescription valueType="double" name="Concentrations" />
              </compositeDescription>
            </compositeDescription>
          </dimensionDescription>
          <dimension>

    :param dd:
    :return:
    """
    cd_top = dd.getCompositeDescription()
    print('cd_top', cd_top)

    dim_info = None
    # FIXME: implement
    return dim_info


def load_numl_data(source):
    """ Helper function for loading data files from given source.

    For more information see:
        https://github.com/numl/numl

          <dimensionDescription>
            <compositeDescription indexType="double" name="time">
              <compositeDescription indexType="string" name="SpeciesIds">
                <atomicDescription valueType="double" name="Concentrations" />
              </compositeDescription>
            </compositeDescription>
          </dimensionDescription>

    :param source: 
    :return: data matrix
    """
    # FIXME: handle urn/url sources

    doc_numl = libnuml.readNUMLFromFile(source)

    print('source:', source)
    print(doc_numl)

    # reads all the resultComponents from the numl file
    results = []

    Nrc = doc_numl.getNumResultComponents()
    rcs = doc_numl.getResultComponents()
    libnuml.ResultComponents


    print('NumResultComponents:', Nrc)
    for k in range(Nrc):
        res_comp = rcs.get(k)
        print(type(res_comp))
        dd = res_comp.getDimensionDescription()
        print(dd)
        dimension_info = parse_dimension_description(dd)

        for cvalue in dd.getComponentValues():
            print(cvalue)


    # TODO: figure out the dimensionality, and create np.array
    # if 2D return a DataFrame (Does this work with the slicing?)

    columns = None
    data = None

    df = None
    return df

# load data from sources
# FIXME: implement, see
df_numl = load_numl_data(SOURCE_NUML)
print(df_numl)



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





df_csv = load_csv_data(SOURCE_CSV)
print(df_csv.head())

exit()



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
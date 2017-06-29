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

import libnuml

SOURCE_CSV = "./oscli.csv"
SOURCE_NUML = "./oscli.numl"
SOURCE_NUML_1D = "./OneDimensionalNuMLData.xml"
SOURCE_NUML_2D = "./TwoDimensionalNuMLData.xml"


#####################################
# NUML PARSING
#####################################

def parse_description(d, info=None):
    """ Parses the recursive DimensionDescription, TupleDescription,
    AtomicDescription.

    :param d:
    :param info:
    :return:
    """
    if info is None:
        info = []

    if d.isContentCompositeDescription():
        assert(isinstance(d, libnuml.CompositeDescription))
        content = {
            'id': d.getId(),
            'name': d.getName(),
            'indexType': d.getIndexType(),
        }
        info.append(content)
        print('* CompositeDescription *', content)

        info = parse_description(d.get(0), info)

    elif d.isContentTupleDescription():

        tuple_des = d.getTupleDescription()
        assert (isinstance(tuple_des, libnuml.TupleDescription))

        Natomic = tuple_des.size()
        valueTypes = []
        for k in range(Natomic):
            atomic = tuple_des.getAtomicDescription(k)
            assert(isinstance(atomic, libnuml.AtomicDescription))
            valueTypes.append(atomic.getValueType())

        info.append(valueTypes)
        print('* TupleDescription * ', valueTypes)

    elif d.isContentAtomicDescription():
        atomic = d.getAtomicDescription()
        assert(isinstance(atomic, libnuml.AtomicDescription))

        valueTypes = [atomic.getValueType()]
        info.append(valueTypes)
        print('* AtomicDescription *', valueTypes)

    return info


def parse_value(d, info=None):
    """ Parses the recursive CompositeValue, Tuple, AtomicValue.

    :param d:
    :param info:
    :return:
    """
    # TODO: implement
    pass


def parse_dimension_description(dd):
    # type: (libnuml.DimensionDescription) -> None
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
    print("DimensionDescription:", dd)
    assert(isinstance(dd, libnuml.DimensionDescription))
    cd_top = dd.get(0)
    dim_info = parse_description(cd_top)

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
        print('-'*80)
        # parse the ResultComponent
        res_comp = rcs.get(k)
        dd = res_comp.getDimensionDescription()

        # dimension info
        dimension_info = parse_dimension_description(dd)
        print("dimension_info", dimension_info)

        # data
        # for cvalue in dd.getComponentValues():
        #    print(cvalue)


    # TODO: figure out the dimensionality, and create np.array
    # if 2D return a DataFrame (Does this work with the slicing?)
    df = None
    return df

# load data from sources
# FIXME: implement, see
df_numl = load_numl_data(SOURCE_NUML_1D)
# df_numl = load_numl_data(SOURCE_NUML)
print(df_numl)

exit()


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
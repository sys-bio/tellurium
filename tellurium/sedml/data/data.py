"""
Testing reading data form the libsedml.

Helper functions to work with data in SED-ML.
This includes helper for CSV and NUML.

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
        print('\t* CompositeDescription *', content)

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
        print('\t* TupleDescription * ', valueTypes)

    elif d.isContentAtomicDescription():
        atomic = d.getAtomicDescription()
        assert(isinstance(atomic, libnuml.AtomicDescription))

        valueTypes = [atomic.getValueType()]
        info.append(valueTypes)
        print('* AtomicDescription *', valueTypes)

    return info


def parse_value(d, data=None):
    """ Parses the recursive CompositeValue, Tuple, AtomicValue.

    :param d:
    :param data:
    :return:
    """
    if data is None:
        data = []

    print(type(d), d)
    if d.isCompositeValue():
        assert(isinstance(d, libnuml.CompositeValue))
        content = {
            'indexValue': d.getIndexValue(),
        }
        data.append(content)
        print('\t* CompositeValue *', content)

        info = parse_value(d.get(0), data)

    elif d.isConentTuple():

        tuple = d.getTuple()
        assert (isinstance(tuple, libnuml.Tuple))

        Natomic = tuple.size()
        values = []
        for k in range(Natomic):
            atomic = tuple.getAtomicValue(k)
            assert(isinstance(atomic, libnuml.Atomic))
            values.append(atomic.getDoubleValue())
        data.append(values)
        print('\t* TupleDescription * ', values)

    elif d.isContentAtomicValue():
        atomic = d.getAtomicValue()
        assert(isinstance(atomic, libnuml.AtomicValue))

        values = [atomic.getDoubleValue()]
        data.append(values)
        print('* AtomicValue *', values)

    return data


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
    print('source:', source, doc_numl)

    # reads all the resultComponents from the numl file
    results = []

    Nrc = doc_numl.getNumResultComponents()
    rcs = doc_numl.getResultComponents()
    print('NumResultComponents:', Nrc)
    for k in range(Nrc):
        print('-'*80)
        # parse ResultComponent
        res_comp = rcs.get(k)

        # dimension info
        dim_description = res_comp.getDimensionDescription()
        print("DimensionDescription:", dim_description)
        assert (isinstance(dim_description, libnuml.DimensionDescription))
        info = parse_description(dim_description.get(0))
        print("info:", info)

        # data
        dim = res_comp.getDimension()
        print("Dimension:", dim)
        assert (isinstance(dim, libnuml.Dimension))
        data = parse_value(dim.get(0))
        print("data", data)

        res = {'info': info, 'data': data}
        results.append(res)

    return results

# load data from sources
# FIXME: implement, see
for source in [SOURCE_NUML, SOURCE_NUML_1D, SOURCE_NUML_2D, SOURCE_NUML_2DRC]:
    print('#' * 80)
    print(source)
    print('#' * 80)

    df_numl = load_numl_data(source)
    print(df_numl)
    print()

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


def sedml_example():
    # --------------------------------------
    # Sedml document
    # --------------------------------------

    # load sedml document
    doc_sedml = libsedml.readSedMLFromFile('./data_plot_numl.xml')
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
    # libnuml.NUMLDocument.getNumResultComponents()
    print('NumResultComponents:', Nrc)

    for res_comp in doc_numl.getResultComponents():
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


if __name__ == "__main__":
    # -----------------------------------------------------
    SOURCE_CSV = "./oscli.csv"
    SOURCE_NUML = "./oscli.numl"
    SOURCE_NUML_1D = "./OneDimensionalNuMLData.xml"
    SOURCE_NUML_2D = "./TwoDimensionalNuMLData.xml"
    SOURCE_NUML_2DRC = "./TwoDimensionTwoRCNuMLData.xml"
    # -----------------------------------------------------

    # load data from sources
    df_numl = load_numl_data(SOURCE_NUML)
    print(df_numl)

    sedml_example()


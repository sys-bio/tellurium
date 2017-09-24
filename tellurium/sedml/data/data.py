"""
Reading NUML, CSV and TSV data from DataDescriptions
"""
from __future__ import print_function, absolute_import
import pandas as pd

# py2 / py3
try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    import libsedml
except ImportError:
    import tesedml as libsedml

try:
    import libnuml
except ImportError:
    import tenuml as libnuml

# -----------------------------------------------------
# Format definitions
# -----------------------------------------------------
FORMAT_URN = "urn:sedml:format:"
FORMAT_NUML = "urn:sedml:format:numl"
FORMAT_CSV = "urn:sedml:format:csv"
FORMAT_TSV = "urn:sedml:format:tsv"
FORMATS = [FORMAT_NUML, FORMAT_CSV, FORMAT_TSV]
# -----------------------------------------------------


def load_data(dataDescription):
    """ Load data from given DataDescription.

    Returns the DataSources.

    :param dataDescription: SED-ML data descripions
    :return: dataSources
    """
    source = dataDescription.getSource()
    format = dataDescription.getFormat()

    # TODO: necessary to read the DataSources

    # returns a dictionary of data sources


    return load_data(source=source, format=format)


def load_data(source, format, indexSet=None, slices=None):
    """ Load data from given source and format

    Returns the DataSources.

    :param source:
    :param format:
    :return: dataSources
    """
    if slices is None:
        slices = []  # mutable default argument

    # TODO: get data from source



    # Find the format
    if format is None:
        # defaults to numl
        format = FORMAT_NUML

    # only interested in base format
    if format.startswith(FORMAT_NUML):
        format = FORMAT_NUML

    # check supported formats
    if format not in FORMATS:
        raise NotImplementedError("Only the following data formats are supported: {}".format(FORMATS))

    data_sources = None
    # CSV
    if format == FORMAT_CSV:
        data_slices = _load_sv(source, separator=",", slices=slices)
    # TSV
    elif format == FORMAT_TSV:
        data_slices = _load_sv(source, separator="\t", slices=slices)
    # NUML
    elif format == FORMAT_NUML:
        # TODO: implement
        _load_numl(source=source)

    return data_sources


def _load_sv(source, separator, slices):
    """ Helper function for loading data file from given source.

    CSV files must have a header.

    :param source: source information from the SED-ML file
    :return: dictionary of data sources
    """
    df = pd.read_csv(source, sep=separator,
                     index_col=False,
                     skip_blank_lines=True,
                     quotechar='"',
                     comment="#",
                     skipinitialspace=True)
    # print(df)
    data_slices = []
    for sid in slices:
        data_slices.append(df[sid])
    return data_slices


def _load_numl(source):
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

    doc_numl = None

    if source.startswith('http') or source.startswith('HTTP'):
        conn = httplib.HTTPConnection(source)
        conn.request("GET", "")
        r1 = conn.getresponse()
        # print(r1.status, r1.reason)
        data = r1.read()
        conn.close()
        try:
            numl_str = str(data.decode("utf-8"))
        except:
            numl_str = str(data)
        doc_numl = libnuml.readNUMLFromString(numl_str)
    else:
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



# ----------------------------------------------------------------------------------
# NUML PARSING
# ----------------------------------------------------------------------------------

def sedml_example(sedml_file):
    """ Parsing data descriptions from given SEDML file.

    :param sedml_file:
    :return:
    """
    print('*' * 80)
    print(sedml_file)
    print('*' * 80)

    # load sedml document
    doc_sedml = libsedml.readSedMLFromFile(sedml_file)
    print(doc_sedml)

    # parse DataDescriptions
    list_dd = doc_sedml.getListOfDataDescriptions()

    for dd in list_dd:
        parseDataDescription(dd)

def parseDataDescription(dd):
    """ Parses single DataDescription.

    :param dd:
    :return:
    """
    print('-' * 80)
    print('DataDescription: :', dd)
    print('\tid:', dd.getId())
    print('\tname:', dd.getId())
    print('\tsource', dd.getSource())


    dim_description = dd.getDimensionDescription()
    print('\n\t*** DimensionDescription:', dim_description)

    cd_top = dim_description.getCompositeDescription()
    print(cd_top, type(cd_top))
    # TODO: read the compositeDescription

    for k, ds in enumerate(dd.getListOfDataSources()):
        print('\n\t*** DataSource:', ds)
        print('\t\tid:', ds.getId())
        print('\t\tname:', ds.getName())
        print('\t\tindexSet:', ds.getIndexSet())
        print('\t\tslices')
        for slice in ds.getListOfSlices():
            print('\t\t\treference={}; value={}'.format(slice.getReference(), slice.getValue()))


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


def parse_description(d, info=None):
    """ Parses the recursive DimensionDescription, TupleDescription, AtomicDescription.

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




if __name__ == "__main__":
    sedml_file = './examples/data_plot_numl.xml'
    sedml_example(sedml_file)

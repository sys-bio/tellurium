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


class DataDescriptionParser(object):
    """ Class for parsing DataDescriptions. """

    @staticmethod
    def parse(dd):
        """ Parses single DataDescription.

        Returns dictionary of data sources {DataSource.id, slice_data}

        :param dd: SED-ML DataDescription
        :return:
        """
        did = dd.getId()
        name = dd.getName()
        source = dd.getSource()
        format = None
        if hasattr(dd, "getFormat"):
            format = dd.getFormat()

        print('-' * 80)
        print('DataDescription: :', dd)
        print('\tid:', did)
        print('\tname:', name)
        print('\tsource', source)

        # -------------------------------
        # Parse DimensionDescription
        # -------------------------------
        # TODO: parse the DimensionDescription
        dim_description = dd.getDimensionDescription()
        print('\n\t*** DimensionDescription:', dim_description)

        cd_top = dim_description.getCompositeDescription()
        print(cd_top, type(cd_top))

        # -------------------------------
        # Find the format
        # -------------------------------
        if format is None:
            # defaults to numl
            format = FORMAT_NUML

            # only interested in base format
        if format.startswith(FORMAT_NUML):
            format = FORMAT_NUML

            # check supported formats
        if format not in FORMATS:
            raise NotImplementedError("Only the following data formats are supported: {}".format(FORMATS))

        # -------------------------------
        # Load complete data
        # -------------------------------
        data = None
        # CSV
        if format == FORMAT_CSV:
            data = DataDescriptionParser._load_sv(source, separator=",")
        # TSV
        elif format == FORMAT_TSV:
            data = DataDescriptionParser = DataDescriptionParser._load_sv(source, separator="\t")
        # NUML
        elif format == FORMAT_NUML:
            DataDescriptionParser._load_numl(source=source)

        # -------------------------------
        # Process DataSources
        # -------------------------------
        # TODO: parse DataSources (this gets the subset of data out of the full dataset)
        data_sources = {}
        for k, ds in enumerate(dd.getListOfDataSources()):
            print('\n\t*** DataSource:', ds)
            print('\t\tid:', ds.getId())
            print('\t\tname:', ds.getName())
            print('\t\tindexSet:', ds.getIndexSet())
            print('\t\tslices')
            for slice in ds.getListOfSlices():
                print('\t\t\treference={}; value={}'.format(slice.getReference(), slice.getValue()))

                # CSV/TSV
                data_slices = []
                for sid in slices:
                    data_slices.append(df[sid])

                # NUML

        return data_sources

    @staticmethod
    def _load_sv(source, separator):
        """ Helper function for loading data file from given source.

        CSV files must have a header. Handles file and online resources.

        :param source: source information from the SED-ML file
        :return: dictionary of data sources
        """
        df = pd.read_csv(source, sep=separator,
                         index_col=False,
                         skip_blank_lines=True,
                         quotechar='"',
                         comment="#",
                         skipinitialspace=True)
        return df

    @staticmethod
    def _load_numl(source):
        """ Helper function for loading data files from given source.

        This loads the complete numl data.
        Subsequently subsets of the data can be selected via DataSources from the dataset.

        For more information see:
            https://github.com/numl/numl

              <dimensionDescription>
                <compositeDescription indexType="double" name="time">
                  <compositeDescription indexType="string" name="SpeciesIds">
                    <atomicDescription valueType="double" name="Concentrations" />
                  </compositeDescription>
                </compositeDescription>
              </dimensionDescription>

        :param dd: dimensionDescription: outer dimension description
        :return: data matrix
        """
        # Read the numl document
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

    @staticmethod
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

    @staticmethod
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
        DataDescriptionParser.parse(dd)


if __name__ == "__main__":
    sedml_file = './examples/data_plot_numl.xml'
    sedml_example(sedml_file)

"""
Reading NUML, CSV and TSV data from DataDescriptions
"""
from __future__ import print_function, absolute_import
import os
import pandas as pd
from pprint import pprint
import csv

import tempfile

# py2 / py3
try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    import libnuml

except ImportError:
    import tenuml as libnuml


class DataDescriptionParser(object):
    """ Class for parsing DataDescriptions. """

    FORMAT_URN = "urn:sedml:format:"
    FORMAT_NUML = "urn:sedml:format:numl"
    FORMAT_CSV = "urn:sedml:format:csv"
    FORMAT_TSV = "urn:sedml:format:tsv"

    # supported formats
    SUPPORTED_FORMATS = [FORMAT_NUML, FORMAT_CSV, FORMAT_TSV]

    @classmethod
    def parse(cls, dd, workingDir=None):
        """ Parses single DataDescription.

        Returns dictionary of data sources {DataSource.id, slice_data}

        :param dd: SED-ML DataDescription
        :param workingDir: workingDir relative to which the sources are resolved
        :return:
        """
        did = dd.getId()
        name = dd.getName()
        source = dd.getSource()

        # -------------------------------
        # Resolve source
        # -------------------------------
        # FIXME: this must work for absolute paths and URL paths
        if workingDir is None:
            workingDir = '.'

        tmp_file = None
        if source.startswith('http') or source.startswith('HTTP'):
            conn = httplib.HTTPConnection(source)
            conn.request("GET", "")
            r1 = conn.getresponse()
            # print(r1.status, r1.reason)
            data = r1.read()
            conn.close()
            try:
                file_str = str(data.decode("utf-8"))
            except:
                file_str = str(data)

            doc_numl = libnuml.readNUMLFromString(numl_str)
            tmp_file = tempfile.NamedTemporaryFile("w")
            tmp_file.write(file_str)
            source_path = tmp_file.name
        else:
            source_path = os.path.join(workingDir, source)

        # -------------------------------
        # Find the format
        # -------------------------------
        format = None
        if hasattr(dd, "getFormat"):
            format = dd.getFormat()
        format = cls._determine_format(source_path=source_path, format=format)

        print('-' * 80)
        print('DataDescription: :', dd)
        print('\tid:', did)
        print('\tname:', name)
        print('\tsource', source)
        print('\tformat', format)

        # -------------------------------
        # Parse DimensionDescription
        # -------------------------------
        # TODO: parse the DimensionDescription
        '''
        dim_description = dd.getDimensionDescription()
        print('\n\t*** DimensionDescription:', dim_description)

        cd_top = dim_description.getCompositeDescription()
        print(cd_top, type(cd_top))
        '''

        # -------------------------------
        # Load complete data
        # -------------------------------
        data = None
        if format == cls.FORMAT_CSV:
            data = cls._load_csv(source=source_path)
        elif format == cls.FORMAT_TSV:
            data = cls._load_tsv(source=source_path)
        elif format == cls.FORMAT_NUML:
            data = cls._load_numl(source=source_path)

        print("-" * 80)
        print("Data")
        print("-" * 80)
        pprint(data)
        print("-" * 80)

        # -------------------------------
        # Process DataSources
        # -------------------------------
        # TODO: parse DataSources (this gets the subset of data out of the full dataset)
        data_sources = {}
        for k, ds in enumerate(dd.getListOfDataSources()):

            dsid = ds.getId()

            print('\n\t*** DataSource:', ds)
            print('\t\tid:', ds.getId())
            print('\t\tname:', ds.getName())
            print('\t\tindexSet:', ds.getIndexSet())
            print('\t\tslices')

            # CSV/TSV
            if format in [cls.FORMAT_CSV, cls.FORMAT_TSV]:
                sids = []
                for slice in ds.getListOfSlices():
                    print('\t\t\treference={}; value={}'.format(slice.getReference(), slice.getValue()))

                    sids.append(slice.getValue())
                # get columns from pandas DataFrame
                data_sources[dsid] = data[sids].values

            # NUML
            elif format == cls.FORMAT_NUML:
                # TODO: not implemented
                pass

        print("-" * 80)
        print("DataSources")
        print("-" * 80)
        for key, value in data_sources.items():
            print('{} : {}; shape={}'.format(key, type(value), value.shape))
        print("-" * 80)

        # cleanup
        if tmp_file is not None:
            # TODO: implement cleanup of tmp file
            pass

        return data_sources


    @classmethod
    def _determine_format(cls, source_path, format=None):
        """

        :param source_path: path of file
        :param format: format given in the DataDescription
        :return:
        """
        if format is None:
            is_xml = False
            with open(source_path) as unknown_file:
                start_str = unknown_file.read(1024)
                start_str = start_str.strip()
                if start_str.startswith('<'):
                    is_xml = True

            if is_xml:
                # xml format is numl
                format = cls.FORMAT_NUML  # defaults to numl
            else:
                # format is either csv or tsv
                df_csv = cls._load_csv(source_path)
                df_tsv = cls._load_tsv(source_path)
                if df_csv.shape[1] >= df_tsv.shape[1]:
                    format = cls.FORMAT_CSV
                else:
                    format = cls.FORMAT_TSV

        # base format
        if format.startswith(cls.FORMAT_NUML):
            format = cls.FORMAT_NUML

        # check supported formats
        if format not in cls.SUPPORTED_FORMATS:
            raise NotImplementedError("Only the following data formats are supported: {}".format(cls.FORMATS))

        return format


    @classmethod
    def _load_csv(cls, source):
        return cls._load_sv(source, separator=",")

    @classmethod
    def _load_tsv(cls, source):
        return cls._load_sv(source, separator="\t")

    @classmethod
    def _load_sv(cls, source, separator):
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

    @classmethod
    def _load_numl(cls, source):
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
        doc_numl = libnuml.readNUMLFromFile(source)
        # FIXME: show parsing errors

        print('source:', source, doc_numl)

        # reads all the resultComponents from the numl file
        results = []

        Nrc = doc_numl.getNumResultComponents()
        rcs = doc_numl.getResultComponents()

        print('NumResultComponents:', Nrc)
        for k in range(Nrc):
            # parse ResultComponent
            res_comp = rcs.get(k)

            # dimension info
            dim_description = res_comp.getDimensionDescription()
            print("DimensionDescription:", dim_description)
            assert (isinstance(dim_description, libnuml.DimensionDescription))
            info = cls._parse_description(dim_description.get(0))
            print("info:", info)

            # data
            dim = res_comp.getDimension()
            print("Dimension:", dim)
            assert (isinstance(dim, libnuml.Dimension))
            data = cls._parse_value(dim.get(0))
            print("data", data)

            res = {'info': info, 'data': data}
            results.append(res)

        return results

    @classmethod
    def _parse_description(cls, d, info=None):
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

            info = cls._parse_description(d.get(0), info)

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

    @classmethod
    def _parse_value(cls, d, data=None):
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

            info = cls._parse_value(d.get(0), data)

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

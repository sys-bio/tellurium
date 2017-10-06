"""
Reading NUML, CSV and TSV data from DataDescriptions
"""
from __future__ import print_function, absolute_import
import os
import logging
import warnings
import tempfile
import numpy as np
import pandas as pd

# py2 / py3
try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    import libnuml
except ImportError:
    import tenuml as libnuml

log = logging.getLogger('sedml-data')


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

        # TODO: refactor in general resource module (for resolving anyURI and resource)
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

        # log data description
        log.info('-' * 80)
        log.info('DataDescription: :', dd)
        log.info('\tid:', did)
        log.info('\tname:', name)
        log.info('\tsource', source)
        log.info('\tformat', format)

        # -------------------------------
        # Parse DimensionDescription
        # -------------------------------
        # FIXME: uses the data_types to check the actual data type
        dim_description = dd.getDimensionDescription()
        if dim_description is not None:
            data_types = cls.parse_dimension_description(dim_description)
        else:
            data_types = None

        # -------------------------------
        # Load complete data
        # -------------------------------
        data = None
        if format == cls.FORMAT_CSV:
            data = cls._load_csv(path=source_path)
        elif format == cls.FORMAT_TSV:
            data = cls._load_tsv(path=source_path)
        elif format == cls.FORMAT_NUML:
            data = cls._load_numl(path=source_path)

        # log data
        log.info("-" * 80)
        log.info("Data")
        log.info("-" * 80)
        if format in [cls.FORMAT_CSV, cls.FORMAT_TSV]:
            log.info(data.head(10))
        elif format == cls.FORMAT_NUML:
            # multiple result components via id
            for result in data:
                log.info(result[0])           # rc id
                log.info(result[1].head(10))  # DataFrame
        log.info("-" * 80)

        # -------------------------------
        # Process DataSources
        # -------------------------------
        data_sources = {}
        for k, ds in enumerate(dd.getListOfDataSources()):

            dsid = ds.getId()

            # log DataSource
            log.info('\n\t*** DataSource:', ds)
            log.info('\t\tid:', ds.getId())
            log.info('\t\tname:', ds.getName())
            log.info('\t\tindexSet:', ds.getIndexSet())
            log.info('\t\tslices')

            # CSV/TSV
            if format in [cls.FORMAT_CSV, cls.FORMAT_TSV]:
                if len(ds.getIndexSet()) > 0:
                    # if index set we return the index
                    data_sources[dsid] = pd.Series(data.index.tolist())
                else:
                    sids = []
                    for slice in ds.getListOfSlices():
                        # FIXME: this does not handle multiple slices for rows
                        # print('\t\t\treference={}; value={}'.format(slice.getReference(), slice.getValue()))
                        sids.append(slice.getValue())

                    # slice values are columns from data frame
                    try:
                        data_sources[dsid] = data[sids].values
                    except KeyError as e:
                        # something does not fit between data and data sources
                        print("-" * 80)
                        print("Format:", format)
                        print("Source:", source_path)
                        print("-" * 80)
                        print(data)
                        print("-" * 80)
                        raise

            # NUML
            elif format == cls.FORMAT_NUML:
                # Using the first results component only in SED-ML L1V3
                rc_id, rc, data_types = data[0]

                index_set = ds.getIndexSet()
                if ds.getIndexSet() and len(ds.getIndexSet()) != 0:
                    # data via indexSet
                    data_source = rc[index_set].drop_duplicates()
                    data_sources[dsid] = data_source
                else:
                    # data via slices
                    for slice in ds.getListOfSlices():
                        reference = slice.getReference()
                        value = slice.getValue()
                        df = rc.loc[rc[reference] == value]
                        # select last column with values
                        data_sources[dsid] = df.iloc[:, -1]

        # log data sources
        log.info("-" * 80)
        log.info("DataSources")
        log.info("-" * 80)
        for key, value in data_sources.items():
            log.info('{} : {}; shape={}'.format(key, type(value), value.shape))
        log.info("-" * 80)

        # cleanup
        # FIXME: handle in finally
        if tmp_file is not None:
            os.remove(tmp_file)

        return data_sources

    @classmethod
    def _determine_format(cls, source_path, format=None):
        """

        :param source_path: path of file
        :param format: format given in the DataDescription
        :return:
        """
        if format is None or format == "":
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
            raise NotImplementedError("Format '{}' not supported for DataDescription. Format must be in: {}".format(format, cls.SUPPORTED_FORMATS))

        return format

    @classmethod
    def _load_csv(cls, path):
        """ Read CSV data from file.

        :param path: path of file
        :return: returns pandas DataFrame with data
        """
        return cls._load_sv(path, separator=",")

    @classmethod
    def _load_tsv(cls, path):
        """ Read TSV data from file.

                :param path: path of file
                :return: returns pandas DataFrame with data
                """
        return cls._load_sv(path, separator="\t")

    @classmethod
    def _load_sv(cls, path, separator):
        """ Helper function for loading data file from given source.

        CSV files must have a header. Handles file and online resources.

        :param path: path of file.
        :return: pandas data frame
        """
        df = pd.read_csv(path, sep=separator,
                         index_col=False,
                         skip_blank_lines=True,
                         quotechar='"',
                         comment="#",
                         skipinitialspace=True,
                         na_values="nan")
        return df

    @classmethod
    def read_numl_document(cls, path):
        """ Helper to read numl document and checking errors

        :param path: path of file
        :return:
        """
        doc_numl = libnuml.readNUMLFromFile(path)  # type: libnuml.NUMLDocument

        # check for errors
        errorlog = doc_numl.getErrorLog()
        msg = "NUML ERROR in '{}': {}".format(path, errorlog.toString())
        if errorlog.getNumFailsWithSeverity(libnuml.LIBNUML_SEV_ERROR) > 0:
            raise IOError(msg)
        if errorlog.getNumFailsWithSeverity(libnuml.LIBNUML_SEV_FATAL) > 0:
            raise IOError(msg)
        if errorlog.getNumFailsWithSeverity(libnuml.LIBNUML_SEV_WARNING) > 0:
            warnings.warn(msg)
        if errorlog.getNumFailsWithSeverity(libnuml.LIBNUML_SEV_SCHEMA_ERROR) > 0:
            warnings.warn(msg)
        if errorlog.getNumFailsWithSeverity(libnuml.LIBNUML_SEV_GENERAL_WARNING) > 0:
            warnings.warn(msg)

        return doc_numl

    @classmethod
    def _load_numl(cls, path):
        """ Reading NuML data from file.

        This loads the complete numl data.
        For more information see: https://github.com/numl/numl

        :param path: NuML path
        :return: data
        """
        doc_numl = DataDescriptionParser.read_numl_document(path)

        # reads all the resultComponents from the numl file
        results = []

        Nrc = doc_numl.getNumResultComponents()
        rcs = doc_numl.getResultComponents()

        log.info('\nNumResultComponents:', Nrc)
        for k in range(Nrc):
            rc = rcs.get(k)  # parse ResultComponent
            rc_id = rc.getId()

            # dimension info
            description = rc.getDimensionDescription()
            data_types = cls.parse_dimension_description(description)

            # data
            dimension = rc.getDimension()
            assert (isinstance(dimension, libnuml.Dimension))
            data = [cls._parse_dimension(dimension.get(k)) for k in range(dimension.size())]

            # create data frame
            flat_data = []
            for entry in data:
                for part in entry:
                    flat_data.append(part)

            # column ids from DimensionDescription
            column_ids = []
            for entry in data_types:
                for cid, dtype in entry.items():
                    column_ids.append(cid)

            df = pd.DataFrame(flat_data, columns=column_ids)

            # convert data types to actual data types
            for entry in data_types:
                for cid, dtype in entry.items():
                    if dtype == 'double':
                        df[cid] = df[cid].astype(np.float64)
                    elif dtype == 'string':
                        df[cid] = df[cid].astype(str)

            # convert all the individual columns to the corresponding data types
            # df = df.apply(pd.to_numeric, errors="ignore")

            results.append([rc_id, df, data_types])

        return results


    @classmethod
    def parse_dimension_description(cls, description):
        """ Parses the given dimension description.

        Returns dictionary of { key: dtype }

        :param description:
        :return:
        """
        assert (isinstance(description, libnuml.DimensionDescription))
        info = [cls._parse_description(description.get(k)) for k in range(description.size())]

        flat_info = []
        for entry in info:
            for part in entry:
                flat_info.append(part)

        return flat_info

    @classmethod
    def _parse_description(cls, d, info=None, entry=None):
        """ Parses the recursive DimensionDescription, TupleDescription, AtomicDescription.

        This gets the dimension information from NuML.

          <dimensionDescription>
            <compositeDescription indexType="double" id="time" name="time">
              <compositeDescription indexType="string" id="SpeciesIds" name="SpeciesIds">
                <atomicDescription valueType="double" id="Concentrations" name="Concentrations" />
              </compositeDescription>
            </compositeDescription>
          </dimensionDescription>

        :param d:
        :param info:
        :return:
        """
        if info is None:
            info = []
        if entry is None:
            entry = []

        type_code = d.getTypeCode()
        # print('typecode:', type_code)

        if type_code == libnuml.NUML_COMPOSITEDESCRIPTION:
            content = {d.getId(): d.getIndexType()}
            info.append(content)
            # print('\t* CompositeDescription:', content)
            if d.isContentCompositeDescription():
                for k in range(d.size()):
                    info = cls._parse_description(d.getCompositeDescription(k), info, list(entry))
            elif d.isContentAtomicDescription():
                info = cls._parse_description(d.getAtomicDescription(), info, entry)

        elif type_code == libnuml.NUML_ATOMICDESCRIPTION:
            content = {d.getId(): d.getValueType()}
            info.append(content)
            # print('\t* AtomicDescription:', content)

        elif type_code == libnuml.NUML_TUPLEDESCRIPTION:
            tuple_des = d.getTupleDescription()
            Natomic = d.size()
            valueTypes = []
            for k in range(Natomic):
                atomic = tuple_des.getAtomicDescription(k)
                valueTypes.append(atomic.getValueType())

            info.append(valueTypes)
            # print('\t* TupleDescription:', valueTypes)

        else:
            raise NotImplementedError("Type code: {}".format(type_code))

        return info

    @classmethod
    def _parse_dimension(cls, d, data=None, entry=None):
        """ Parses the recursive CompositeValue, Tuple, AtomicValue.

        This gets the actual data from NuML.

        :param d:
        :param data:
        :return:
        """
        if data is None:
            data = []
        if entry is None:
            entry = []

        type_code = d.getTypeCode()
        # print('typecode:', type_code)

        if type_code == libnuml.NUML_COMPOSITEVALUE:
            indexValue = d.getIndexValue()
            entry.append(indexValue)
            # print('\t* CompositeValue:', indexValue)

            if d.isContentCompositeValue():
                for k in range(d.size()):
                    # make copy, so every entry is own entry
                    data = cls._parse_dimension(d.getCompositeValue(k), data, list(entry))
            elif d.isContentAtomicValue():
                data = cls._parse_dimension(d.getAtomicValue(), data, entry)

        elif type_code == libnuml.NUML_ATOMICVALUE:
            # Data is converted to correct
            # value = d.getDoubleValue()
            value = d.getValue()
            entry.append(value)
            # entry finished, we are appending
            data.append(entry)
            # print('\t* AtomicValue:', value)

        elif type_code == libnuml.NUML_TUPLE:
            tuple = d.getTuple()
            Natomic = d.size()
            values = []
            for k in range(Natomic):
                atomic = tuple.getAtomicValue(k)
                values.append(atomic.getDoubleValue())

            data.append(values)
            # print('\t* TupleDescription:', values)

        else:
            raise NotImplementedError

        return data

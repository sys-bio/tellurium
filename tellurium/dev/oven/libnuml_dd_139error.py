from __future__ import print_function

try:
    import libsedml
except ImportError:
    import tesedml as libsedml

try:
    import libnuml
except ImportError:
    import tenuml as libnuml


class ErrorTest(object):
    @classmethod
    def parseDataDescriptions(cls, sedml_path):
        """ Test helper functions.

        Tries to parse all DataDescriptions in the SED-ML file.
        """
        print('parseDataDescriptions:', sedml_path)
        doc_sedml = libsedml.readSedMLFromFile(sedml_path)

        # parse DataDescriptions
        list_dd = doc_sedml.getListOfDataDescriptions()
        for dd in list_dd:
            dim_description = dd.getDimensionDescription()

            # This results in:
            #   Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
            data_types = None
            print(dim_description)
            if dim_description is not None:
                data_types = cls.parse_dimension_description(dim_description)
            print(data_types)

    @classmethod
    def parse_dimension_description(cls, description):
        """ Parses the given dimension description.

        Returns dictionary of { key: dtype }

        :param description:
        :return:
        """
        print('parse_dimension_description:', description)
        assert (isinstance(description, libnuml.DimensionDescription))
        # !THIS IS WRONG: 3929155189, probably not set
        print(description.size())
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
        print('typecode:', type_code)

        if type_code == libnuml.NUML_COMPOSITEDESCRIPTION:
            content = {d.getId(): d.getIndexType()}
            info.append(content)
            print('\t* CompositeDescription:', content)
            if d.isContentCompositeDescription():
                for k in range(d.size()):
                    info = cls._parse_description(d.getCompositeDescription(k), info, list(entry))
            elif d.isContentAtomicDescription():
                info = cls._parse_description(d.getAtomicDescription(), info, entry)

        elif type_code == libnuml.NUML_ATOMICDESCRIPTION:
            content = {d.getId(): d.getValueType()}
            info.append(content)
            print('\t* AtomicDescription:', content)

        elif type_code == libnuml.NUML_TUPLEDESCRIPTION:
            tuple_des = d.getTupleDescription()
            Natomic = d.size()
            valueTypes = []
            for k in range(Natomic):
                atomic = tuple_des.getAtomicDescription(k)
                valueTypes.append(atomic.getValueType())

            info.append(valueTypes)
            print('\t* TupleDescription:', valueTypes)

        else:
            raise NotImplementedError("Type code: {}".format(type_code))

        return info


if __name__ == "__main__":
    sedml_file = "reading-numlData1D.xml"
    ErrorTest.parseDataDescriptions(sedml_file)


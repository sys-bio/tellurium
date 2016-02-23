"""
Tellurium SED-ML support.

This module reads SED-ML files ('.sedml' extension) or archives ('.sedx' extension)
and generates executable python code.
To work with phrasedml files convert these to SED-ML first (see `tephrasedml.py`).

::

    # execute example sedml
    import tellurium.tesedml as s2p
    ret = s2p.sedmlToPython('example.sedml')
    exec ret

    # execute sedml archive (sedx)
    import SedmlToRr as s2p
    ret = s2p.sedmlToPython("example.sedx")
    exec ret


SED-ML is build of five main classes, which are translated in python code:
    the Model Class,
    the Simulation Class,
    the Task Class,
    the DataGenerator Class,
    and the Output Class.

The Model Class
    The Model class is used to reference the models used in the simulation experiment.
    SED-ML itself is independent of the model encoding underlying the models. The only
    requirement is that the model needs to be referenced by using an unambiguous identifier
    which allows for finding it, for example using a MIRIAM URI. To specify the language in
    which the model is encoded, a set of predefined language URNs is provided.
    The SED-ML Change class allows the application of changes to the referenced models,
    including changes on the XML attributes, e.g. changing the value of an observable,
    computing the change of a value using mathematics, or general changes on any XML element
    of the model representation that is addressable by XPath expressions, e.g. substituting
    a piece of XML by an updated one.

The Simulation Class
    The Simulation class defines the simulation settings and the steps taken during simulation.
    These include the particular type of simulation and the algorithm used for the execution of
    the simulation; preferably an unambiguous reference to such an algorithm should be given,
    using a controlled vocabulary, or ontologies. One example for an ontology of simulation
    algorithms is the Kinetic Simulation Algorithm Ontology KiSAO. Further information encodable
    in the Simulation class includes the step size, simulation duration, and other
    simulation-type dependent information.

The Task Class
    SED-ML makes use of the notion of a Task class to combine a defined model (from the Model class)
    and a defined simulation setting (from the Simulation class). A task always holds one reference each.
    To refer to a specific model and to a specific simulation, the corresponding IDs are used.

The DataGenerator Class
    The raw simulation result sometimes does not correspond to the desired output of the simulation,
    e.g. one might want to normalise a plot before output, or apply post-processing like mean-value calculation.
    The DataGenerator class allows for the encoding of such post-processings which need to be applied to the
    simulation result before output. To define data generators, any addressable variable or parameter
    of any defined model (from instances of the Model class) may be referenced, and new entities might
    be specified using MathML definitions.

The Output Class
    The Output class defines the output of the simulation, in the sense that it specifies what shall be
    plotted in the output. To do so, an output type is defined, e.g. 2D-plot, 3D-plot or data table,
    and the according axes or columns are all assigned to one of the formerly specified instances
    of the DataGenerator class.
"""
from __future__ import print_function, division
import os
import warnings
import libsedml
import libsbml
import zipfile

# TODO: handle combine archives with multiple SEDML-Files


def sedml_to_python(input):
    """ Convert sedml file to python code.

    Deprecated: use sedmlToPython()

    :param inputstring:
    :type inputstring:
    :return:
    :rtype:
    """
    warnings.warn('Use sedmlToPython instead, will be removed in v1.4',
                  DeprecationWarning, stacklevel=2)
    return sedmlToPython(input)


def sedmlToPython(input):
    """ Convert sedml file to python code.

    :param inputstring: full path name to SedML model or SED-ML string
    :type inputstring: path
    :return: contents
    :rtype:
    """
    factory = SEDMLCodeFactory(input)
    return factory.toPython()


class SEDMLCodeFactory(object):
    """ Code Factory generating executable code. """

    # possible input types to the factory
    INPUT_TYPE_STR = 'SEDML_STRING'
    INPUT_TYPE_FILE_SEDML = 'SEDML_FILE'
    INPUT_TYPE_FILE_COMBINE = 'COMBINE_FILE'  # includes .sedx archives

    def __init__(self, input, workingDir=None):
        """ Create CodeFactory for given input.
        :param input:
        :type input:
        :return:
        :rtype:
        """
        self.input = input
        self.inputType = None

        # where do we work
        if workingDir is None:
            workingDir = os.getcwd()
        self.workingDir = workingDir

        # read sedml
        self._readSEDMLDocument()
        if self.sedmlDoc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_ERROR) > 0:
            raise IOError(self.sedmlDoc.getErrorLog().toString())

    def __str__(self):
        """ Print Input
        :return:
        :rtype:
        """
        lines = [
            '{}'.format(self.__class__),
            'sedmlDoc: {}'.format(self.sedmlDoc),
            'workingDir: {}'.format(self.workingDir),
            'inputType: {}'.format(self.inputType)
        ]
        if self.inputType != self.INPUT_TYPE_STR:
            lines.append('input: {}'.format(self.input))
        return '\n'.join(lines)

    def _readSEDMLDocument(self):
        """ Parses the SedMLDocument from given input.

        Necessary to find out the respective type of the input and set
        the path information respectively.

        :return:
        :rtype:
        """
        # SEDML-String
        try:
            from xml.etree import ElementTree
            x = ElementTree.fromstring(self.input)
            # is parsable xml string
            self.sedmlDoc = libsedml.readSedMLFromString(self.input)
            self.inputType = self.__class__.INPUT_TYPE_STR

        # SEDML-File
        except ElementTree.ParseError:
            if not os.path.exists(input):
                raise IOError("File not found:", input)

            filename, extension = os.path.splitext(os.path.basename(self.input))

            # SEDML file
            if extension == ".sedml":
                self.sedmlDoc = libsedml.readSedMLFromFile(self.input)
                self.inputType = self.__class__.INPUT_TYPE_FILE_SEDML
                # working directory is where the sedml file is
                self.workingDir = os.path.dirname(os.path.realpath(input))

            # Archive
            elif zipfile.is_zipfile(self.input):
                # in case of sedx and combine a working directory has to be
                # created where the files are extracted to
                self.workingDir = os.path.join(self.workingDir, '_te_{}'.format(filename))
                # extract the archive to working directory
                self.__extractArchive(self.input, self.workingDir)
                # get SEDML files from archive
                sedmlFiles = self.__sedmlFilesFromArchive(self.workingDir)
                print(sedmlFiles)
                # FIXME: there could be multiple SEDML files in archive (currently only first used)
                self.sedmlDoc = libsedml.readSedMLFromString(sedmlFiles[0])
                self.inputType = self.__class__.INPUT_TYPE_FILE_COMBINE

    @staticmethod
    def __extractArchive(archivePath, directory):
        """ Extracts given archive into the target directory.

        :param archivePath:
        :type archivePath:
        :param directory:
        :type directory:
        :return:
        :rtype:
        """
        # FIXME: refactor in tecombine (generic archive function)
        zip = zipfile.ZipFile(archivePath, 'r')

        if not os.path.isdir(directory):
            os.makedirs(directory)

        for each in zip.namelist():
            # check if the item includes a subdirectory
            # if it does, create the subdirectory in the output folder and write the file
            # otherwise, just write the file to the output folder
            if not each.endswith('/'):
                root, name = os.path.split(each)
                directory = os.path.normpath(os.path.join(directory, root))
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                file(os.path.join(directory, name), 'wb').write(zip.read(each))
        zip.close()

    @staticmethod
    def __filePathsFromExtractedArchive(directory, formatType='sed-ml'):
        """ Reads file paths from extracted combine archive.
        Searches the manifest.xml of the archive for files of the
        specified formatType and checks if the files exist in the directory.

        Supported formatTypes are:
            'sed-ml' : SED-ML files
            'sbml' : SBML files

        :param directory: directory of extracted archive
        :return: list of paths
        :rtype: list
        """
        import xml.etree.ElementTree as et
        filePaths = []
        tree = et.parse(os.path.join(directory + "manifest.xml"))
        root = tree.getroot()
        print(root)
        for child in root:
            format = child.attrib['format']
            if format.endswith(formatType):
                location = child.attrib['location']

                # real path
                fpath = os.path.join(directory, location)
                if not os.path.exists(fpath):
                    raise IOError('Path specified in manifest.xml does not exist in archive: {}'.format(fpath))
                filePaths.append(fpath)
        return filePaths


    def toPython(self):
        """ Create python code and return.

        Renders the respective template.

        :return:
        :rtype:
        """



if __name__ == "__main__":
    input = "app2sim.sedml"
    factory = SEDMLCodeFactory(input)
    print(factory)
    # sedmlToPython(input)

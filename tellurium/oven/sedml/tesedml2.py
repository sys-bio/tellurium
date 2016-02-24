# -*- coding: utf-8 -*-
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
import sys
import warnings
import libsedml
import libsbml
from jinja2 import Environment, FileSystemLoader
import zipfile
import sedmlfilters
from tellurium import getTelluriumVersion
import datetime


# Change default encoding to UTF-8
# We need to reload sys module first, because setdefaultencoding is available only at startup time
reload(sys)
sys.setdefaultencoding('utf-8')


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


def sedmlToPython(inputStr):
    """ Convert sedml file to python code.

    :param inputstring: full path name to SedML model or SED-ML string
    :type inputstring: path
    :return: contents
    :rtype:
    """
    factory = SEDMLCodeFactory(inputStr)
    return factory.toPython()


class SEDMLTools(object):
    """ Helper functions to work with sedml. """

    INPUT_TYPE_STR = 'SEDML_STRING'
    INPUT_TYPE_FILE_SEDML = 'SEDML_FILE'
    INPUT_TYPE_FILE_COMBINE = 'COMBINE_FILE'  # includes .sedx archives

    @classmethod
    def checkSEDMLDocument(cls, doc):
        """ Checks the SedDocument for errors.
        Raises IOError if error exists.
        :param doc:
        :type doc:
        """
        if doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_ERROR) > 0:
            raise IOError(doc.getErrorLog().toString())

    @classmethod
    def readSEDMLDocument(cls, inputStr):
        """ Parses SedMLDocument from given input.

        :return: dictionary of SedDocument, inputType and working directory.
        :rtype: {doc, inputType, workingDir}
        """
        # SEDML-String
        try:
            from xml.etree import ElementTree
            x = ElementTree.fromstring(inputStr)
            # is parsable xml string
            doc = libsedml.readSedMLFromString(inputStr)
            inputType = cls.INPUT_TYPE_STR

        # SEDML-File
        except ElementTree.ParseError:
            if not os.path.exists(inputStr):
                raise IOError("File not found:", inputStr)

            filename, extension = os.path.splitext(os.path.basename(inputStr))

            # SEDML file
            if extension in [".sedml", '.xml']:
                inputType = cls.INPUT_TYPE_FILE_SEDML
                doc = libsedml.readSedMLFromFile(inputStr)
                cls.checkSEDMLDocument(doc)
                # working directory is where the sedml file is
                workingDir = os.path.dirname(os.path.realpath(inputStr))

            # Archive
            elif zipfile.is_zipfile(inputStr):
                archive = inputStr
                inputType = cls.INPUT_TYPE_FILE_COMBINE

                # in case of sedx and combine a working directory is created
                # in which the files are extracted
                workingDir = os.path.join(os.path.dirname(os.path.realpath(inputStr)), '_te_{}'.format(filename))
                # extract the archive to working directory
                cls.extractArchive(archive, workingDir)
                # get SEDML files from archive
                # FIXME: there could be multiple SEDML files in archive (currently only first used)
                sedmlFiles = cls.filePathsFromExtractedArchive(workingDir)
                print('sedml files in archive:', sedmlFiles)
                if len(sedmlFiles) == 0:
                    raise IOError("No SEDML files found in archive.")
                if len(sedmlFiles) > 1:
                    warnings.warn("More than 1 sedml file in archive, only processing first one.")
                doc = libsedml.readSedMLFromFile(sedmlFiles[0])
                cls.checkSEDMLDocument(doc)

        return {'doc': doc,
                'inputType': inputType,
                'workingDir': workingDir}

    @staticmethod
    def extractArchive(archivePath, directory):
        """ Extracts given archive into the target directory.

        :param archivePath:
        :type archivePath:
        :param directory:
        :type directory:
        :return:
        :rtype:
        """
        zip = zipfile.ZipFile(archivePath, 'r')

        if not os.path.isdir(directory):
            os.makedirs(directory)
        else:
            warnings.warn("Folder for combine archive already exists:{}".format(directory))

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
    def filePathsFromExtractedArchive(directory, formatType='sed-ml'):
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

        filePaths = []

        manifest = os.path.join(directory, "manifest.xml")
        if os.path.exists(manifest):
            # get the sedml files from the manifest
            import xml.etree.ElementTree as et
            tree = et.parse(manifest)
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
        else:
            # no manifest (use all sedml files in folder)
            warnings.warn("No 'manifest.xml' in archive, using all '*.sedml' files.")
            for fname in os.listdir(directory):
                if fname.endswith(".sedml") or fname.endswith(".sedx.xml"):
                    filePaths.append(os.path.join(directory, fname))

        return filePaths


    @staticmethod
    def resolveModelChanges(doc):
        """ Resolves the original source model and full change lists for models.

         Going through the tree of model upwards until root is reached and
         collecting changes on the way (example models m* and changes c*)
         m1 (source) -> m2 (c1, c2) -> m3 (c3, c4)
         resolves to
         m1 (source) []
         m2 (source) [c1,c2]
         m3 (source) [c1,c2,c3,c4]
         The order of changes is important (at least between nodes on different
         levels of hierarchies), because later changes of derived models could
         reverse earlier changes.

         Uses recursive search strategy, which should be okay as long as the model tree hierarchy is
         not getting to big.
         """
        # initial dicts (handle source & change information for single node)
        model_sources = {}
        model_changes = {}

        for m in doc.getListOfModels():
            mid = m.getId()
            source = m.getSource()
            model_sources[mid] = source
            changes = []
            # store the changes unique for this model
            for c in m.getListOfChanges():
                changes.append(c)
            model_changes[mid] = changes

        # recursive search for original model and store the
        # changes which have to be applied in the list of changes
        def findSource(mid, changes):

            # mid is node above
            if mid in model_sources:
                # add changes for node
                for c in model_changes[mid]:
                    changes.append(c)
                # keep looking deeper
                return findSource(model_sources[mid], changes)
            # the source is no longer a key in the sources, it is the source
            return mid, changes

        all_changes = {}

        mids = [m.getId() for m in doc.getListOfModels()]
        for mid in mids:
            source, changes = findSource(mid, changes=list())
            model_sources[mid] = source
            all_changes[mid] = changes[::-1]

        print(model_sources)
        print(all_changes)
        return model_sources, all_changes


    def applyChangeToXML(self):
        # TODO: implement
        pass


class SEDMLCodeFactory(object):
    """ Code Factory generating executable code. """

    # template location
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

    def __init__(self, inputStr):
        """ Create CodeFactory for given input.
        :param inputStr:
        :type inputStr:
        :return:
        :rtype:
        """
        self.inputStr = inputStr
        info = SEDMLTools.readSEDMLDocument(inputStr)
        self.doc = info['doc']
        self.inputType = info['inputType']
        self.workingDir = info['workingDir']

        # parse the models & prepare for roadrunner
        # TODO: implement

        SEDMLTools.resolveModelChanges(self.doc)



    def __str__(self):
        """ Print Input
        :return:
        :rtype:
        """
        lines = [
            '{}'.format(self.__class__),
            'doc: {}'.format(self.doc),
            'workingDir: {}'.format(self.workingDir),
            'inputType: {}'.format(self.inputType)
        ]
        if self.inputType != SEDMLTools.INPUT_TYPE_STR:
            lines.append('input: {}'.format(self.inputStr))
        return '\n'.join(lines)

    def _parseSEDMLModels(self):
        """
        :return:
        :rtype:
        """
        # TODO: implement
        pass

    def _loadModel(self):
        """ Load model. """
        # TODO: implement
        pass
        """
        string = currentModel.getSource()
        string = string.replace("\\", "/")
        if isId(string):                             # it's the Id of a model
            originalModel = sedmlDoc.getModel(string)
            if originalModel is not None:
                string = originalModel.getSource()          #  !!! for now, we reuse the original model to which the current model is referring to
            else:
                pass
        if string.startswith("."):                  # relative location, we trust it but need it trimmed
            if string.startswith("../"):
                string = string[3:]
            elif string.startswith("./"):
                string = string[2:]
            print(rrName + ".load('" + path.replace("\\","/") + string + "')")    # SBML model name recovered from "source" attr
            #from os.path import expanduser
            #path = expanduser("~")
            #print(rrName + ".load('" + path + "\\" + string + "')")    # SBML model name recovered from "source" attr
        elif "\\" or "/" or "urn:miriam" not in string:
            print(rrName + ".load('" + path.replace("\\","/") + string + "')")
        elif string.startswith("urn:miriam"):
            print("Downloading model from BioModels Database...")
            astr = string.rsplit(':', 1)
            astr = astr[1]
            string = path + astr + ".xml"
            if not os.path.exists(string):
                conn = httplib.HTTPConnection("www.ebi.ac.uk")
                conn.request("GET", "/biomodels-main/download?mid=" + astr)
                r1 = conn.getresponse()
                #print(r1.status, r1.reason)
                data1 = r1.read()
                conn.close()
                f1 = open(string, 'w')
                f1.write(data1)
                f1.close()
            else:
                pass
            print(rrName + ".load('" + string +"'))")
        else:         # assume absolute path pointing to hard disk location
            string = string.replace("\\", "/")
            print(rrName + ".load('" + string + "')")

        """

    def _parseSimulations(self):
        # TODO: implement
        pass

    def toPython(self, python_template='tesedml_template.py'):
        """ Create python code by rendering the python template.
        Uses the information in the SED-ML document to create
        python code

        Renders the respective template.

        :return: returns the rendered template
        :rtype: str
        """
        # template environment
        env = Environment(loader=FileSystemLoader(self.TEMPLATE_DIR),
                             extensions=['jinja2.ext.autoescape'],
                             trim_blocks=True,
                             lstrip_blocks=True)

        # additional filters
        for key in sedmlfilters.filters:
             env.filters[key] = getattr(sedmlfilters, key)
        template = env.get_template(python_template)

        # timestamp
        time = datetime.datetime.now()
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%S')

        # Context
        c = {
            'version': getTelluriumVersion(),
            'timestamp': timestamp,
            'factory': self,
            'doc': self.doc
        }
        return template.render(c)

    def executePython(self):
        """ Executes created python code.
        See :func:`createpython`
        """
        execStr = self.toPython()
        try:
            # This calls exec. Be very sure that nothing bad happens here.
            exec execStr
        except Exception as e:
            raise e


if __name__ == "__main__":
    import os
    from tellurium.tests.testdata import sedmlDir, sedxDir, psedmlDir

    # test file
    sedml_input = os.path.join(sedmlDir, 'app2sim.sedml')
    # resolve models
    factory = SEDMLCodeFactory(sedml_input)

    # test file
    sedml_input = os.path.join(sedxDir, 'app2sim.sedx')
    # resolve models
    factory = SEDMLCodeFactory(sedml_input)

    # ------------------------------------------------------
    def testInput(sedmlInput):
        """ Test function run on inputStr. """
        print('\n', '*'*100)
        print(sedmlInput)
        print('*'*100)
        factory = SEDMLCodeFactory(sedmlInput)
        print(factory)

    # ------------------------------------------------------
    # Check sed-ml files
    for fname in sorted(os.listdir(sedmlDir)):
        if fname.endswith(".sedml"):
            testInput(os.path.join(sedmlDir, fname))

    # Check sedx archives
    for fname in sorted(os.listdir(sedxDir)):
        if fname.endswith(".sedx"):
            testInput(os.path.join(sedxDir, fname))

    # Check phrasedml files
    for fname in sorted(os.listdir(psedmlDir)):
        if fname.endswith(".psedml"):
            pass
            # testInput(os.path.join(psedmlDir, fname))

    # ------------------------------------------------------

    """
    python_str = factory.toPython()

    print('#'*80)
    print(python_str)
    print('#'*80)

    factory.executePython()
    """

    """
    sim = libsedml.SedSimulation()
    sim.getTypeCode()
    libsedml.SEDML_SIMULATION_ONESTEP
    """

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
from tellurium.tecombine import CombineTools


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
                CombineTools.extractArchive(archive, workingDir)
                # get SEDML files from archive
                # FIXME: there could be multiple SEDML files in archive (currently only first used)
                sedmlFiles = CombineTools.filePathsFromExtractedArchive(workingDir)
                if len(sedmlFiles) == 0:
                    raise IOError("No SEDML files found in archive.")
                if len(sedmlFiles) > 1:
                    warnings.warn("More than one sedml file in archive, only processing first one.")
                doc = libsedml.readSedMLFromFile(sedmlFiles[0])
                cls.checkSEDMLDocument(doc)

        return {'doc': doc,
                'inputType': inputType,
                'workingDir': workingDir}


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

        return model_sources, all_changes


    @staticmethod
    def resolveSimulations(doc):
        """ Resolves all the settings for the simulation.

        The parsed algorithm settings are stores in dictionaries which allow than to
        easily set the simulation options and the integrator settings.
        Two dictionaries are created:
            simulate_settings: keyword arguments for simulate
            integrator_setting

        :return:
        :rtype:
        """
        sids = [sim.getId() for sim in doc.getListOfSimulations()]
        print(sids)
        simulate_settings = {}
        integrator_settings = {}
        algorithms = {}
        for sim in doc.getListOfSimulations():
            sid = sim.getId()
            alg = sim.getAlgorithm()
            algorithms[sid] = alg
            kisaoId = alg.getKisaoID()
            print(kisaoId)

        print(algorithms)

        return None


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

        # parse the models (resolve the source models & the applied changes for all models)
        model_sources, model_changes =SEDMLTools.resolveModelChanges(self.doc)
        self.model_sources = model_sources
        self.model_changes = model_changes

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
        env.globals['modelChangeToPython'] = self.modelChangeToPython

        # timestamp
        time = datetime.datetime.now()
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%S')

        # Context
        c = {
            'version': getTelluriumVersion(),
            'timestamp': timestamp,
            'factory': self,
            'doc': self.doc,
            'model_sources': self.model_sources,
            'model_changes': self.model_changes,
        }
        return template.render(c)

    # <CHANGE>
    # SEDML_CHANGE_ATTRIBUTE = _libsedml.SEDML_CHANGE_ATTRIBUTE
    # SEDML_CHANGE_REMOVEXML = _libsedml.SEDML_CHANGE_REMOVEXML
    # SEDML_CHANGE_COMPUTECHANGE = _libsedml.SEDML_CHANGE_COMPUTECHANGE
    # SEDML_CHANGE_ADDXML = _libsedml.SEDML_CHANGE_ADDXML
    # SEDML_CHANGE_CHANGEXML = _libsedml.SEDML_CHANGE_CHANGEXML

    @staticmethod
    def modelChangeToPython(model, change):
        """ Creates the apply change python string for given model and change.

        Currently only a very limited subset of model changes is supported.
        Namely changes of parameters and concentrations within a SedChangeAttribute.

        :param model: given model
        :type model: SedModel
        :param change: model change
        :type change: SedChange
        :return:
        :rtype: str
        """
        # FIXME: getting of sids, pids not very robust
        lines = []
        mid = model.getId()

        # is a libsedml.SedChangeAttribute instance
        if change.getTypeCode() == libsedml.SEDML_CHANGE_ATTRIBUTE:
            value = change.getNewValue()
            target = change.getTarget()
            lines.append("# {} {}".format(target, value))

            # parameter value change
            if ("model" in target) and ("parameter" in target):
                target = target.rsplit("id=\'", 1)[1]
                pid = target.rsplit("\'", 1)[0]
                s = "{}['{}'] = {}".format(mid, pid, value)
                lines.append(s)

            # species concentration change
            elif ("model" in target) and ("species" in target):
                target = target.rsplit("id=\'", 1)[1]
                sid = target.rsplit("\'", 1)[0]
                s = "{}['init([{}])'] = {}".format(mid, sid, value)
                lines.append(s)

            else:
                lines.append("# Unsupported changeAttribute target: {}".format(target))
        else:
            lines.append("# Unsupported change: {}".format(change.getElementName()))

        return '\n'.join(lines)

    @staticmethod
    def taskToPython(doc, task):
        """ Creates the simulation python code for a given task.

        handle: ".conservedMoietyAnalysis = False"

        handle steadyStateSelections & timeCourseSelections via variablesList


        cvode (19; the default for uniform time course simulations)
        gillespie (241; the default for stochastic time course simulations)
        steadystate (407; the default for steady state simulations)
        rk4 (32; 4th-order Runge-Kutta)
        rk45 (435; embedded Runge-Kutta)
        """
        # FIXME: There are many more nodes in the KISAO ontology (handle more terms)
        lines = []

        # model
        mid = task.getModelReference()
        model = doc.getModel(mid)
        sid = task.getSimulationReference()
        simulation = doc.getSimulation(sid)
        simType = simulation.getTypeCode()
        algorithm = simulation.getAlgorithm()
        kisao = algorithm.getKisaoID()

        lines.append("# {}: {}".format(str(simType), sid))

        # KISAO:0000433 : CVODE-like method
        # KISAO:0000019 : CVODE
        # KISAO:0000241 : Gillespie-like method
        # KISAO_0000064 : Runge-Kutta based method
        # KISAO_0000032 : explicit fourth-order Runge-Kutta method
        # KISAO_0000435 : embedded Runge-Kutta 5(4) method

        # Check if supported algorithm
        def isSupportedKisao(simType, kisao):
            supported = []
            if simType == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
                supported = ['KISAO:0000433', 'KISAO:0000019', 'KISAO:0000241', 'KISAO:0000032', 'KISAO:0000435', 'KISAO_0000064']
            elif simType == libsedml.SEDML_SIMULATION_ONESTEP:
                supported = ['KISAO:0000433', 'KISAO:0000019', 'KISAO:0000241', 'KISAO:0000032', 'KISAO:0000435', 'KISAO_0000064']
            elif simType == libsedml.SEDML_SIMULATION_STEADYSTATE:
                supported = ['KISAO:0000099', 'KISAO:0000407']
            return kisao in supported

        if not isSupportedKisao(simType, kisao):
            lines.append("# Unsupported KisaoID {} for Algorithm {}".format(kisao, simType))
            return

        # Set integrator
        def getIntegratorName(kisao):
            # cvode & steady state are mapped to cvode
            if kisao in ['KISAO:0000433', 'KISAO:0000019', 'KISAO:0000407']:
                return 'cvode'
            elif kisao == 'KISAO:0000241':
                return 'gillespie'
            elif kisao == 'KISAO:0000032':
                return 'rk4'
            elif kisao in ['KISAO:0000435', 'KISAO_0000064']:
                return 'rk45'
            else:
                return None

        integratorName = getIntegratorName(kisao)
        if not integratorName:
            lines.append("# No integrator for KisaoID {} in tellurium".format(kisao))
            return
        lines.append("{}.setIntegrator('{}')".format(mid, integratorName))

        # Set integrator settings (AlgorithmParameters)
        def setSettingForAlgorithmParameter(par):
            parKisao = par.getKisaoID()
            parValue = par.getValue()

            TODO:

            if key:
                lines.append("{}.getIntegrator('{}').setValue({}, {})".format(integratorName, key, value))
            if not key:
                lines.append("# Unsupported AlgorithmParameter: {} = {})".format(parKisao, parValue))


        for par in algorithm.getListOfAlgorithmParameters():
            setSettingForAlgorithmParameter(par)


        # Integrator settings & simulate call
        if simType == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
            pass
        elif simType == libsedml.SEDML_SIMULATION_ONESTEP:
            pass
        elif simType == libsedml.SEDML_SIMULATION_STEADYSTATE:
            pass
        else:
            lines.append("# Unsupported simulation: {}".format(str(simType)))

        return "\n".join(lines)

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
    python_str = factory.toPython()
    # create file
    with open(sedml_input + '.py', 'w') as f:
        f.write(python_str)

    print('#'*80)
    print(python_str)
    print('#'*80)

    factory.executePython()

    # SEDMLTools.resolveSimulations(factory.doc)
    for task in factory.doc.getListOfTasks():
        test_str = factory.taskToPython(factory.doc, task)
        print(test_str)


    exit()

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

    """

    """
    sim = libsedml.SedSimulation()
    sim.getTypeCode()
    libsedml.SEDML_SIMULATION_ONESTEP
    """

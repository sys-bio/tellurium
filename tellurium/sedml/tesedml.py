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

import sys
import warnings
import datetime
import zipfile
from collections import namedtuple
import os.path
import re
import numpy as np
from mathml import evaluateMathML, evaluableMathML

import libsedml
from jinja2 import Environment, FileSystemLoader

import tellurium as te
from tellurium.tecombine import CombineTools

try:
    # requrired imports
    import pandas
    import matplotlib.pyplot as plt
    import mpl_toolkits.mplot3d
except ImportError:
    warnings.warn("Dependencies for SEDML code generation not fullfilled.")

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


class SEDMLCodeFactory(object):
    """ Code Factory generating executable code.
        All implemented operations are supported for SBML models,
        wheras the cellml support is very limited.

        The following SED-ML constructs are currently NOT supported:
            1. XML transformation changes:
                - Change.RemoveXML
                - Change.AddXML
                - Change.ChangeXML

            2. Repeated simulations of repeated simulations

            3. Functional evaluation of MathML expressions
                - functional range
                - data generators
                - Change.ComputeChange
    """

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
        model_sources, model_changes = SEDMLTools.resolveModelChanges(self.doc)
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

    def sedmlString(self):
        """ Get the SEDML XML string of the current document.

        :return: SED-ML XML
        :rtype: str
        """
        return libsedml.writeSedMLToString(self.doc)

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
        # for key in sedmlfilters.filters:
        #      env.filters[key] = getattr(sedmlfilters, key)
        template = env.get_template(python_template)
        env.globals['modelToPython'] = self.modelToPython
        env.globals['taskToPython'] = self.taskToPython
        env.globals['dataGeneratorToPython'] = self.dataGeneratorToPython
        env.globals['outputToPython'] = self.outputToPython

        # timestamp
        time = datetime.datetime.now()
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%S')

        # Context
        c = {
            'version': te.getTelluriumVersion(),
            'timestamp': timestamp,
            'factory': self,
            'doc': self.doc,
            'model_sources': self.model_sources,
            'model_changes': self.model_changes,
        }
        try:
            pysedml = template.render(c)
        except Exception as e:
            # something went wrong in the conversion to python
            # show detailed information about the factory
            # and the libsedml document
            # msg = e.message + '\n' + self.__str__() + '\n' + libsedml.writeSedMLToString(self.doc) + '\n'
            msg = e.message
            raise type(e), type(e)(msg), sys.exc_info()[2]

        return pysedml

    def executePython(self):
        """ Executes python code.

        The python code is created during the function call.
        See :func:`createpython`
        """
        execStr = self.toPython()
        try:
            # This calls exec. Be very sure that nothing bad happens here.
            exec execStr
        except Exception as e:
            # something went wrong in the conversion to python
            # show detailed information about the factory
            # and the libsedml document
            raise type(e), type(e)('-'*80 + '\n'
                                   + self.__str__() + '\n'
                                   + '*'*80 + '\n'
                                   + execStr + '\n'
                                   + '*'*80 + '\n'
                                   + e.message + '\n'
                                   ), sys.exc_info()[2]

    def modelToPython(self, model):
        """ Python code for SedModel.

        :param model: SedModel instance
        :type model: SedModel
        :return: python str
        :rtype: str
        """
        lines = []
        mid = model.getId()
        language = model.getLanguage()
        source = self.model_sources[mid]

        def isUrn():
            return source.startswith('urn') or source.startswith('URN')

        def isHttp():
            return source.startswith('http') or source.startswith('HTTP')

        # read model
        if 'sbml' in language:
            # urn
            if isUrn():
                lines.append("import tellurium.temiriam as temiriam")
                lines.append("__{}_sbml = temiriam.getSBMLFromBiomodelsURN('{}')".format(mid, source))
                lines.append("{} = te.loadSBMLModel(__{}_sbml)".format(mid, mid))
            # http
            elif isHttp():
                lines.append("{} = te.loadSBMLModel('{}')".format(mid, source))
            # file
            else:
                if not source.endswith('.xml'):
                    # FIXME: this is a bug in how the combine archive is created (missing .xml)
                    source += '.xml'
                lines.append("{} = te.loadSBMLModel(os.path.join(workingDir, '{}'))".format(mid, source))

        elif 'cellml' in language:
            # http
            if isHttp():
                lines.append("{} = te.loadCellMLModel('{}')".format(mid, source))
            # file
            else:
                lines.append("{} = te.loadCellMLModel(os.path.join(workingDir, '{}'))".format(mid, self.model_sources[mid]))
        else:
            warnings.warn("Unsupported model language:".format(language))

        # apply model changes
        for change in self.model_changes[mid]:
            lines.extend(SEDMLCodeFactory.modelChangeToPython(model, change))

        return '\n'.join(lines)

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
        lines = []
        mid = model.getId()
        xpath = change.getTarget()

        if change.getTypeCode() == libsedml.SEDML_CHANGE_ATTRIBUTE:
            # resolve target change
            value = change.getNewValue()
            lines.append("# {} {}".format(xpath, value))
            lines.append(SEDMLCodeFactory.targetToPython(xpath, value, modelId=mid))

        elif change.getTypeCode() == libsedml.SEDML_CHANGE_COMPUTECHANGE:
            # TODO: refactor in function and reuse in SedSetValue
            variables = {}
            for par in change.getListOfParameters():
                variables[par.getId()] = par.getValue()
            for var in change.getListOfVariables():
                vid = var.getId()
                selection = SEDMLCodeFactory.resolveSelectionFromVariable(var)
                if type == "species":
                    lines.append("__var__{} = {}['[{}]']".format(vid, mid, selection.id))
                else:
                    lines.append("__var__{} = {}['{}']".format(vid, mid, selection.id))
                variables[vid] = "__var__{}".format(vid)

            # value is calculated with the current state of model
            value = evaluableMathML(change.getMath(), variables=variables)
            lines.append(SEDMLCodeFactory.targetToPython(xpath, value, modelId=mid))

        elif change.getTypeCode() in [libsedml.SEDML_CHANGE_REMOVEXML,
                                      libsedml.SEDML_CHANGE_ADDXML,
                                      libsedml.SEDML_CHANGE_CHANGEXML]:
            lines.append("# Unsupported change: {}".format(change.getElementName()))
            warnings.warn("Unsupported change: {}".format(change.getElementName()))
        else:
            lines.append("# Unsupported change: {}".format(change.getElementName()))
            warnings.warn("Unsupported change: {}".format(change.getElementName()))

        return lines

    @staticmethod
    def taskToPython(doc, task):
        """ Create python for arbitrary task (repeated or simple).

        :param doc:
        :type doc:
        :param task:
        :type task:
        :return:
        :rtype:
        """
        lines = []
        taskType = task.getTypeCode()

        # <SIMPLE TASK>
        if taskType == libsedml.SEDML_TASK:
            lines.extend(SEDMLCodeFactory.simpleTaskToPython(doc, task))
        # <REPEATED TASK>
        elif taskType == libsedml.SEDML_TASK_REPEATEDTASK:
            lines.extend(SEDMLCodeFactory.repeatedTaskToPython(doc, task))
        else:
            lines.append("# Unsupported task: {}".format(taskType))
        return '\n'.join(lines)

    @staticmethod
    def simpleTaskToPython(doc, task):
        """ Create python for simple task. """
        lines = []
        tid = task.getId()
        lines.append("{} = [None]".format(tid))
        resultVariable = "{}[0]".format(tid)
        selections = SEDMLCodeFactory.selectionsForTask(doc=doc, task=task)
        lines.extend(SEDMLCodeFactory.subtaskToPython(doc=doc, task=task,
                                                      selections=selections,
                                                      resultVariable=resultVariable))
        return lines


    @staticmethod
    def uniformRangeToPython(r):
        """ Create python lines for uniform range.
        :param r:
        :type r:
        :return:
        :rtype:
        """
        lines = []
        rId = r.getId()
        rStart = r.getStart()
        rEnd = r.getEnd()
        rPoints = r.getNumberOfPoints()+1  # One point more than number of points
        rType = r.getType()
        if rType in ['Linear', 'linear']:
            lines.append("__range__{} = list(np.linspace(start={}, stop={}, num={}))".format(rId, rStart, rEnd, rPoints))
        elif rType in ['Log', 'log']:
            lines.append("__range__{} = list(np.logspace(start={}, stop={}, num={}))".format(rId, rStart, rEnd, rPoints))
        else:
            warnings.warn("Unsupported range type in UniformRange: {}".format(rType))
        return lines

    @staticmethod
    def vectorRangeToPython(r):
        lines = []
        __range = np.zeros(shape=[r.getNumValues()])
        for k, v in enumerate(r.getValues()):
            __range[k] = v
        lines.append("__range__{} = {}".format(r.getId(), list(__range)))
        return lines


    @staticmethod
    def repeatedTaskToPython(doc, task):
        """ Create python for RepeatedTask. """
        lines = []

        resetModel = task.getResetModel()
        rangeId = task.getRangeId()

        # -- create ranges ----------
        # master range
        masterRange = task.getRange(rangeId)
        if masterRange.getTypeCode() == libsedml.SEDML_RANGE_UNIFORMRANGE:
            lines.extend(SEDMLCodeFactory.uniformRangeToPython(masterRange))
        elif masterRange.getTypeCode() == libsedml.SEDML_RANGE_VECTORRANGE:
            lines.extend(SEDMLCodeFactory.vectorRangeToPython(masterRange))
        elif masterRange.getTypeCode() == libsedml.SEDML_RANGE_FUNCTIONALRANGE:
            warnings.warn("FunctionalRange for master range not supported in task.")
        # other ranges
        for r in task.getListOfRanges():
            if r.getId() != rangeId:
                if r.getTypeCode() == libsedml.SEDML_RANGE_UNIFORMRANGE:
                    lines.extend(SEDMLCodeFactory.uniformRangeToPython(r))
                elif r.getTypeCode() == libsedml.SEDML_RANGE_VECTORRANGE:
                    lines.extend(SEDMLCodeFactory.vectorRangeToPython(r))

        # -- iterate over ordered subtasks ----------
        subtasks = task.getListOfSubTasks()
        subtaskOrder = [st.getOrder() for st in subtasks]

        # sort by order, if all subtasks have order (not required)
        if all(subtaskOrder) != None:
            subtasks = [st for (stOrder, st) in sorted(zip(subtaskOrder, subtasks))]

        # storage of results
        lines.append("{} = []".format(task.getId()))
        # -- iterate over master range ----------
        lines.append("for k in range(len(__range__{})):".format(rangeId))

        # Everything from now on is done in every iteration of the range
        # We have to collect & intent all lines in the loop)
        forLines = []

         # <range values>
        # calculate the current values of all range variables
        # value for masterRange
        forLines.append("__value__{} = __range__{}[k]".format(rangeId, rangeId))
        # other range values
        helperRanges = {}
        for r in task.getListOfRanges():
            if r.getId() != rangeId:
                helperRanges[r.getId()] = r
                if r.getTypeCode() in [libsedml.SEDML_RANGE_UNIFORMRANGE,
                                       libsedml.SEDML_RANGE_VECTORRANGE]:
                    forLines.append("__value__{} = __range__{}[k]".format(r.getId(), r.getId()))

                # <functional range>
                if r.getTypeCode() == libsedml.SEDML_RANGE_FUNCTIONALRANGE:
                    # TODO: refactor (code reusage of the MathML evaluation
                    variables = {}
                    # range variables
                    variables[rangeId] = "__value__{}".format(rangeId)
                    for key in helperRanges.keys():
                        variables[key] = "__value__{}".format(key)
                    # parameters
                    for par in r.getListOfParameters():
                        variables[par.getId()] = par.getValue()
                    for var in r.getListOfVariables():
                        vid = var.getId()
                        selection = SEDMLCodeFactory.resolveSelectionFromVariable(var)
                        if type == "species":
                            forLines.append("__var__{} = {}['[{}]']".format(vid, mid, selection.id))
                        else:
                            forLines.append("__var__{} = {}['{}']".format(vid, mid, selection.id))
                        variables[vid] = "__var__{}".format(vid)

                    # value is calculated with the current state of model
                    value = evaluableMathML(r.getMath(), variables=variables)
                    forLines.append("__value__{} = {}".format(r.getId(), value))

        # reset all subtask models before executing the subtasks if necessary
        st_mids = set([doc.getTask(st.getTask()).getModelReference() for st in subtasks])
        for st_mid in st_mids:
            # <resetModel>
            if resetModel:
                # reset before every iteration
                forLines.append("{}.reset()".format(st_mid))
            else:
                # reset before first iteration of repeated task
                forLines.append("if k == 0:")
                forLines.append("    {}.reset()".format(st_mid))

        # <setValues>
        # apply changes based on current variables, parameters and range variables
        for setValue in task.getListOfTaskChanges():
            variables = {}
            # range variables
            variables[rangeId] = "__value__{}".format(rangeId)
            for key in helperRanges.keys():
                variables[key] = "__value__{}".format(key)
            # parameters
            for par in setValue.getListOfParameters():
                variables[par.getId()] = par.getValue()
            for var in setValue.getListOfVariables():
                vid = var.getId()
                mid = var.getModelReference()
                selection = SEDMLCodeFactory.resolveSelectionFromVariable(var)
                if type == "species":
                    forLines.append("__var__{} = {}['[{}]']".format(vid, mid, selection.id))
                else:
                    forLines.append("__var__{} = {}['{}']".format(vid, mid, selection.id))
                variables[vid] = "__var__{}".format(vid)

            # value is calculated with the current state of model
            value = evaluableMathML(setValue.getMath(), variables=variables)
            xpath = setValue.getTarget()
            mid = setValue.getModelReference()
            forLines.append(SEDMLCodeFactory.targetToPython(xpath, value, modelId=mid))

        # handle the offsets of the next subtask
        offset = 0
        for ksub, subtask in enumerate(subtasks):
            # All subtasks have to be carried out sequentially, each continuing
            # from the current model state (i.e. at the end of the previous subTask,
            # assuming it simulates the same model), and with their results
            # concatenated (thus appearing identical to a single complex simulation).
            # get task which belongs to subtask
            t = doc.getTask(subtask.getTask())

            # <Run single repeat>
            # All local variables for the loop iteration and subtask are available.
            # Run the single simulation now.
            resultVariable = "__subtask__".format(t.getId())
            selections = SEDMLCodeFactory.selectionsForTask(doc=doc, task=task)
            if t.getTypeCode() == libsedml.SEDML_TASK:

                # lines.extend(SEDMLCodeFactory.simpleTaskToPython(doc, task))
                forLines.extend(SEDMLCodeFactory.subtaskToPython(doc, task=t,
                                                          selections=selections,
                                                          resultVariable=resultVariable, offset=offset))
                # append subtask to task simulation
                forLines.append("{}.extend([__subtask__])".format(task.getId()))

            # <REPEATED TASK>
            elif t.getTypeCode() == libsedml.SEDML_TASK_REPEATEDTASK:
                # lines.extend(SEDMLCodeFactory.repeatedTaskToPython(doc, task=t))
                # raise NotImplementedError("RepeatedTasks of repeated tasks not supported.")
                warnings.warn("RepeatedTasks of repeated tasks not supported.")
                # TODO: extend with the whole set

        # add lines
        lines.extend('    ' + line for line in forLines)

        return lines


    @staticmethod
    def subtaskToPython(doc, task, selections, resultVariable=None):
        """ Creates the simulation python code for a given task.

            cvode (19; the default for uniform time course simulations)
            gillespie (241; the default for stochastic time course simulations)
            steadystate (407; the default for steady state simulations)
            rk4 (32; 4th-order Runge-Kutta)
            rk45 (435; embedded Runge-Kutta)
        """
        lines = []
        mid = task.getModelReference()
        sid = task.getSimulationReference()
        simulation = doc.getSimulation(sid)

        simType = simulation.getTypeCode()
        algorithm = simulation.getAlgorithm()
        if algorithm is None:
            warnings.warn("Algorithm missing on simulation, defaulting to 'cvode: KISAO:0000019'")
            algorithm = simulation.createAlgorithm()
            algorithm.setKisaoID("KISAO:0000019")
        kisao = algorithm.getKisaoID()

        # Check if supported algorithm
        if not SEDMLCodeFactory.isSupportedKisaoIDForSimulation(kisao=kisao, simType=simType):
            lines.append("# Unsupported Algorithm {} for SimulationType {}".format(kisao, simulation.getElementName()))
            return lines

        # Set integrator
        integratorName = SEDMLCodeFactory.getIntegratorNameForKisaoID(kisao)
        if not integratorName:
            warnings.warn("No integrator exists for {} in roadrunner".format(kisao))
            return lines
        lines.append("{}.setIntegrator('{}')".format(mid, integratorName))

        # Set integrator settings (AlgorithmParameters)
        for par in algorithm.getListOfAlgorithmParameters():
            pkey = SEDMLCodeFactory.algorithmParameterToParameterKey(par)
            lines.append("{}.getIntegrator().setValue('{}', '{}')".format(mid, pkey.key, pkey.value))
            # FIXME: settings for steady state solver have to be set via {}.steadyStateSolver


        # handle result variable
        if resultVariable is None:
            resultVariable = task.getId()

        # -------------------------------------------------------------------------
        # <UNIFORM TIMECOURSE>
        # -------------------------------------------------------------------------
        if simType == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
            lines.append("{}.timeCourseSelections = {}".format(mid, list(selections)))

            initialTime = simulation.getInitialTime()
            outputStartTime = simulation.getOutputStartTime()
            outputEndTime = simulation.getOutputEndTime()
            numberOfPoints = simulation.getNumberOfPoints()

            # throw some points away
            if abs(outputStartTime - initialTime) > 1E-6:
                lines.append("{}.simulate(start={}, end={}, points=2)".format(
                                    mid, initialTime+offset, outputStartTime))
            # real simulation
            lines.append("{} = {}.simulate(start={}, end={}, steps={})".format(
                                    resultVariable, mid, outputStartTime, outputEndTime, numberOfPoints))
        # -------------------------------------------------------------------------
        # <ONESTEP>
        # -------------------------------------------------------------------------
        elif simType == libsedml.SEDML_SIMULATION_ONESTEP:
            lines.append("{}.timeCourseSelections = {}".format(mid, list(selections)))
            step = simulation.getStep()
            lines.append("{} = {}.simulate(start={}, end={}, points=2)".format(resultVariable, mid, 0.0, step))

        # -------------------------------------------------------------------------
        # <STEADY STATE>
        # -------------------------------------------------------------------------
        elif simType == libsedml.SEDML_SIMULATION_STEADYSTATE:
            lines.append("Config = {}".format(mid, list(selections)))
            lines.append("{}.conservedMoietyAnalysis = True".format(mid))
            lines.append("{}.steadyStateSelections = {}".format(mid, list(selections)))
            lines.append("{}.steadyState()".format(mid))
            # FIX as long as no NamedArrays are returned
            lines.append("{} = dict(zip({}.steadyStateSelections, {}.getSteadyStateValues()))".format(resultVariable, mid, mid))
            lines.append("{}.conservedMoietyAnalysis = False".format(mid))

        # -------------------------------------------------------------------------
        # <OTHER>
        # -------------------------------------------------------------------------
        else:
            lines.append("# Unsupported simulation: {}".format(simType))

        return lines

    @staticmethod
    def selectionsForTask(doc, task):
        """ Populate variable lists from the data generators for the given task.

        These are the timeCourseSelections and steadyStateSelections
        in RoadRunner.

        Search all data generators for variables which have to be part of the simulation.
        """
        selections = set()
        for dg in doc.getListOfDataGenerators():
            for var in dg.getListOfVariables():
                # either has not task reference or not for the current task
                if var.getTaskReference() != task.getId():
                    continue

                sel = SEDMLCodeFactory.resolveSelectionFromVariable(var)
                selections.add(sel.id)

        return selections

    @staticmethod
    def resolveSelectionFromVariable(var):
        """ Resolve the model target to model identifier.

        :param var:
        :type var: SedVariable
        :return:
        :rtype: Target
        """
        Selection = namedtuple('Selection', 'id type')

        # symbol field of variable is set
        if var.isSetSymbol():
            cvs = var.getSymbol()
            astr = cvs.rsplit("symbol:")
            sid = astr[1]
            return Selection(sid, 'symbol')

        elif var.isSetTarget():
            cvt = var.getTarget()    # target field of variable is set
            astr = cvt.rsplit("@id='")
            if len(astr) is 1:
                astr = cvt.rsplit("@name='")
            astr = astr[len(astr)-1]
            sid = astr[:-2]
            if 'species' in cvt:
                return Selection('[{}]'.format(sid), 'species')
            if 'parameter' in cvt:
                return Selection(sid, 'parameter')
            else:
                return Selection(sid, 'other')
        else:
            warnings.warn("Unrecognized Selection in variable")
            return None

    @staticmethod
    def isSupportedKisaoIDForSimulation(kisao, simType):
        """ Test if Algorithm Kisao Id is supported for simulation.

            KISAO:0000433 : CVODE-like method
            KISAO:0000019 : CVODE
            KISAO:0000241 : Gillespie-like method
            KISAO_0000064 : Runge-Kutta based method
            KISAO_0000032 : explicit fourth-order Runge-Kutta method
            KISAO_0000435 : embedded Runge-Kutta 5(4) method

        :return:
        :rtype: bool
        """
        supported = []
        if simType == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
            supported = ['KISAO:0000433',
                         'KISAO:0000019',
                         'KISAO:0000241',
                         'KISAO:0000032',
                         'KISAO:0000435',
                         'KISAO_0000064',
                         'KISAO:0000035',
                         'KISAO:0000071']
        elif simType == libsedml.SEDML_SIMULATION_ONESTEP:
            supported = ['KISAO:0000433',
                         'KISAO:0000019',
                         'KISAO:0000241',
                         'KISAO:0000032',
                         'KISAO:0000435',
                         'KISAO_0000064']
        elif simType == libsedml.SEDML_SIMULATION_STEADYSTATE:
            supported = ['KISAO:0000099',
                         'KISAO:0000407']
        return kisao in supported

    @staticmethod
    def getIntegratorNameForKisaoID(kid):
        """ RoadRunner integrator name for algorithm KisaoID.

        :param kid: KisaoID
        :type kid: str
        :return: RoadRunner integrator name.
        :rtype: str
        """
        # cvode & steady state are mapped to cvode
        if kid in ['KISAO:0000433',
                   'KISAO:0000019',
                   'KISAO:0000407',
                   'KISAO:0000099',
                   'KISAO:0000035',
                   'KISAO:0000071']:
            return 'cvode'
        elif kid == 'KISAO:0000241':
            return 'gillespie'
        elif kid == 'KISAO:0000032':
            return 'rk4'
        elif kid in ['KISAO:0000435',
                     'KISAO_0000064']:
            return 'rk45'
        else:
            return None

    @staticmethod
    def algorithmParameterToParameterKey(par):
        """ Resolve the mapping between parameter keys and roadrunner integrator keys.

            relative_tolerance (209; the relative tolerance)
            absolute_tolerance (211; the absolute tolerance)
            maximum_bdf_order (220; the maximum BDF (stiff) order)
            maximum_adams_order (219; the maximum Adams (non-stiff) order)
            maximum_num_steps (415; the maximum number of steps that can be taken before exiting)
            maximum_time_step (467; the maximum time step that can be taken)
            minimum_time_step (485; the minimum time step that can be taken)
            initial_time_step (332; the initial value of the time step for algorithms that change this value)
            variable_step_size (107; whether or not the algorithm proceeds with an adaptive step size or not)
            maximum_iterations (486; the maximum number of iterations the algorithm should take before exiting)
            minimum_damping (487; minimum damping value)
            seed (488; the seed for stochastic runs of the algorithm)
        """
        kid = par.getKisaoID()
        value = par.getValue()
        ParameterKey = namedtuple('ParameterKey', 'key value')
        key = None

        if kid == 'KISAO:0000209':
            key = 'relative_tolerance'
        elif kid == 'KISAO:0000211':
            key = 'relative_tolerance'
        elif kid == 'KISAO:0000220':
            key = 'maximum_bdf_order'
        elif kid == 'KISAO:0000219':
            key = 'maximum_adams_order'
        elif kid == 'KISAO:0000415':
            key = 'maximum_num_steps'
        elif kid == 'KISAO:0000467':
            key = 'maximum_time_step'
        elif kid == 'KISAO:0000485':
            key = 'minimum_time_step'
        elif kid == 'KISAO:0000332':
            key = 'initial_time_step'
        elif kid == 'KISAO:0000107':
            key = 'variable_step_size'
        elif kid == 'KISAO:0000486':
            key = 'maximum_iterations'
        elif kid == 'KISAO:0000487':
            key = 'maximum_damping'
        elif kid == 'KISAO:0000488':
            key = 'seed'
        # set the setting
        if key is not None:
            return ParameterKey(key, value)
        else:
            warnings.warn("Unsupported AlgorithmParameter: {} = {})".format(kid, value))
            return None

    @staticmethod
    def targetToPython(xpath, value, modelId):
        """ Creates python line for given xpath target and value.
        :param xpath:
        :type xpath:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        target = SEDMLCodeFactory.resolveTargetFromXPath(xpath)
        if target is None:
            line = ("# Unsupported target: {}".format(xpath))
        else:
            # parameter value change
            if target.type == "parameter":
                line = ("{}['{}'] = {}".format(modelId, target.id, value))
            # species concentration change
            elif target.type == "species":
                line = ("{}['init([{}])'] = {}".format(modelId, target.id, value))
            # unknown
            elif target.type == "unknown":
                line = ("{}['{}'] = {}".format(modelId, target.id, value))
            else:
                line = ("# Unsupported target: {}".format(xpath))

        return line

    @staticmethod
    def resolveTargetFromXPath(xpath):
        """ Resolve the model target to model identifier.

        :param xpath:
        :type xpath:
        :return:
        :rtype:
        """
        # FIXME: getting of sids, pids not very robust
        # TODO: handle more cases (rules, reactions, ...)
        # real xpath with SBML (get all objects)
        Target = namedtuple('Target', 'id type')

        def getId(xpath):
            xpath = xpath.replace('"', "'")
            match = re.findall(r"id='(.*?)'", xpath)
            if (match is None) or (len(match) is 0):
                warnings.warn("Xpath could not be resolved: {}".format(xpath))
            return match[0]

        # parameter value change
        if ("model" in xpath) and ("parameter" in xpath):
            return Target(getId(xpath), 'parameter')

        # species concentration change
        elif ("model" in xpath) and ("species" in xpath):
            return Target(getId(xpath), 'species')

        # other
        elif ("model" in xpath) and ("id" in xpath):
            return Target(getId(xpath), 'unknown')

        # cannot be parsed
        else:
            warnings.warn("Unsupported target: {}".format(xpath))
            return None

    @staticmethod
    def dataGeneratorToPython(doc, generator):
        """ Create variable from the data generators and the simulations.

            The data of repeatedTasks is handled differently depending
            on if reset=True or reset=False.
            reset=True:
                every repeat is a single curve, i.e. the data is a list of data
            reset=False:
                all curves belong to a single simulation and are concatenated to one dataset
        """
        lines = []
        gid = generator.getId()
        mathml = generator.getMath()

        # create variables
        variables = {}
        for par in generator.getListOfParameters():
            variables[par.getId()] = par.getValue()
        for var in generator.getListOfVariables():
            varId = var.getId()
            variables[varId] = "__var__{}".format(varId)

        # create python for variables
        for var in generator.getListOfVariables():
            taskId = var.getTaskReference()
            task = doc.getTask(taskId)

            selection = SEDMLCodeFactory.resolveSelectionFromVariable(var)
            isTime = False
            if selection.type == "symbol" and selection.id == "time":
                isTime = True

            resetModel = True
            if task.getTypeCode() == libsedml.SEDML_TASK_REPEATEDTASK:
                resetModel = task.getResetModel()

            # Series of curves

            if resetModel is True:
                lines.append("__var__{} = np.transpose(np.array([sim['{}'] for sim in {}]))".format(varId, selection.id, taskId))
            else:
                # One curve via time adjusted concatenate
                if isTime is True:
                    lines.append("__offsets__{} = np.cumsum(np.array([sim['{}'][-1] for sim in {}]))".format(taskId, selection.id, taskId))
                    lines.append("__offsets__{} = np.insert(__offsets__{}, 0, 0)".format(taskId, taskId))
                    lines.append("__var__{} = np.transpose(np.array([sim['{}']+__offsets__{}[k] for k, sim in enumerate({})]))".format(varId, selection.id, taskId, taskId))
                    lines.append("__var__{} = np.concatenate(np.transpose(__var__{}))".format(varId, varId))
                else:
                    lines.append("__var__{} = np.transpose(np.array([sim['{}'] for sim in {}]))".format(varId, selection.id, taskId))
                    lines.append("__var__{} = np.concatenate(np.transpose(__var__{}))".format(varId, varId))
            lines.append("if len(__var__{}.shape) == 1:".format(varId))
            lines.append("     __var__{}.shape += (1,)".format(varId))

        # calculate data generator
        value = evaluableMathML(mathml, variables=variables, array=True)
        lines.append("{} = {}".format(gid, value))

        return "\n".join(lines)

    @staticmethod
    def outputToPython(doc, output):
        """ Create output """
        # TODO: save plots and reports in workingDir
        lines = []
        typeCode = output.getTypeCode()
        if typeCode == libsedml.SEDML_OUTPUT_REPORT:
            lines.extend(SEDMLCodeFactory.outputReportToPython(doc, output))
        elif typeCode == libsedml.SEDML_OUTPUT_PLOT2D:
            lines.extend(SEDMLCodeFactory.outputPlot2DToPython(doc, output))
        elif typeCode == libsedml.SEDML_OUTPUT_PLOT3D:
            lines.extend(SEDMLCodeFactory.outputPlot3DToPython(doc, output))
        else:
            lines.append("# Unsupported output type: {}".format(output.getElementName()))
        return '\n'.join(lines)

    @staticmethod
    def outputReportToPython(doc, output):
        """ OutputReport

        :param doc:
        :type doc: SedDocument
        :param output:
        :type output: SedOutputReport
        :return: list of python lines
        :rtype: list(str)
        """
        # TODO: reports for repeated tasks?
        lines = []

        headers = []
        dgIds = []
        columns = []
        for dataSet in output.getListOfDataSets():
            # these are the columns
            headers.append(dataSet.getLabel())
            # data generator (the id is the id of the data in python)
            dgId = dataSet.getDataReference()
            dgIds.append(dgId)
            columns.append("{}[:,k]".format(dgId))
        # create data frames for the repeats
        lines.append("__dfs__{} = []".format(output.getId()))
        lines.append("for k in range({}.shape[1]):".format(dgIds[0]))
        lines.append("    print('-'*80)")
        lines.append("    print('{}, Repeat:', k)".format(output.getId()))
        lines.append("    print('-'*80)")
        lines.append("    __df__k = pandas.DataFrame(np.column_stack(" + str(columns).replace("'", "") + "), \n    columns=" + str(headers) + ")")
        lines.append("    print(__df__k.head(10))")
        lines.append("    __dfs__{}.append(__df__k)".format(output.getId()))
        return lines

    @staticmethod
    def outputPlotSettings():
        """ Settings for all plot types.

        :return:
        :rtype:
        """
        PlotSettings = namedtuple('PlotSettings', 'colors, figsize, dpi, facecolor, edgecolor, linewidth, markersize, alpha')

        # all lines of same cuve have same color
        settings = PlotSettings(
            colors=[u'r', u'b', u'g', u'm', u'c', u'y', u'k'],
            figsize=(9, 5),
            dpi=80,
            facecolor='w',
            edgecolor='k',
            linewidth=1.5,
            markersize=4.0,
            alpha=0.8
        )
        return settings

    @staticmethod
    def outputPlot2DToPython(doc, output):
        """ OutputReport

        :param doc:
        :type doc: SedDocument
        :param output:
        :type output: SedOutputReport
        :return: list of python lines
        :rtype: list(str)
        """
        # TODO: handle mix of log and linear axis
        lines = []
        settings = SEDMLCodeFactory.outputPlotSettings()

        title = output.getId()
        if output.isSetName():
            title = output.getName()

        lines.append("plt.figure(num=None, figsize={}, dpi={}, facecolor='{}', edgecolor='{}')".format(settings.figsize, settings.dpi, settings.facecolor, settings.edgecolor))
        lines.append("from matplotlib import gridspec")
        lines.append("__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])")
        lines.append("plt.subplot(__gs[0])")

        oneXLabel = True
        allXLabel = None
        for kc, curve in enumerate(output.getListOfCurves()):
            logX = curve.getLogX()
            logY = curve.getLogY()
            xId = curve.getXDataReference()
            yId = curve.getYDataReference()
            dgx = doc.getDataGenerator(xId)
            dgy = doc.getDataGenerator(yId)
            color = settings.colors[kc % len(settings.colors)]

            yLabel = yId
            if curve.isSetName():
                yLabel = curve.getName()
            elif dgy.isSetName():
                yLabel = dgy.getName()
            xLabel = xId
            if dgx.isSetName():
                xLabel = dgx.getName()

            # do all curves have the same xLabel
            if kc == 0:
                allXLabel = xLabel
            elif xLabel != allXLabel:
                oneXLabel = False

            lines.append("for k in range({}.shape[1]):".format(xId))
            lines.append("    if k == 0:")
            lines.append("        plt.plot({}[:,k], {}[:,k], '-o', color='{}', linewidth={}, markersize={}, alpha={}, label='{}')".format(xId, yId, color, settings.linewidth, settings.markersize, settings.alpha, yLabel))
            lines.append("    else:")
            lines.append("        plt.plot({}[:,k], {}[:,k], '-o', color='{}', linewidth={}, markersize={}, alpha={})".format(xId, yId, color, settings.linewidth, settings.markersize, settings.alpha))


            # FIXME: has to be handeled via multiple axis
            if logX is True:
                lines.append("plt.xscale('log')")
            if logY is True:
                lines.append("plt.yscale('log')")
        lines.append("plt.title('{}', fontweight='bold')".format(title))
        if oneXLabel:
            lines.append("plt.xlabel('{}', fontweight='bold')".format(xLabel))
        if len(output.getListOfCurves()) == 1:
            lines.append("plt.ylabel('{}', fontweight='bold')".format(yLabel))

        lines.append("__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)")
        lines.append("__lg.draw_frame(False)")
        lines.append("plt.setp(__lg.get_texts(), fontsize='small')")
        lines.append("plt.setp(__lg.get_texts(), fontweight='bold')")
        lines.append("plt.show()".format(title))

        return lines

    @staticmethod
    def outputPlot3DToPython(doc, output):
        """ OutputPlot3D

        :param doc:
        :type doc: SedDocument
        :param output:
        :type output: SedOutputPlot3D
        :return: list of python lines
        :rtype: list(str)
        """
        # TODO: handle mix of log and linear axis
        settings = SEDMLCodeFactory.outputPlotSettings()
        lines = []
        lines.append("from mpl_toolkits.mplot3d import Axes3D")
        lines.append("fig = plt.figure(num=None, figsize={}, dpi={}, facecolor='{}', edgecolor='{}')".format(settings.figsize, settings.dpi, settings.facecolor, settings.edgecolor))
        lines.append("from matplotlib import gridspec")
        lines.append("__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])")
        lines.append("ax = plt.subplot(__gs[0], projection='3d')")
        # lines.append("ax = fig.gca(projection='3d')")

        title = output.getId()
        if output.isSetName():
            title = output.getName()

        oneXLabel = True
        oneYLabel = True
        allXLabel = None
        allYLabel = None

        for kc, surf in enumerate(output.getListOfSurfaces()):
            logX = surf.getLogX()
            logY = surf.getLogY()
            logZ = surf.getLogZ()
            xId = surf.getXDataReference()
            yId = surf.getYDataReference()
            zId = surf.getZDataReference()
            dgx = doc.getDataGenerator(xId)
            dgy = doc.getDataGenerator(yId)
            dgz = doc.getDataGenerator(zId)
            color = settings.colors[kc % len(settings.colors)]

            zLabel = zId
            if surf.isSetName():
                zLabel = surf.getName()
            elif dgy.isSetName():
                zLabel = dgz.getName()

            xLabel = xId
            if dgx.isSetName():
                xLabel = dgx.getName()
            yLabel = yId
            if dgy.isSetName():
                yLabel = dgy.getName()

            # do all curves have the same xLabel & yLabel
            if kc == 0:
                allXLabel = xLabel
                allYLabel = yLabel
            if xLabel != allXLabel:
                oneXLabel = False
            if yLabel != allYLabel:
                oneYLabel = False

            lines.append("for k in range({}.shape[1]):".format(xId))
            lines.append("    if k == 0:")
            lines.append("        ax.plot({}[:,k], {}[:,k], {}[:,k], '-o', color='{}', linewidth=1.5, markersize=4.0, alpha=0.8, label='{}')".format(xId, yId, zId, color, zLabel))
            lines.append("    else:")
            lines.append("        ax.plot({}[:,k], {}[:,k], {}[:,k], '-o', color='{}', linewidth=1.5, markersize=4.0, alpha=0.8)".format(xId, yId, zId, color))

        lines.append("ax.set_title('{}', fontweight='bold')".format(title))
        if oneXLabel:
            lines.append("ax.set_xlabel('{}', fontweight='bold')".format(xLabel))
        if oneYLabel:
            lines.append("ax.set_ylabel('{}', fontweight='bold')".format(yLabel))
        if len(output.getListOfSurfaces()) == 1:
            lines.append("ax.set_zlabel('{}', fontweight='bold')".format(zLabel))

        lines.append("__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)")
        lines.append("__lg.draw_frame(False)")
        lines.append("plt.setp(__lg.get_texts(), fontsize='small')")
        lines.append("plt.setp(__lg.get_texts(), fontweight='bold')")
        lines.append("plt.tick_params(axis='both', which='major', labelsize=10)")
        lines.append("plt.tick_params(axis='both', which='minor', labelsize=8)")
        lines.append("plt.show()".format(title))

        return lines


##################################################################################################
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
            print(libsedml.writeSedMLToString(doc))
            raise IOError(doc.getErrorLog().toString())
        if doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_FATAL) > 0:
            print(libsedml.writeSedMLToString(doc))
            raise IOError(doc.getErrorLog().toString())
        if doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_WARNING) > 0:
            warnings.warn(doc.getErrorLog().toString())
        if doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_SCHEMA_ERROR) > 0:
            warnings.warn(doc.getErrorLog().toString())
        if doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_GENERAL_WARNING) > 0:
            warnings.warn(doc.getErrorLog().toString())

    @classmethod
    def readSEDMLDocument(cls, inputStr):
        """ Parses SedMLDocument from given input.

        :return: dictionary of SedDocument, inputType and working directory.
        :rtype: {doc, inputType, workingDir}
        """
        if not isinstance(inputStr, basestring):
            raise IOError("SED-ML input is not instance of basestring:", inputStr)

        # SEDML-String
        if not os.path.exists(inputStr):
            try:
                from xml.etree import ElementTree
                x = ElementTree.fromstring(inputStr)
                # is parsable xml string
                doc = libsedml.readSedMLFromString(inputStr)
                inputType = cls.INPUT_TYPE_STR
                workingDir = os.getcwd()

            except ElementTree.ParseError:
                if not os.path.exists(inputStr):
                    raise IOError("SED-ML String is not valid XML:", inputStr)

        # SEDML-File
        else:
            filename, extension = os.path.splitext(os.path.basename(inputStr))

            # Archive
            if zipfile.is_zipfile(inputStr):
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

            # SEDML single file
            elif os.path.isfile(inputStr):
                if extension not in [".sedml", '.xml']:
                    raise IOError("SEDML file should have [.sedml|.xml] extension:", inputStr)
                inputType = cls.INPUT_TYPE_FILE_SEDML
                doc = libsedml.readSedMLFromFile(inputStr)
                cls.checkSEDMLDocument(doc)
                # working directory is where the sedml file is
                workingDir = os.path.dirname(os.path.realpath(inputStr))

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


##################################################################################################
if __name__ == "__main__":
    import os
    from tellurium.tests.testdata import sedmlDir, sedxDir
    import matplotlib
    matplotlib.pyplot.switch_backend("Agg")

    def testInput(sedmlInput):
        """ Test function run on inputStr. """
        print('\n', '*'*100)
        print(sedmlInput)
        print('*'*100)
        factory = SEDMLCodeFactory(sedmlInput)

        # create python file
        python_str = factory.toPython()
        with open(sedmlInput + '.py', 'w') as f:
            f.write(python_str)
        # execute python
        factory.executePython()

    # Check sed-ml files
    for fname in sorted(os.listdir(sedmlDir)):
        if fname.endswith(".sedml"):
            testInput(os.path.join(sedmlDir, fname))


    # Check sedx archives
    for fname in sorted(os.listdir(sedxDir)):
        if fname.endswith(".sedx"):
            testInput(os.path.join(sedxDir, fname))

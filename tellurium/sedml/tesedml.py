# -*- coding: utf-8 -*-
"""
Tellurium SED-ML support.

This module implements SED-ML support for tellurium.

----------------
Overview SED-ML
----------------
SED-ML is build of main classes
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

TODO: DATA CLASS


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

For information about SED-ML please refer to http://www.sed-ml.org/
and the SED-ML specification.

------------------------------------
SED-ML in tellurium: Implementation
------------------------------------
SED-ML support in tellurium is based on Combine Archives.
The SED-ML files in the Archive can be executed and stored with results.

----------------------------------------
SED-ML in tellurium: Supported Features
----------------------------------------
Tellurium supports SED-ML L1V3 with SBML as model format.

SBML models are fully supported, whereas for CellML models only basic support
is implemented (when additional support is requested it be implemented).
CellML models are transformed to SBML models which results in different XPath expressions,
so that targets, selections cannot be easily resolved in the CellMl-SBML.

Supported input for SED-ML are either SED-ML files ('.sedml' extension),
SED-ML XML strings or combine archives ('.sedx'|'.omex' extension).
Executable python code is generated from the SED-ML which allows the
execution of the defined simulation experiment.

    In the current implementation all SED-ML constructs with exception of
    XML transformation changes of the model
        - Change.RemoveXML
        - Change.AddXML
        - Change.ChangeXML
    are supported.

-------
Notice
-------
The main maintainer for SED-ML support is Matthias König.
Please let changes to this file be reviewed and make sure that all SED-ML related tests are working.
"""
from __future__ import  absolute_import, print_function, division

import sys
import platform
import tempfile
import shutil
import traceback
import os.path
import warnings
import datetime
import zipfile
import re
import numpy as np
from collections import namedtuple
import jinja2

try:
    import libsedml
except ImportError:
    import tesedml as libsedml

from tellurium.utils import omex
from .mathml import evaluableMathML
import tellurium as te

try:
    # required imports in generated python code
    import pandas
    import matplotlib.pyplot as plt
    import mpl_toolkits.mplot3d
except ImportError:
    warnings.warn("Dependencies for SEDML code execution not fulfilled.")
    print(traceback.format_exc())

######################################################################################################################
# KISAO MAPPINGS
######################################################################################################################

def getKisaoValFromString(id):
    idvec = []
    if ":" in id:
        idvec = id.split(":")
    elif "_" in id:
        idvec = id.split("_")
    return int(idvec[-1])

def getKisaoStringFromVal(val):
    return "KISAO_" + str(val).zfill(7)

KISAOS_CVODE = [  # 'cvode'
    19,  # CVODE
    433,  # CVODE-like method
    407,
    99,
    35,
    71,
    288,  # "BDF" cvode, stiff=true
    280,  # "Adams-Moulton" cvode, stiff=false
]

KISAOS_RK4 = [  # 'rk4'
    32,  # RK4 explicit fourth-order Runge-Kutta method
    64,  # Runge-Kutta based method
]

KISAOS_RK45 = [  # 'rk45'
    435,  # RKF45 embedded Runge-Kutta 5(4) method
    321,  # RKF45 embedded Runge-Kutta 5(4) method of Cash-Karp
    87,  # RKF45 embedded Runge-Kutta 5(4) method of Dormand-Price
    86,  # RKF45 embedded Runge-Kutta 5(4) method of Fehlberg
    434,  # RKF45 embedded Runge-Kutta 5(4) method of Higham-Hall
]

KISAOS_LSODA = [  # 'lsoda'
    88,  # roadrunner doesn't have an lsoda solver so use cvode
]

KISAOS_EULER = [  # 'lsoda'
    30,  # The Euler forward method
    261, # The Euler method in general.  (31 is the backward method, which we don't support.)
]

KISAOS_GILLESPIE = [  # 'gillespie'
    241,  # Gillespie-like method
    29,
    319,
    274,
    333,
    329,
    323,
    331,
    27,
    82,
    324,
    350,
    330,
    28,
    38,
    39,
    48,
    74,
    81,
    45,
    351,
    84,
    40,
    46,
    3,
    51,
    335,
    336,
    95,
    22,
    76,
    15,
    75,
    278,
]

KISAOS_NLEQ = [  # 'nleq'
    99,
    274,
    282,
    283,
    355,
    356,
    407,
    408,
    409,
    410,
    411,
    412,
    413,
    432,
    437,
]

# allowed algorithms for simulation type
KISAOS_STEADYSTATE = KISAOS_NLEQ
KISAOS_UNIFORMTIMECOURSE = KISAOS_CVODE + KISAOS_RK4 + KISAOS_RK45 + KISAOS_GILLESPIE + KISAOS_LSODA + KISAOS_EULER
KISAOS_ONESTEP = KISAOS_UNIFORMTIMECOURSE

# supported algorithm parameters
KISAOS_ALGORITHMPARAMETERS = {
    209: ('relative_tolerance', float),  # the relative tolerance
    211: ('absolute_tolerance', float),  # the absolute tolerance
    220: ('maximum_bdf_order', int),  # the maximum BDF (stiff) order
    219: ('maximum_adams_order', int),  # the maximum Adams (non-stiff) order
    415: ('maximum_num_steps', int),  # the maximum number of steps that can be taken before exiting
    467: ('maximum_time_step', float),  # the maximum time step that can be taken
    485: ('minimum_time_step', float),  # the minimum time step that can be taken
    559: ('initial_time_step', float),  # the initial value of the time step for algorithms that change this value
    332: ('initial_time_step', float),  # the initial value of the time step for algorithms that change this value
    107: ('variable_step_size', bool),  # whether or not the algorithm proceeds with an adaptive step size or not (not accurate, but grandfathered in; it was a similar thing but not an algorithm parameter.)
    656: ('variable_step_size', bool),  # whether or not the algorithm proceeds with an adaptive step size or not
    486: ('maximum_iterations', int),  # [nleq] the maximum number of iterations the algorithm should take before exiting
    487: ('minimum_damping', float),  # [nleq] minimum damping value
    488: ('seed', int),  # the seed for stochastic runs of the algorithm
    673: ('nonnegative', bool), #For gillespie algorithms; ensures no reaction produces negative species amounts.
    674: ('allow_presimulation', bool), #For any steady state solver, allow presimulation.
    677: ('presimulation_maximum_steps', float), #For any steady state solver, number of presimulation steps to take.
    680: ('presimulation_time', float), #For any steady state solver, amount of time for the presimulation.
    682: ('allow_approx', bool), #For any steady state solver: use an approximation routine when steady state calculation fails.
    683: ('approx_tolerance', float), #For any steady state solver, tolerance of the approximation routine.
    678: ('approx_maximum_steps', int), #For any steady state solver, max steps of the approximation routine.
    679: ('approx_time', float), #For any steady state solver, end time for approximation routine.
    675: ('broyden_method', int), #For an NLEQ steady state solver: use the Broyden method.
    676: ('linearity', int), #For an NLEQ steady state solver: set the linearity of the problem (1-4).
}

curve_types = {
    libsedml.SEDML_CURVETYPE_POINTS: "line",
    libsedml.SEDML_CURVETYPE_BAR: "bar",
    libsedml.SEDML_CURVETYPE_BARSTACKED: "barStacked",
    libsedml.SEDML_CURVETYPE_HORIZONTALBAR: "barHorizontal",
    libsedml.SEDML_CURVETYPE_HORIZONTALBARSTACKED: "barHorizontalStacked",
}

line_types = {
    libsedml.SEDML_LINETYPE_NONE: (False, "none", []),
    libsedml.SEDML_LINETYPE_DASH: (True, "dash", [4, 2]),
    libsedml.SEDML_LINETYPE_DASHDOT: (True, "dash", [4, 2, 1, 2]),
    libsedml.SEDML_LINETYPE_DASHDOTDOT: (True, "dash", [4, 2, 1, 2, 1, 2]),
    libsedml.SEDML_LINETYPE_DOT: (True, "dash", [1, 2]),
    libsedml.SEDML_LINETYPE_SOLID: (True, "line", []),
}

marker_types = {
    libsedml.SEDML_MARKERTYPE_CIRCLE: "o",
    libsedml.SEDML_MARKERTYPE_DIAMOND: "D",
    libsedml.SEDML_MARKERTYPE_HDASH: "_",
    libsedml.SEDML_MARKERTYPE_NONE: "",
    libsedml.SEDML_MARKERTYPE_PLUS: "+",
    libsedml.SEDML_MARKERTYPE_SQUARE: "s",
    libsedml.SEDML_MARKERTYPE_STAR: "*",
    libsedml.SEDML_MARKERTYPE_TRIANGLEDOWN: "v",
    libsedml.SEDML_MARKERTYPE_TRIANGLELEFT: "<",
    libsedml.SEDML_MARKERTYPE_TRIANGLERIGHT: ">",
    libsedml.SEDML_MARKERTYPE_TRIANGLEUP: "^",
    libsedml.SEDML_MARKERTYPE_VDASH: "|",
    libsedml.SEDML_MARKERTYPE_XCROSS: "x",
}

surface_types = {
    libsedml.SEDML_SURFACETYPE_BAR: "plot",
    libsedml.SEDML_SURFACETYPE_CONTOUR: "contour",
    libsedml.SEDML_SURFACETYPE_HEATMAP: "pcolormesh",
    libsedml.SEDML_SURFACETYPE_PARAMETRICCURVE: "plot",
    libsedml.SEDML_SURFACETYPE_STACKEDCURVES: "plot",
    libsedml.SEDML_SURFACETYPE_SURFACECONTOUR: "plot_surface",
    libsedml.SEDML_SURFACETYPE_SURFACEMESH: "plot_wireframe",
}

######################################################################################################################
# Interface functions
######################################################################################################################
# The functions listed in this section are the only functions one should interact with this module.
# We try to keep these back-wards compatible and keep the function signatures.
#
# All other function and class signatures can change.
######################################################################################################################

def sedmlToPython(inputStr, workingDir=None):
    """ Convert sedml file to python code.

    :param inputStr: full path name to SedML model or SED-ML string
    :type inputStr: path
    :return: generated python code
    """
    factory = SEDMLCodeFactory(inputStr, workingDir=workingDir)
    return factory.toPython()


def executeSEDML(inputStr, 
                 workingDir=None,
                 createOutputs=True,
                 saveOutputs=False,
                 outputDir=None,
                 plottingEngine=None
):
    """ Run a SED-ML file or combine archive with results.

    If a workingDir is provided the files and results are written in the workingDir.

    :param inputStr:
    :type inputStr:
    :return:
    :rtype:
    """
    # execute the sedml
    factory = SEDMLCodeFactory(inputStr, workingDir=workingDir,
                     createOutputs=createOutputs,
                     saveOutputs=saveOutputs,
                     outputDir=outputDir,
                     plottingEngine=plottingEngine
)
    factory.executePython()


def combineArchiveToPython(omexPath):
    """ All python code generated from given combine archive.

    :param omexPath:
    :return: dictionary of { sedml_location: pycode }
    """
    tmp_dir = tempfile.mkdtemp()
    pycode = {}
    try:
        omex.extractCombineArchive(omexPath, directory=tmp_dir, method="zip")
        locations = omex.getLocationsByFormat(omexPath, "sed-ml")
        sedml_files = [os.path.join(tmp_dir, loc) for loc in locations]

        for k, sedml_file in enumerate(sedml_files):
            pystr = sedmlToPython(sedml_file)
            pycode[locations[k]] = pystr

    finally:
        shutil.rmtree(tmp_dir)
    return pycode


def executeCombineArchive(omexPath,
                          workingDir=None,
                          printPython=False,
                          createOutputs=True,
                          saveOutputs=False,
                          outputDir=None,
                          plottingEngine=None):
    """ Run all SED-ML simulations in given COMBINE archive.

    If no workingDir is provided execution is performed in temporary directory
    which is cleaned afterwards.
    The executed code can be printed via the 'printPython' flag.

    :param omexPath: OMEX Combine archive
    :param workingDir: directory to extract archive to
    :param printPython: boolean switch to print executed python code
    :param createOutputs: boolean flag if outputs should be created, i.e. reports and plots
    :param saveOutputs: flag if the outputs should be saved to file
    :param outputDir: directory where the outputs should be written
    :param plottingEngin: string of which plotting engine to use; uses set plotting engine otherwise
    :return dictionary of sedmlFile:data generators
    """

    # combine archives are zip format
    if zipfile.is_zipfile(omexPath):
        try:
            tmp_dir = tempfile.mkdtemp()
            if workingDir is None:
                extractDir = tmp_dir
            else:
                if not os.path.exists(workingDir):
                    raise IOError("workingDir does not exist, make sure to create the directoy: '{}'".format(workingDir))
                extractDir = workingDir

            # extract
            omex.extractCombineArchive(omexPath=omexPath, directory=extractDir)

            # get sedml locations by omex
            sedml_locations = omex.getLocationsByFormat(omexPath=omexPath, formatKey="sed-ml", method="omex")
            if len(sedml_locations) == 0:

                # falling back to zip archive
                sedml_locations = omex.getLocationsByFormat(omexPath=omexPath, formatKey="sed-ml", method="zip")
                warnings.warn(
                    "No SED-ML files in COMBINE archive based on manifest '{}'; Guessed SED-ML {}".format(omexPath, sedml_locations))


            # run all sedml files
            results = {}
            sedml_paths = [os.path.join(extractDir, loc) for loc in sedml_locations]
            for sedmlFile in sedml_paths:
                factory = SEDMLCodeFactory(sedmlFile,
                                           workingDir=os.path.dirname(sedmlFile),
                                           createOutputs=createOutputs,
                                           saveOutputs=saveOutputs,
                                           outputDir=outputDir,
                                           plottingEngine=plottingEngine
                                           )
                if printPython:
                    code = factory.toPython()
                    print(code)

                results[sedmlFile] = factory.executePython()

            return results
        finally:
            shutil.rmtree(tmp_dir)
    else:
        if not os.path.exists(omexPath):
            raise FileNotFoundError("File does not exist: {}".format(omexPath))
        else:
            raise IOError("File is not an OMEX Combine Archive in zip format: {}".format(omexPath))

######################################################################################################################

class SEDMLCodeFactory(object):
    """ Code Factory generating executable code."""

    # template location
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

    def __init__(self, inputStr,
                 workingDir=None,
                 createOutputs=True,
                 saveOutputs=False,
                 outputDir=None,
                 plottingEngine=None
                 ):
        """ Create CodeFactory for given input.

        :param inputStr:
        :param workingDir:
        :param createOutputs: if outputs should be created

        :return:
        :rtype:
        """
        self.inputStr = inputStr
        self.workingDir = workingDir
        self.python = sys.version
        self.platform = platform.platform()
        self.createOutputs = createOutputs
        self.saveOutputs = saveOutputs
        self.outputDir = outputDir
        self.plotFormat = "pdf"
        self.reportFormat = "csv"

        if not plottingEngine:
            plottingEngine = te.getPlottingEngine()
        self.plottingEngine = plottingEngine

        if self.outputDir:
            if not os.path.exists(outputDir):
                raise IOError("outputDir does not exist: {}".format(outputDir))


        info = SEDMLTools.readSEDMLDocument(inputStr, workingDir)
        self.doc = info['doc']
        self.inputType = info['inputType']
        self.workingDir = info['workingDir']

        # parse the models (resolve the source models & the applied changes for all models)
        model_sources, model_changes = SEDMLTools.resolveModelChanges(self.doc)
        self.model_sources = model_sources
        self.model_changes = model_changes

    def __str__(self):
        """ Print.

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

    def toPython(self, python_template='tesedml_template.template'):
        """ Create python code by rendering the python template.
        Uses the information in the SED-ML document to create
        python code

        Renders the respective template.

        :return: returns the rendered template
        :rtype: str
        """
        # template environment
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.TEMPLATE_DIR),
                          trim_blocks=True,
                          lstrip_blocks=True)

        # additional filters
        # for key in sedmlfilters.filters:
        #      env.filters[key] = getattr(sedmlfilters, key)
        template = env.get_template(python_template)
        env.globals['modelToPython'] = self.modelToPython
        env.globals['dataDescriptionToPython'] = self.dataDescriptionToPython
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
        pysedml = template.render(c)

        return pysedml

    def executePython(self):
        """ Executes python code.

        The python code is created during the function call.
        See :func:`createpython`

        :return: returns dictionary of information with keys
        """
        result = {}
        code = self.toPython()
        result['code'] = code
        result['platform'] = platform.platform()

        # FIXME: better solution for exec traceback
        filename = os.path.join(tempfile.gettempdir(), 'te-generated-sedml.py')

        try:
            # Use of exec carries the usual security warnings
            symbols = {}
            exec(compile(code, filename, 'exec'), symbols)

            # read information from exec symbols
            dg_data = {}
            for dg in self.doc.getListOfDataGenerators():
                dg_id = dg.getId()
                dg_data[dg_id] = symbols[dg_id]
            result['dataGenerators'] = dg_data
            return result

        except:
            # leak this tempfile just so we can see a full stack trace. freaking python.
            with open(filename, 'w') as f:
                f.write(code)
            raise
    def localParamsInModelChanges(self):
        """
        Returns True if any of the model changes target local parameters.
        """
        for mod in self.model_changes:
            for change in self.model_changes[mod]:
                target = change.getTarget()
                if "kineticLaw" in target and "arameter" in target:
                    return True
        return False

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

        if not language:
            warnings.warn("No model language specified, defaulting to SBML for: {}".format(source))

        def isUrn():
            return source.startswith('urn') or source.startswith('URN')

        def isHttp():
            return source.startswith('http') or source.startswith('HTTP')

        # read SBML
        if 'sbml' in language or len(language) == 0:
            if isUrn():
                lines.append("import tellurium.temiriam as temiriam")
                lines.append("__{}_sbml = temiriam.getSBMLFromBiomodelsURN('{}')".format(mid, source))
                lines.append("{} = te.loadSBMLModel(__{}_sbml)".format(mid, mid))
            elif isHttp():
                lines.append("{} = te.loadSBMLModel('{}')".format(mid, source))
            elif source[0] == "#":
                lines.append("{} = te.loadSBMLModel({}.getCurrentSBML())".format(mid, source[1:]))
            else:
                lines.append("{} = te.loadSBMLModel(os.path.join(workingDir, '{}'))".format(mid, source))
        # read CellML
        elif 'cellml' in language:
            warnings.warn("CellML model encountered. Tellurium CellML support is very limited.".format(language))
            if isHttp():
                lines.append("{} = te.loadCellMLModel('{}')".format(mid, source))
            else:
                lines.append("{} = te.loadCellMLModel(os.path.join(workingDir, '{}'))".format(mid, self.model_sources[mid]))
        # other
        else:
            warnings.warn("Unsupported model language: '{}'.".format(language))

        # If there are local parameters pointed to by the model changes, convert
        # the model first
        if self.localParamsInModelChanges():
            lines.append("# Promote the local parameters, since there are model changes that target them, and roadrunner doesn't normally provide access.")
            lines.append("promoted = {}.getParamPromotedSBML({}.getCurrentSBML())".format(mid, mid))
            lines.append("{} = te.loadSBMLModel(promoted)".format(mid))

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
            variables = {}
            for par in change.getListOfParameters():
                variables[par.getId()] = par.getValue()
            for var in change.getListOfVariables():
                vid = var.getId()
                selection = SEDMLCodeFactory.selectionFromVariable(var, mid)
                expr = selection.id
                if selection.type == "concentration":
                    expr = "init([{}])".format(selection.id)
                elif selection.type == "amount":
                    expr = "init({})".format(selection.id)
                lines.append("__var__{} = {}['{}']".format(vid, mid, expr))
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


    def dataDescriptionToPython(self, dataDescription):
        """ Python code for DataDescription.

        :param dataDescription: SedModel instance
        :type dataDescription: DataDescription
        :return: python str
        :rtype: str
        """
        lines = []

        from tellurium.sedml.data import DataDescriptionParser
        data_sources = DataDescriptionParser.parse(dataDescription, self.workingDir)

        def data_to_string(data):
            info = np.array2string(data)
            # cleaner string and NaN handling
            info = info.replace('\n', ', ').replace('\r', '').replace('nan', 'np.nan')
            return info

        for sid, data in data_sources.items():
            # handle the 1D shapes
            if len(data.shape) == 1:
                data = np.reshape(data.values, (data.shape[0], 1))

            array_str = data_to_string(data)
            lines.append("{} = np.array({})".format(sid, array_str))

        return '\n'.join(lines)


    ################################################################################################
    # Here the main work is done,
    # transformation of tasks to python code
    ################################################################################################
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
        # If no DataGenerator references the task, no execution is necessary
        dgs = SEDMLCodeFactory.getDataGeneratorsForTask(doc, task)
        if len(dgs) == 0:
            return "# not part of any DataGenerator: {}".format(task.getId())

        # tasks contain other subtasks, which can contain subtasks. This
        # results in a tree of task dependencies where the
        # simple tasks are the node leaves. These tree has to be resolved to
        # generate code for more complex task dependencies.

        # resolve task tree (order & dependency of tasks) & generate code
        taskTree = SEDMLCodeFactory.createTaskTree(doc, rootTask=task)
        return SEDMLCodeFactory.taskTreeToPython(doc, tree=taskTree)

    class TaskNode(object):
        """ Tree implementation of task tree. """
        def __init__(self, task, depth):
            self.task = task
            self.depth = depth
            self.children = []
            self.parent = None

        def add_child(self, obj):
            obj.parent = self
            self.children.append(obj)

        def is_leaf(self):
            return len(self.children) == 0

        def __str__(self):
            lines = ["<[{}] {} ({})>".format(self.depth, self.task.getId(), self.task.getElementName())]
            for child in self.children:
                child_str = child.__str__()
                lines.extend(["\t{}".format(line) for line in child_str.split('\n')])
            return "\n".join(lines)

        def info(self):
            return "<[{}] {} ({})>".format(self.depth, self.task.getId(), self.task.getElementName())

        def __iter__(self):
            """ Depth-first iterator which yields TaskNodes."""
            yield self
            for child in self.children:
                for node in child:
                    yield node

    class Stack(object):
        """ Stack implementation for nodes."""
        def __init__(self):
            self.items = []

        def isEmpty(self):
            return self.items == []

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop()

        def peek(self):
            return self.items[len(self.items)-1]

        def size(self):
            return len(self.items)

        def __str__(self):
            return "stack: " + str([item.info() for item in self.items])

    @staticmethod
    def createTaskTree(doc, rootTask):
        """ Creates the task tree.
        Required for resolution of order of all simulations.
        """
        def add_children(node):
            typeCode = node.task.getTypeCode()
            if typeCode == libsedml.SEDML_TASK:
                return  # no children
            elif typeCode == libsedml.SEDML_TASK_REPEATEDTASK:
                # add the ordered list of subtasks as children
                subtasks = SEDMLCodeFactory.getOrderedSubtasks(node.task)
                for st in subtasks:
                    # get real task for subtask
                    t = doc.getTask(st.getTask())
                    child = SEDMLCodeFactory.TaskNode(t, depth=node.depth+1)
                    node.add_child(child)
                    # recursive adding of children
                    add_children(child)
            else:
                raise IOError('Unsupported task type: {}'.format(node.task.getElementName()))

        # create root
        root = SEDMLCodeFactory.TaskNode(rootTask, depth=0)
        # recursive adding of children
        add_children(root)
        return root

    @staticmethod
    def getOrderedSubtasks(task):
        """ Ordered list of subtasks for task."""
        subtasks = task.getListOfSubTasks()
        subtaskOrder = [st.getOrder() for st in subtasks]
        # sort by order, if all subtasks have order (not required)
        if all(subtaskOrder) != None:
            subtasks = [st for (stOrder, st) in sorted(zip(subtaskOrder, subtasks))]
        return subtasks

    @staticmethod
    def taskTreeToPython(doc, tree):
        """ Python code generation from task tree. """

        # go forward through task tree
        lines = []
        nodeStack = SEDMLCodeFactory.Stack()
        treeNodes = [n for n in tree]

        # iterate over the tree
        for kn, node in enumerate(treeNodes):
            taskType = node.task.getTypeCode()

            # Create information for task
            # We are going down in the tree
            if taskType == libsedml.SEDML_TASK_REPEATEDTASK:
                taskLines = SEDMLCodeFactory.repeatedTaskToPython(doc, node=node)

            elif taskType == libsedml.SEDML_TASK:
                if node.parent and node.parent.task.getTypeCode()==libsedml.SEDML_TASK_REPEATEDTASK:
                    #The repeated task itself should have set up the simulation; here we just run it.
                    taskLines = SEDMLCodeFactory.simpleTaskMainSim(doc, node)
                else:
                    taskLines = SEDMLCodeFactory.simpleTaskToPython(doc=doc, node=node)
            else:
                lines.append("# Unsupported task: {}".format(taskType))
                warnings.warn("Unsupported task: {}".format(taskType))

            lines.extend(["    "*node.depth + line for line in taskLines])

            '''
            @staticmethod
            def simpleTaskToPython(doc, task):
                """ Create python for simple task. """
                for ksub, subtask in enumerate(subtasks):
                    t = doc.getTask(subtask.getTask())

                    resultVariable = "__subtask__".format(t.getId())
                    selections = SEDMLCodeFactory.selectionsForTask(doc=doc, task=task)
                    if t.getTypeCode() == libsedml.SEDML_TASK:
                        forLines.extend(SEDMLCodeFactory.subtaskToPython(doc, task=t,
                                                                  selections=selections,
                                                                  resultVariable=resultVariable))
                        forLines.append("{}.extend([__subtask__])".format(task.getId()))

                    elif t.getTypeCode() == libsedml.SEDML_TASK_REPEATEDTASK:
                        forLines.extend(SEDMLCodeFactory.repeatedTaskToPython(doc, task=t))
                        forLines.append("{}.extend({})".format(task.getId(), t.getId()))
            '''

            # Collect information
            # We have to go back up
            # Look at next node in the treeNodes (this is the next one to write)
            if kn == (len(treeNodes)-1):
                nextNode = None
            else:
                nextNode = treeNodes[kn+1]

            # The next node is further up in the tree, or there is no next node
            # and still nodes on the stack
            if (nextNode is None) or (nextNode.depth < node.depth):

                # necessary to pop nodes from the stack and close the code
                test = True
                while test is True:
                    # stack is empty
                    if nodeStack.size() == 0:
                        test = False
                        continue
                    # try to pop next one
                    peek = nodeStack.peek()
                    if (nextNode is None) or (peek.depth > nextNode.depth):
                        # TODO: reset evaluation has to be defined here
                        # determine if it's steady state
                        # if taskType == libsedml.SEDML_TASK_REPEATEDTASK:
                        # print('task {}'.format(node.task.getId()))
                        # print('  peek {}'.format(peek.task.getId()))
                        if node.task.getTypeCode() == libsedml.SEDML_TASK_REPEATEDTASK:
                        # if peek.task.getTypeCode() == libsedml.SEDML_TASK_REPEATEDTASK:
                            # sid = task.getSimulationReference()
                            # simulation = doc.getSimulation(sid)
                            # simType = simulation.getTypeCode()
                            # if simType is libsedml.SEDML_SIMULATION_STEADYSTATE:
                            terminator = 'terminate_trace({})'.format(node.task.getId())
                        else:
                            terminator = '{}'.format(node.task.getId())

                        lines.extend([
                            "",
                            # "    "*node.depth + "{}.extend({})".format(peek.task.getId(), terminator),
                            "    " * node.depth + "{}.extend({})".format(peek.task.getId(), node.task.getId()),
                        ])
                        node = nodeStack.pop()

                    else:
                        test = False
            else:
                # we are going done or next subtask -> put node on stack
                nodeStack.push(node)

        return "\n".join(lines)

    @staticmethod
    def simpleTaskToPython(doc, node):
        """ Creates the simulation python code for a given taskNode.

        The taskNodes are required to handle the relationships between
        RepeatedTasks, SubTasks and SimpleTasks (Task).

        :param doc: sedml document
        :type doc: SEDDocument
        :param node: taskNode of the current task
        :type node: TaskNode
        :return:
        :rtype:
        """
        lines = SEDMLCodeFactory.simpleTaskSetup(doc, node)
        lines.extend(SEDMLCodeFactory.simpleTaskMainSim(doc, node))
        return lines
        


    @staticmethod
    def simpleTaskSetup(doc, node):
        """ Creates the first half of simulation python code for a given taskNode.

        The taskNodes are required to handle the relationships between
        RepeatedTasks, SubTasks and SimpleTasks (Task).

        :param doc: sedml document
        :type doc: SEDDocument
        :param node: taskNode of the current task
        :type node: TaskNode
        :return:
        :rtype:
        """
        lines = []
        task = node.task
        lines.append("# Task: <{}>".format(task.getId()))
        lines.append("{} = [None]".format(task.getId()))

        mid = task.getModelReference()
        sid = task.getSimulationReference()
        simulation = doc.getSimulation(sid)

        simType = simulation.getTypeCode()
        algorithm = simulation.getAlgorithm()
        if algorithm is None:
            warnings.warn("Algorithm missing on simulation, defaulting to 'cvode: KISAO_0000019'")
            algorithm = simulation.createAlgorithm()
            algorithm.setKisaoID(getKisaoStringFromVal(19))
        kisao = getKisaoValFromString(algorithm.getKisaoID())

        # is supported algorithm
        if not SEDMLCodeFactory.isSupportedAlgorithmForSimulationType(kisao=kisao, simType=simType):
            warnings.warn("Algorithm {} unsupported for simulation {} type {} in task {}".format(kisao, simulation.getId(), simType, task.getId()))
            lines.append("# Unsupported Algorithm {} for SimulationType {}".format(kisao, simulation.getElementName()))
            return lines

        # set integrator/solver
        integratorName = SEDMLCodeFactory.getIntegratorNameForKisaoID(kisao)
        if not integratorName:
            warnings.warn("No integrator exists for {} in roadrunner".format(kisao))
            return lines

        if simType is libsedml.SEDML_SIMULATION_STEADYSTATE:
            lines.append("{}.setSteadyStateSolver('{}')".format(mid, integratorName))
        else:
            lines.append("{}.setIntegrator('{}')".format(mid, integratorName))

        # use fixed step by default for stochastic sims
        if integratorName == 'gillespie':
            lines.append("{}.integrator.setValue('{}', {})".format(mid, 'variable_step_size', False))

        if kisao == 288:  # BDF
            lines.append("{}.integrator.setValue('{}', {})".format(mid, 'stiff', True))
        elif kisao == 280:  # Adams-Moulton
            lines.append("{}.integrator.setValue('{}', {})".format(mid, 'stiff', False))

        # integrator/solver settings (AlgorithmParameters)
        for par in algorithm.getListOfAlgorithmParameters():
            pkey = SEDMLCodeFactory.algorithmParameterToParameterKey(par)
            # only set supported algorithm paramters
            if pkey:
                if pkey.dtype is str:
                    value = "'{}'".format(pkey.value)
                else:
                    value = pkey.value

                if value == str('inf') or pkey.value == float('inf'):
                    value = "float('inf')"
                else:
                    pass

                if simType is libsedml.SEDML_SIMULATION_STEADYSTATE:
                    lines.append("{}.steadyStateSolver.setValue('{}', {})".format(mid, pkey.key, value))
                else:
                    lines.append("{}.integrator.setValue('{}', {})".format(mid, pkey.key, value))

        if simType is libsedml.SEDML_SIMULATION_STEADYSTATE:
            lines.append("if {model}.conservedMoietyAnalysis == False: {model}.conservedMoietyAnalysis = True".format(model=mid))
        else:
            lines.append("if {model}.conservedMoietyAnalysis == True: {model}.conservedMoietyAnalysis = False".format(model=mid))
        return lines


    @staticmethod
    def simpleTaskParentInit(doc, node):
        """ Creates the simulation python code for a given taskNode.

        The taskNodes are required to handle the relationships between
        RepeatedTasks, SubTasks and SimpleTasks (Task).

        :param doc: sedml document
        :type doc: SEDDocument
        :param node: taskNode of the current task
        :type node: TaskNode
        :return:
        :rtype:
        """
        lines = []
        task = node.task

        mid = task.getModelReference()
        sid = task.getSimulationReference()
        simulation = doc.getSimulation(sid)

        simType = simulation.getTypeCode()

        # get parents
        parents = []
        parent = node.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent

        # get parents
        parents = []
        parent = node.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent

        # <setValues> of all parents
        # ---------------------------
        # apply changes based on current variables, parameters and range variables
        for parent in reversed(parents):
            rangeId = parent.task.getRangeId()
            helperRanges = {}
            for r in parent.task.getListOfRanges():
                if r.getId() != rangeId:
                    helperRanges[r.getId()] = r

            for setValue in parent.task.getListOfTaskChanges():
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
                    selection = SEDMLCodeFactory.selectionFromVariable(var, mid)
                    expr = selection.id
                    if selection.type == 'concentration':
                        expr = "init([{}])".format(selection.id)
                    elif selection.type == 'amount':
                        expr = "init({})".format(selection.id)

                    # create variable
                    lines.append("__value__{} = {}['{}']".format(vid, mid, expr))
                    # variable for replacement
                    variables[vid] = "__value__{}".format(vid)

                # value is calculated with the current state of model
                lines.append(SEDMLCodeFactory.targetToPython(xpath=setValue.getTarget(),
                                                             value=evaluableMathML(setValue.getMath(), variables=variables),
                                                             modelId=setValue.getModelReference())
                             )
        return lines

    @staticmethod
    def simpleTaskMainSim(doc, node):
        """ Creates the simulation python code for a given taskNode.

        The taskNodes are required to handle the relationships between
        RepeatedTasks, SubTasks and SimpleTasks (Task).

        :param doc: sedml document
        :type doc: SEDDocument
        :param node: taskNode of the current task
        :type node: TaskNode
        :return:
        :rtype:
        """
        lines = SEDMLCodeFactory.simpleTaskParentInit(doc, node)

        task = node.task

        mid = task.getModelReference()
        sid = task.getSimulationReference()
        simulation = doc.getSimulation(sid)

        simType = simulation.getTypeCode()

        # get parents
        parents = []
        parent = node.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent

        # <selections> of all parents
        # ---------------------------
        selections = SEDMLCodeFactory.selectionsForTask(doc=doc, task=node.task)
        for p in parents:
            selections.update(SEDMLCodeFactory.selectionsForTask(doc=doc, task=p.task))

        # handle result variable
        resultVariable = "{}[0]".format(task.getId())

        # -------------------------------------------------------------------------
        # <UNIFORM TIMECOURSE>
        # -------------------------------------------------------------------------
        if simType == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
            lines.append("{}.timeCourseSelections = {}".format(mid, list(selections)))

            initialTime = simulation.getInitialTime()
            outputStartTime = simulation.getOutputStartTime()
            outputEndTime = simulation.getOutputEndTime()
            numberOfSteps = simulation.getNumberOfSteps()

            # reset before simulation (see https://github.com/sys-bio/tellurium/issues/193)
            lines.append("{}.reset()".format(mid))

            # throw some points away
            if abs(outputStartTime - initialTime) > 1E-6:
                lines.append("{}.simulate(start={}, end={}, points=2)".format(
                                    mid, initialTime, outputStartTime))
            # real simulation
            lines.append("{} = {}.simulate(start={}, end={}, steps={})".format(
                                    resultVariable, mid, outputStartTime, outputEndTime, numberOfSteps))
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
            lines.append("{}.steadyStateSolver.setValue('{}', {})".format(mid, 'allow_presimulation', False))
            lines.append("{}.steadyStateSelections = {}".format(mid, list(selections)))
            lines.append("{}.simulate()".format(mid))  # for stability of the steady state solver
            lines.append("{} = {}.steadyStateNamedArray()".format(resultVariable, mid))
            # no need to turn this off because it will be checked before the next simulation
            # lines.append("{}.conservedMoietyAnalysis = False".format(mid))

        # -------------------------------------------------------------------------
        # <OTHER>
        # -------------------------------------------------------------------------
        else:
            lines.append("# Unsupported simulation: {}".format(simType))

        return lines

    @staticmethod
    def repeatedTaskToPython(doc, node):
        """ Create python for RepeatedTask.

        Must create
        - the ranges (Ranges)
        - apply all changes (SetValues)
        """
        # storage of results
        task = node.task
        lines = ["", "{} = []".format(task.getId())]


        # Set up the integrator outside the loop.  This is mostly so that
        # the 'seed' is set up outside the loop, but everything else also 
        # doesn't need to be reset all the time.
        for child in node:
            if child.task.getTypeCode() == libsedml.SEDML_TASK:
                lines.extend(SEDMLCodeFactory.simpleTaskSetup(doc=doc, node=child))

        # <Range Definition>
        # master range
        rangeId = task.getRangeId()
        masterRange = task.getRange(rangeId)
        if masterRange.getTypeCode() == libsedml.SEDML_RANGE_UNIFORMRANGE:
            lines.extend(SEDMLCodeFactory.uniformRangeToPython(masterRange))
        elif masterRange.getTypeCode() == libsedml.SEDML_RANGE_VECTORRANGE:
            lines.extend(SEDMLCodeFactory.vectorRangeToPython(masterRange))
        elif masterRange.getTypeCode() == libsedml.SEDML_RANGE_FUNCTIONALRANGE:
            warnings.warn("FunctionalRange for master range not supported in task.")
        # lock-in ranges
        for r in task.getListOfRanges():
            if r.getId() != rangeId:
                if r.getTypeCode() == libsedml.SEDML_RANGE_UNIFORMRANGE:
                    lines.extend(SEDMLCodeFactory.uniformRangeToPython(r))
                elif r.getTypeCode() == libsedml.SEDML_RANGE_VECTORRANGE:
                    lines.extend(SEDMLCodeFactory.vectorRangeToPython(r))

        # <Range Iteration>
        # iterate master range
        lines.append("for __k__{}, __value__{} in enumerate(__range__{}):".format(rangeId, rangeId, rangeId))

        # Everything from now on is done in every iteration of the range
        # We have to collect & intent all lines in the loop)
        forLines = []

        # definition of lock-in ranges
        helperRanges = {}
        for r in task.getListOfRanges():
            if r.getId() != rangeId:
                helperRanges[r.getId()] = r
                if r.getTypeCode() in [libsedml.SEDML_RANGE_UNIFORMRANGE,
                                       libsedml.SEDML_RANGE_VECTORRANGE]:
                    forLines.append("__value__{} = __range__{}[__k__{}]".format(r.getId(), r.getId(), rangeId))

                # <functional range>
                if r.getTypeCode() == libsedml.SEDML_RANGE_FUNCTIONALRANGE:
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
                        mid = var.getModelReference()
                        selection = SEDMLCodeFactory.selectionFromVariable(var, mid)
                        expr = selection.id
                        if selection.type == 'concentration':
                            expr = "[{}]".format(selection.id)
                        lines.append("__value__{} = {}['{}']".format(vid, mid, expr))
                        variables[vid] = "__value__{}".format(vid)

                    # value is calculated with the current state of model
                    value = evaluableMathML(r.getMath(), variables=variables)
                    forLines.append("__value__{} = {}".format(r.getId(), value))

        # <resetModels>
        # models to reset via task tree below node
        mids = set([])
        for child in node:
            t = child.task
            if t.getTypeCode() == libsedml.SEDML_TASK:
                mids.add(t.getModelReference())
        # reset models referenced in tree below task
        for mid in mids:
            if task.getResetModel():
                # reset before every iteration
                forLines.append("{}.reset()".format(mid))
            else:
                # reset before first iteration
                forLines.append("if __k__{} == 0:".format(rangeId))
                forLines.append("    {}.reset()".format(mid))

        # add lines
        lines.extend('    ' + line for line in forLines)

        return lines

    ################################################################################################

    @staticmethod
    def getDataGeneratorsForTask(doc, task):
        """ Get the DataGenerators which reference the given task.

        :param doc:
        :type doc:
        :param task:
        :type task:
        :return:
        :rtype:
        """
        dgs = []
        for dg in doc.getListOfDataGenerators():
            for var in dg.getListOfVariables():
                if var.getTaskReference() == task.getId():
                    dgs.append(dg)
                    break  # the DataGenerator is added, no need to look at rest of variables
        return dgs

    @staticmethod
    def getModelsFrom(task):
        """
        Parameters
        ----------
        task : libsedml.SedRepeatedTask
            The repeated task that you need the models from.

        Returns
        -------
        A vector of unique model IDs from the repeated task's subtasks.

        """
        modvec = []
        for st in range(task.getNumSubTasks()):
            subtask = task.getSubTask(st)
            stid = subtask.getTask()
            refed_task = task.getSedDocument().getTask(stid)
            if isinstance(refed_task, libsedml.SedTask):
                newmod = refed_task.getModelReference()
                if newmod not in modvec:
                    modvec.append(newmod)
            elif isinstance(refed_task, libsedml.SedRepeatedTask):
                subvec = SEDMLCodeFactory.getModelsFrom(refed_task)
                for newmod in subvec:
                    if newmod not in modvec:
                        modvec.append(newmod)
            else:
                raise NotImplemented("Abstract Tasks that are not Tasks or Repeated Tasks are not supported.")
        return modvec

    @staticmethod
    def selectionsForTask(doc, task):
        """ Populate variable lists from the data generators for the given task.

        These are the timeCourseSelections and steadyStateSelections
        in RoadRunner.

        Search all data generators for variables which have to be part of the simulation.
        """
        modelId = ""
        if isinstance(task, libsedml.SedTask):
            modelId = task.getModelReference()
        elif isinstance(task, libsedml.SedRepeatedTask):
            modvec = SEDMLCodeFactory.getModelsFrom(task)
            if len(modvec) == 1:
                modelId = modvec[0]
            
        selections = set()
        for dg in doc.getListOfDataGenerators():
            for var in dg.getListOfVariables():
                if var.getTaskReference() == task.getId():
                    if modelId=="":
                        modelId = var.getModelReference()
                    if modelId=="":
                        raise RuntimeError("Unable to determine which model a referenced task variable is from.")
                    selection = SEDMLCodeFactory.selectionFromVariable(var, modelId)
                    if selection is None:
                        raise RuntimeError("Unable to retrieve model variable '" + var + "' from model '" + modelId + "'.")
                    expr = selection.id
                    if selection.type == "concentration":
                        expr = "[{}]".format(selection.id)
                    selections.add(expr)

        return selections

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
            lines.append("__range__{} = np.linspace(start={}, stop={}, num={})".format(rId, rStart, rEnd, rPoints))
        elif rType in ['Log', 'log']:
            lines.append("__range__{} = np.logspace(start={}, stop={}, num={})".format(rId, rStart, rEnd, rPoints))
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
    def isSupportedAlgorithmForSimulationType(kisao, simType):
        """ Check Algorithm Kisao Id is supported for simulation.

        :return: is supported
        :rtype: bool
        """
        supported = []
        if simType == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
            supported = KISAOS_UNIFORMTIMECOURSE
        elif simType == libsedml.SEDML_SIMULATION_ONESTEP:
            supported = KISAOS_ONESTEP
        elif simType == libsedml.SEDML_SIMULATION_STEADYSTATE:
            supported = KISAOS_STEADYSTATE
        return kisao in supported

    @staticmethod
    def getIntegratorNameForKisaoID(kid):
        """ RoadRunner integrator name for algorithm KisaoID.

        :param kid: KisaoID
        :type kid: str
        :return: RoadRunner integrator name.
        :rtype: str
        """
        if kid in KISAOS_NLEQ:
            return 'nleq2'
        if kid in KISAOS_CVODE:
            return 'cvode'
        if kid in KISAOS_GILLESPIE:
            return 'gillespie'
        if kid in KISAOS_RK4:
            return 'rk4'
        if kid in KISAOS_RK45:
            return 'rk45'
        if kid in KISAOS_EULER:
            return 'euler'
        if kid in KISAOS_LSODA:
            warnings.warn('Tellurium does not support LSODA. Using CVODE instead.')
            return 'cvode' # just use cvode
        return None

    @staticmethod
    def algorithmParameterToParameterKey(par):
        """ Resolve the mapping between parameter keys and roadrunner integrator keys."""
        ParameterKey = namedtuple('ParameterKey', 'key value dtype')
        kid = getKisaoValFromString(par.getKisaoID())
        value = par.getValue()

        if kid in KISAOS_ALGORITHMPARAMETERS:
            # algorithm parameter is in the list of parameters
            key, dtype = KISAOS_ALGORITHMPARAMETERS[kid]
            if dtype is bool:
                # transform manually ! (otherwise all strings give True)
                if value == 'true' or value == "True":
                    value = True
                elif value == 'false' or value == "False":
                    value = False
            else:
                # cast to data type of parameter
                value = dtype(value)
            return ParameterKey(key, value, dtype)
        else:
            # algorithm parameter not supported
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
        target = SEDMLCodeFactory._resolveXPath(xpath, modelId)
        if target:
            # initial concentration
            if target.type == "concentration":
                expr = 'init([{}])'.format(target.id)
            # initial amount
            elif target.type == "amount":
                expr = 'init({})'.format(target.id)
            # other (parameter, flux, ...)
            else:
                expr = target.id
            line = ("{}['{}'] = {}".format(modelId, expr, value))
        else:
            line = ("# Unsupported target xpath: {}".format(xpath))

        return line

    @staticmethod
    def selectionFromVariable(var, modelId):
        """ Resolves the selection for the given variable.

        First checks if the variable is a symbol and returns the symbol.
        If no symbol is set the xpath of the target is resolved
        and used in the selection

        :param var: variable to resolve
        :type var: SedVariable
        :return: a single selection
        :rtype: Selection (namedtuple: id type)
        """
        Selection = namedtuple('Selection', 'id type')

        # parse symbol expression
        if var.isSetSymbol():
            cvs = var.getSymbol()
            astr = cvs.rsplit("symbol:")
            sid = astr[1]
            return Selection(sid, 'symbol')
        # use xpath
        elif var.isSetTarget():
            xpath = var.getTarget()
            target = SEDMLCodeFactory._resolveXPath(xpath, modelId)
            return Selection(target.id, target.type)

        else:
            warnings.warn("Unrecognized Selection in variable")
            return None

    @staticmethod
    def _resolveXPath(xpath, modelId):
        """ Resolve the target from the xpath expression.

        A single target in the model corresponding to the modelId is resolved.
        Currently, the model is not used for xpath resolution.

        :param xpath: xpath expression.
        :type xpath: str
        :param modelId: id of model in which xpath should be resolved
        :type modelId: str
        :return: single target of xpath expression
        :rtype: Target (namedtuple: id type)
        """
        # TODO: via better xpath expression
        #   get type from the SBML document for the given id.
        #   The xpath expression can be very general and does not need to contain the full
        #   xml path
        #   For instance:
        #   /sbml:sbml/sbml:model/descendant::*[@id='S1']
        #   has to resolve to species.
        # TODO: figure out concentration or amount (from SBML document)
        # FIXME: getting of sids, pids not very robust, handle more cases (rules, reactions, ...)

        Target = namedtuple('Target', 'id type')

        def getId(xpath):
            xpath = xpath.replace('"', "'")
            match = re.findall(r"id='(.*?)'", xpath)
            if (match is None) or (len(match) == 0):
                warnings.warn("Xpath could not be resolved: {}".format(xpath))
            return match[0]

        def getAllIds(xpath):
            xpath = xpath.replace('"', "'")
            match = re.findall(r"id='(.*?)'", xpath)
            if (match is None) or (len(match) == 0):
                warnings.warn("Xpath could not be resolved: {}".format(xpath))
            return match

        #Local parameter value change
        if ("model" in xpath) and ("parameter" in xpath) and ("reaction" in xpath):
            (rxn, param) = getAllIds(xpath)
            return Target(rxn + "_" + param, 'parameter')

        # parameter value change
        if ("model" in xpath) and ("parameter" in xpath):
            return Target(getId(xpath), 'parameter')
        # species concentration change
        elif ("model" in xpath) and ("species" in xpath):
            return Target(getId(xpath), 'concentration')
        # other
        elif ("model" in xpath) and ("id" in xpath):
            return Target(getId(xpath), 'other')
        # cannot be parsed
        else:
            raise ValueError("Unsupported target in xpath: {}".format(xpath))


    @staticmethod
    def dataGeneratorToPython(doc, generator):
        """ Create variable from the data generators and the simulation results and data sources.

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
            varId = var.getId()
            taskId = var.getTaskReference()
            task = doc.getTask(taskId)

            # simulation data
            if task is not None:
                modelId = ""
                if isinstance(task, libsedml.SedTask):
                    modelId = task.getModelReference()
                elif isinstance(task, libsedml.SedRepeatedTask):
                    modvec = SEDMLCodeFactory.getModelsFrom(task)
                    if len(modvec) == 1:
                        modelId = modvec[0]
                if modelId=="" and isinstance(task, libsedml.SedTask):
                    modelId = task.getModelReference()
                if modelId=="":
                    modelId = var.getModelReference()
                if modelId=="":
                    raise RuntimeError("Unable to determine which model a referenced task variable is from.")

                selection = SEDMLCodeFactory.selectionFromVariable(var, modelId)
                isTime = False
                if selection.type == "symbol" and selection.id == "time":
                    isTime = True

                resetModel = True
                if task.getTypeCode() == libsedml.SEDML_TASK_REPEATEDTASK:
                    resetModel = task.getResetModel()

                sid = selection.id
                if selection.type == "concentration":
                    sid = "[{}]".format(selection.id)

                # Series of curves
                if resetModel is True:
                    # If each entry in the task consists of a single point (e.g. steady state scan)
                    # , concatenate the points. Otherwise, plot as separate curves.
                    import os
                    if 'PROCESS_TRACE' in os.environ and os.environ['PROCESS_TRACE']:
                        lines.append("__var__{} = np.concatenate([process_trace(sim['{}']) for sim in {}])".format(varId, sid, taskId))
                    else:
                        lines.append("__var__{} = np.column_stack([sim['{}'] for sim in {}])".format(varId, sid, taskId))
                else:
                    # One curve via time adjusted concatenate
                    if isTime is True:
                        lines.append("__offsets__{} = np.cumsum(np.array([sim['{}'][-1] for sim in {}]))".format(taskId, sid, taskId))
                        lines.append("__offsets__{} = np.insert(__offsets__{}, 0, 0)".format(taskId, taskId))
                        lines.append("__var__{} = np.transpose(np.array([sim['{}']+__offsets__{}[k] for k, sim in enumerate({})]))".format(varId, sid, taskId, taskId))
                        lines.append("__var__{} = np.concatenate(np.transpose(__var__{}))".format(varId, varId))
                    else:
                        lines.append("__var__{} = np.transpose(np.array([sim['{}'] for sim in {}]))".format(varId, sid, taskId))
                        lines.append("__var__{} = np.concatenate(np.transpose(__var__{}))".format(varId, varId))
                lines.append("if len(__var__{}.shape) == 1:".format(varId))
                lines.append("     __var__{}.shape += (1,)".format(varId))

            # check for data sources
            else:
                target = var.getTarget()
                if target.startswith('#'):
                    sid = target[1:]
                    lines.append("__var__{} = {}".format(varId, sid))
                else:
                    warnings.warn("Unknown target in variable, no reference to SId: {}".format(target))

        # calculate data generator
        value = evaluableMathML(mathml, variables=variables, array=True)
        lines.append("{} = {}".format(gid, value))

        return "\n".join(lines)


    def outputToPython(self, doc, output):
        """ Create output """
        lines = []
        typeCode = output.getTypeCode()
        if typeCode == libsedml.SEDML_OUTPUT_REPORT:
            lines.extend(SEDMLCodeFactory.outputReportToPython(self, doc, output))
        elif typeCode == libsedml.SEDML_OUTPUT_PLOT2D:
            lines.extend(SEDMLCodeFactory.outputPlot2DToPython(self, doc, output))
        elif typeCode == libsedml.SEDML_OUTPUT_PLOT3D:
            lines.extend(SEDMLCodeFactory.outputPlot3DToPython(self, doc, output))
        else:
            warnings.warn("# Unsupported output type '{}' in output {}".format(output.getElementName(), output.getId()))
        return '\n'.join(lines)

    def outputReportToPython(self, doc, output):
        """ OutputReport

        :param doc:
        :type doc: SedDocument
        :param output:
        :type output: SedOutputReport
        :return: list of python lines
        :rtype: list(str)
        """
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
        lines.append("    __df__k = pandas.DataFrame(np.column_stack(" + str(columns).replace("'", "") + "), \n    columns=" + str(headers) + ")")
        lines.append("    __dfs__{}.append(__df__k)".format(output.getId()))
        # save as variable in Tellurium
        lines.append("    te.setLastReport(__df__k)")
        if self.saveOutputs and self.createOutputs:

            lines.append(
                "    filename = os.path.join('{}', '{}.{}')".format(self.outputDir, output.getId(), self.reportFormat))
            lines.append(
                "    __df__k.to_csv(filename, sep=',', index=False)")
            lines.append(
                "    print('Report {}: {{}}'.format(filename))".format(output.getId()))
        return lines


    @staticmethod
    def outputPlotSettings():
        """ Settings for all plot types.

        :return:
        :rtype:
        """
        PlotSettings = namedtuple('PlotSettings', 'colors, figsize, dpi, facecolor, edgecolor, linewidth, marker, markersize, alpha')

        # all lines of same cuve have same color
        settings = PlotSettings(
            colors=[u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#d62728', u'#9467bd', u'#8c564b', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf'],
            figsize=(9, 5),
            dpi=80,
            facecolor='w',
            edgecolor='k',
            linewidth=1.5,
            marker='',
            markersize=3.0,
            alpha=1.0
        )
        return settings

    def outputPlot2DToPython(self, doc, output):
        """ OutputReport

        If workingDir is provided the plot is saved in the workingDir.
        :param doc:
        :type doc: SedDocument
        :param output:
        :type output: SedOutputReport
        :return: list of python lines
        :rtype: list(str)
        """

        # TODO: logX and logY not applied
        lines = []
        settings = SEDMLCodeFactory.outputPlotSettings()

        # figure title
        title = output.getId()
        if output.isSetName():
            title = "{}".format(output.getName())

        # xtitle
        oneXLabel = True
        allXLabel = None
        for kc, curve in enumerate(output.getListOfCurves()):
            xId = curve.getXDataReference()
            dgx = doc.getDataGenerator(xId)
            xLabel = xId
            if dgx.isSetName():
                xLabel = "{}".format(dgx.getName())

            # do all curves have the same xLabel
            if kc == 0:
                allXLabel = xLabel
            elif xLabel != allXLabel:
                oneXLabel = False
        xtitle = ''
        if oneXLabel:
            xtitle = allXLabel

        lines.append("_stacked = False")
        # stacking, currently disabled
        # lines.append("_stacked = False")
        # lines.append("_engine = te.getPlottingEngine()")
        # for kc, curve in enumerate(output.getListOfCurves()):
        #     xId = curve.getXDataReference()
        #     lines.append("if {}.shape[1] > 1 and te.getDefaultPlottingEngine() == 'plotly':".format(xId))
        #     lines.append("    stacked=True")
        lines.append("if _stacked:")
        lines.append("    tefig = te.getPlottingEngine().newStackedFigure(title='{}', xtitle='{}')".format(title, xtitle))
        lines.append("else:")
        lines.append("    tefig = te.nextFigure(title='{}', xtitle='{}')\n".format(title, xtitle))

        lastvbar = []
        lasthbar = []
        for kc, curve in enumerate(output.getListOfCurves()):
            #defaults:
            color = settings.colors[kc % len(settings.colors)]
            showLine = True
            showMarkers = False
            lthickness = None
            ltype = "line"
            mtype = None
            ctype = ""
            mfc = None
            mec = None
            ms = None
            mew = None
            fillcolor = None
            edgecolor = None
            bottom = None
            dashes = []
            yId2 = None
            dgy2 = None
            
            #Data:
            xId = curve.getXDataReference()
            if curve.getTypeCode()==libsedml.SEDML_SHADEDAREA:
                yId = curve.getYDataReferenceFrom()
                yId2 = curve.getYDataReferenceTo()
                dgy2 = doc.getDataGenerator(yId2)
                ctype = "fillBetween"
            else:
                yId = curve.getYDataReference()
                if curve.isSetType():
                    ctype = curve_types[curve.getType()]
            dgx = doc.getDataGenerator(xId)
            dgy = doc.getDataGenerator(yId)

            if curve.isSetStyle():
                style = doc.getEffectiveStyle(curve.getStyle())
                if doc.getStyle(curve.getStyle())==None:
                    raise ValueError("SED-ML curve '" + curve.getId() + "' references nonexistent style '" + curve.getStyle() + "'.")
                if style.isSetLineStyle():
                    line = style.getLineStyle()
                    if line.isSetType():
                        (showLine, ltype, dashes) = line_types[line.getType()]
                    if line.isSetColor():
                        color = line.getColor()
                    if line.isSetThickness():
                        lthickness = line.getThickness()
                if style.isSetMarkerStyle():
                    marker = style.getMarkerStyle()
                    if marker.isSetType():
                        mtype = marker_types[marker.getType()]
                    if marker.isSetFill():
                        mfc = marker.getFill()
                    if marker.isSetLineColor():
                        mec = marker.getLineColor()
                    if marker.isSetSize():
                        ms = marker.getSize()
                    if marker.isSetLineThickness():
                        mew = marker.getLineThickness()
                if style.isSetFillStyle():
                    fill = style.getFillStyle()
                    fillcolor = fill.getColor()
                
            tag = 'tag{}'.format(kc)

            yLabel = yId
            if curve.isSetName():
                yLabel = "{}".format(curve.getName())
            elif dgy.isSetName():
                yLabel = "{}".format(dgy.getName())


            if ctype=="line" and ltype=="none":
                ctype = "markers"
            bartype = None
            if "bar" in ctype:
                if color is not None:
                    edgecolor = color
                if fillcolor is not None:
                    color = fillcolor
                if "Stacked" in ctype:
                    lastbar = []
                    if "Horizontal" in ctype:
                        lastbar = lasthbar
                    else:
                        lastbar = lastvbar
                    for b, bid in enumerate(lastbar):
                        if b==0:
                            bottom = ""
                        else:
                            bottom += " + "
                        bottom += bid
                        bottom += "[:,k]"
                if "Horizontal" in ctype:
                    bartype = "horizontal"
                    lasthbar.append(yId)
                else:
                    bartype = "vertical"
                    lastvbar.append(yId)
                ctype = "bar" #The only issue with st
            
            if ctype == "fillBetween" and fillcolor is not None:
                color = fillcolor

            # FIXME: add all the additional information to the plot, i.e. the settings and styles for a given curve

            lines.append("for k in range({}.shape[1]):".format(xId))
            lines.append("    extra_args = {}")
            lines.append("    if k == 0:")
            lines.append("        extra_args['name'] = '{}'".format(yLabel))
            if ltype=="dash":
                lines.append("    extra_args['dash'] = {dashes}".format(dashes = dashes))
            if not ctype=="":
                lines.append("    extra_args['mode'] = '{ctype}'".format(ctype=ctype))
            if not mtype==None:
                lines.append("    extra_args['marker'] = '{mtype}'".format(mtype = mtype))
            if not lthickness==None:
                lines.append("    extra_args['linewidth'] = {lthickness}".format(lthickness = lthickness))
            if not mfc==None:
                lines.append("    extra_args['mfc'] = '{mfc}'".format(mfc = mfc))
            if not mec==None:
                lines.append("    extra_args['mec'] = '{mec}'".format(mec = mec))
            if not ms==None:
                lines.append("    extra_args['ms'] = {ms}".format(ms = ms))
            if not mew==None:
                lines.append("    extra_args['mew'] = {mew}".format(mew = mew))
            if not edgecolor==None:
                lines.append("    extra_args['edgecolor'] = '{edgecolor}'".format(edgecolor = edgecolor))
            if not bottom==None:
                lines.append("    extra_args['bottom'] = {bottom}".format(bottom = bottom))
            if not bartype==None:
                lines.append("    extra_args['bartype'] = '{bartype}'".format(bartype= bartype))
            if not yId2==None:
                lines.append("    extra_args['y2'] = {yId2}[:,k]".format(yId2= yId2))
                
                
            lines.append("    tefig.addXYDataset({xId}[:,k], {yId}[:,k], color='{color}', tag='{tag}', **extra_args)".format(xId=xId, yId=yId, color=color, tag=tag))

            if fillcolor is not None and ctype != "bar" and ctype != "fillBetween":
                lines.append("    tefig.addXYDataset({xId}[:,k], {yId}[:,k], color='{fillcolor}', mode='fill')".format(xId=xId, yId=yId, fillcolor=fillcolor))

            # FIXME: endpoints must be handled via plotting functions
            # lines.append("    fix_endpoints({}[:,k], {}[:,k], color='{}', tag='{}', fig=tefig)".format(xId, yId, color, tag))
        lines.append("if te.tiledFigure():\n")
        lines.append("    if te.tiledFigure().renderIfExhausted():\n")
        lines.append("        te.clearTiledFigure()\n")
        lines.append("else:\n")
        lines.append("    fig = tefig.render()\n")

        if self.saveOutputs and self.createOutputs:
            # FIXME: only working for matplotlib
            lines.append("if str(te.getPlottingEngine()) == '<MatplotlibEngine>':".format(self.outputDir, output.getId(), self.plotFormat))
            lines.append("    filename = os.path.join('{}', '{}.{}')".format(self.outputDir, output.getId(), self.plotFormat))
            lines.append("    fig.savefig(filename, format='{}', bbox_inches='tight')".format(self.plotFormat))
            lines.append("    print('Figure {}: {{}}'.format(filename))".format(output.getId()))
            lines.append("")
        return lines

    def outputPlot3DToPython(self, doc, output):
        """ OutputPlot3D

        :param doc:
        :type doc: SedDocument
        :param output:
        :type output: SedOutputPlot3D
        :return: list of python lines
        :rtype: list(str)
        """
        settings = SEDMLCodeFactory.outputPlotSettings()
        lines = []
        lines.append("from mpl_toolkits.mplot3d import Axes3D")
        lines.append("fig = plt.figure(num=None, figsize={}, dpi={}, facecolor='{}', edgecolor='{}')".format(settings.figsize, settings.dpi, settings.facecolor, settings.edgecolor))
        lines.append("from matplotlib import gridspec")
        lines.append("__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])")
        # lines.append("ax = fig.gca(projection='3d')")

        title = output.getId()
        if output.isSetName():
            title = output.getName()

        oneXLabel = True
        oneYLabel = True
        allXLabel = None
        allYLabel = None

        for kc, surf in enumerate(output.getListOfSurfaces()):
            xId = surf.getXDataReference()
            yId = surf.getYDataReference()
            zId = surf.getZDataReference()
            dgx = doc.getDataGenerator(xId)
            dgy = doc.getDataGenerator(yId)
            dgz = doc.getDataGenerator(zId)

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
            
            kwargs = {}
            kwargs["color"] = "'" + settings.colors[kc % len(settings.colors)] + "'"
            kwargs["linewidth"] = settings.linewidth
            kwargs["marker"] = "'" + settings.marker + "'"
            kwargs["ms"] = settings.markersize
            kwargs["alpha"] = settings.alpha
            kwargs["label"] = "'" + zLabel + "'"

            mode = "plot"
            
            if (surf.isSetType()):
                mode = surface_types[surf.getType()]
            if (surf.isSetStyle()):
                style = doc.getEffectiveStyle(surf.getStyle())
                if style.isSetLineStyle():
                    line = style.getLineStyle()
                    if line.isSetColor():
                        kwargs["color"] = "'" + line.getColor() + "'"
                    if line.isSetThickness():
                        kwargs["linewidth"] = line.getThickness()
                    if line.isSetType():
                        ltype = line_types[line.getType()]
                if mode=="plot" and style.isSetMarkerStyle():
                    marker = style.getMarkerStyle()
                    if marker.isSetType():
                        kwargs["marker"] = marker.getType()
                    if marker.isSetFill():
                        kwargs["mfc"] = "'" + marker.getFill() + "'"
                    if marker.isSetLineColor():
                        kwargs["mec"] = "'" + marker.getLineColor() + "'"
                    if marker.isSetSize():
                        kwargs["ms"] = marker.getSize()
                    if marker.isSetLineThickness():
                        kwargs["mew"] = marker.getLineThickness()
                if style.isSetFillStyle():
                    fill = style.getFillStyle()
                    if fill.isSetColor():
                        kwargs["fillcolor"] = "'" + fill.getColor() + "'";
            if mode=="contour":
                kwargs["levels"] = 30
            if mode=="pcolormesh":
                kwargs["cmap"] = "'RdBu'"
                kwargs["shading"] = "'auto'"
                lines.append("ax = plt.subplot(__gs[0])")
            else:
                lines.append("ax = plt.subplot(__gs[0], projection='3d')")
            if mode=="plot":
                lines.append("for k in range({}.shape[1]):".format(xId))
                lines.append("    if k == 0:")
                plotline = "        ax." + mode + "({}[:,k], {}[:,k], {}[:,k]".format(xId, yId, zId)
                for kwarg in kwargs:
                    plotline = plotline + ", " + kwarg + "=" + str(kwargs[kwarg])
                # lines.append("        ax.plot({}[:,k], {}[:,k], {}[:,k], marker = '{}', color='{}', linewidth={}, markersize={}, alpha={}, label='{}')".format(xId, yId, zId, mtype, color, linewidth, markersize, alpha, zLabel))
                plotline += ")"
                lines.append(plotline)
                lines.append("    else:")
                plotline = "        ax." + mode + "({}[:,k], {}[:,k], {}[:,k]".format(xId, yId, zId)
                for kwarg in kwargs:
                    if kwarg=="label":
                        continue
                    plotline = plotline + ", " + kwarg + "=" + str(kwargs[kwarg])
                plotline += ")"
                # lines.append("        ax.plot({}[:,k], {}[:,k], {}[:,k], marker = '{}', color='{}', linewidth={}, markersize={}, alpha={})".format(xId, yId, zId, mtype, color, linewidth, markersize, settings.alpha))
                lines.append(plotline)
            else:
                del kwargs["marker"]
                del kwargs["ms"]
                if "fillcolor" in kwargs:
                    kwargs["color"] = kwargs["fillcolor"]
                    del kwargs["fillcolor"]
                plotline = "ax." + mode + "({}, {}, {}".format(xId, yId, zId)
                for kwarg in kwargs:
                    plotline = plotline + ", " + kwarg + "=" + str(kwargs[kwarg])
                # lines.append("        ax.plot({}[:,k], {}[:,k], {}[:,k], marker = '{}', color='{}', linewidth={}, markersize={}, alpha={}, label='{}')".format(xId, yId, zId, mtype, color, linewidth, markersize, alpha, zLabel))
                plotline += ")"
                lines.append(plotline)
                

        lines.append("ax.set_title('{}', fontweight='bold')".format(title))
        if oneXLabel:
            lines.append("ax.set_xlabel('{}', fontweight='bold')".format(xLabel))
        if oneYLabel:
            lines.append("ax.set_ylabel('{}', fontweight='bold')".format(yLabel))
        if len(output.getListOfSurfaces()) == 1 and mode != "pcolormesh":
            lines.append("ax.set_zlabel('{}', fontweight='bold')".format(zLabel))
            
        if mode=="plot":
            lines.append("__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)")
            lines.append("__lg.draw_frame(False)")
            lines.append("plt.setp(__lg.get_texts(), fontsize='small')")
            lines.append("plt.setp(__lg.get_texts(), fontweight='bold')")
        lines.append("plt.tick_params(axis='both', which='major', labelsize=10)")
        lines.append("plt.tick_params(axis='both', which='minor', labelsize=8)")
        lines.append("plt.savefig(os.path.join(workingDir, '{}.png'), dpi=100)".format(output.getId()))
        lines.append("plt.show()")

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
        errorlog = doc.getErrorLog()
        msg = errorlog.toString()
        if doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_ERROR) > 0:
            # FIXME: workaround for https://github.com/fbergmann/libSEDML/issues/47
            warnings.warn(msg)
            # raise IOError(msg)
        if errorlog.getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_FATAL) > 0:
            # raise IOError(msg)
            warnings.warn(msg)
        if errorlog.getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_WARNING) > 0:
            warnings.warn(msg)
        if errorlog.getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_SCHEMA_ERROR) > 0:
            warnings.warn(msg)
        if errorlog.getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_GENERAL_WARNING) > 0:
            warnings.warn(msg)

    @classmethod
    def readSEDMLDocument(cls, inputStr, workingDir):
        """ Parses SedMLDocument from given input.

        :return: dictionary of SedDocument, inputType and working directory.
        :rtype: {doc, inputType, workingDir}
        """

        # SEDML-String
        if not os.path.exists(inputStr):
            try:
                from xml.etree import ElementTree
                x = ElementTree.fromstring(inputStr)
                # is parsable xml string
                doc = libsedml.readSedMLFromString(inputStr)
                doc.sortOrderedObjects()
                inputType = cls.INPUT_TYPE_STR
                if workingDir is None:
                    workingDir = os.getcwd()

            except ElementTree.ParseError:
                if not os.path.exists(inputStr):
                    raise IOError("SED-ML String is not valid XML:", inputStr)

        # SEDML-File
        else:
            filename, extension = os.path.splitext(os.path.basename(inputStr))

            # Archive
            if zipfile.is_zipfile(inputStr):
                omexPath = inputStr
                inputType = cls.INPUT_TYPE_FILE_COMBINE

                # in case of sedx and combine a working directory is created
                # in which the files are extracted
                if workingDir is None:
                    extractDir = os.path.join(os.path.dirname(os.path.realpath(omexPath)), '_te_{}'.format(filename))
                else:
                    extractDir = workingDir


                # TODO: refactor this
                # extract the archive to working directory
                CombineArchive.extractArchive(omexPath, extractDir)
                # get SEDML files from archive
                sedmlFiles = CombineArchive.filePathsFromExtractedArchive(extractDir, filetype='sed-ml')

                if len(sedmlFiles) == 0:
                    raise IOError("No SEDML files found in archive.")

                # FIXME: there could be multiple SEDML files in archive (currently only first used)
                # analogue to executeOMEX
                if len(sedmlFiles) > 1:
                    warnings.warn("More than one sedml file in archive, only processing first one.")

                sedmlFile = sedmlFiles[0]
                doc = libsedml.readSedMLFromFile(sedmlFile)
                doc.sortOrderedObjects()
                # we have to work relative to the SED-ML file
                workingDir = os.path.dirname(sedmlFile)

                cls.checkSEDMLDocument(doc)


            # SEDML single file
            elif os.path.isfile(inputStr):
                if extension not in [".sedml", '.xml']:
                    raise IOError("SEDML file should have [.sedml|.xml] extension:", inputStr)
                inputType = cls.INPUT_TYPE_FILE_SEDML
                doc = libsedml.readSedMLFromFile(inputStr)
                cls.checkSEDMLDocument(doc)
                doc.sortOrderedObjects()
                # working directory is where the sedml file is
                if workingDir is None:
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
            if mid in model_sources and not model_sources[mid] == mid:
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


def process_trace(trace):
    """ If each entry in the task consists of a single point
    (e.g. steady state scan), concatenate the points.
    Otherwise, plot as separate curves."""
    if trace.size > 1:
        if len(trace.shape) == 1:
            return np.concatenate((np.atleast_1d(trace), np.atleast_1d(np.nan)))
        elif len(trace.shape) == 2:
            result = np.vstack((np.atleast_1d(trace), np.full((1,trace.shape[-1]), np.nan)))
            return result
    else:
        return np.atleast_1d(trace)


def terminate_trace(trace):
    """ If each entry in the task consists of a single point
    (e.g. steady state scan), concatenate the points.
    Otherwise, plot as separate curves."""
    warnings.warn("don't use this", DeprecationWarning)

    if isinstance(trace, list):
        if len(trace) > 0 and not isinstance(trace[-1], list) and not isinstance(trace[-1], dict):
            # if len(trace) > 2 and isinstance(trace[-1], dict):
            # e = np.array(trace[-1], copy=True)
            e = {}
            for name in trace[-1].colnames:
                e[name] = np.atleast_1d(np.nan)
            # print('e:')
            # print(e)
            return trace + [e]
    return trace


def fix_endpoints(x, y, color, tag, fig):
    """ Adds endpoint markers wherever there is a discontinuity in the data."""
    warnings.warn("don't use this", DeprecationWarning)
    # expect x and y to be 1d
    if len(x.shape) > 1:
        raise RuntimeError('Expected x to be 1d')
    if len(y.shape) > 1:
        raise RuntimeError('Expected y to be 1d')
    x_aug = np.concatenate((np.atleast_1d(np.nan), np.atleast_1d(x), np.atleast_1d(np.nan)))
    y_aug = np.concatenate((np.atleast_1d(np.nan), np.atleast_1d(y), np.atleast_1d(np.nan)))
    w = np.argwhere(np.isnan(x_aug))

    endpoints_x = []
    endpoints_y = []

    for begin, end in ( (int(w[k]+1), int(w[k+1])) for k in range(w.shape[0]-1) ):
        if begin != end:
            #print('begin {}, end {}'.format(begin, end))
            x_values = x_aug[begin:end]
            x_identical = np.all(x_values == x_values[0])
            y_values = y_aug[begin:end]
            y_identical = np.all(y_values == y_values[0])
            #print('x_values')
            #print(x_values)
            #print('x identical? {}'.format(x_identical))
            #print('y_values')
            #print(y_values)
            #print('y identical? {}'.format(y_identical))

            if x_identical and y_identical:
                # get the coords for the new markers
                x_begin = x_values[0]
                x_end   = x_values[-1]
                y_begin = y_values[0]
                y_end   = y_values[-1]

                # append to the lists
                endpoints_x += [x_begin, x_end]
                endpoints_y += [y_begin, y_end]

        if endpoints_x:
            fig.addXYDataset(np.array(endpoints_x), np.array(endpoints_y), color=color, tag=tag, mode='markers')


##################################################################################################
if __name__ == "__main__":
    import os
    from tellurium.tests.testdata import SEDML_TEST_DIR, OMEX_TEST_DIR
    import matplotlib

    def testInput(sedmlInput):
        """ Test function run on inputStr. """
        print('\n', '*'*100)
        print(sedmlInput)
        print('*'*100)
        factory = SEDMLCodeFactory(sedmlInput)

        # create python file
        python_str = factory.toPython()
        realPath = os.path.realpath(sedmlInput)
        with open(sedmlInput + '.py', 'w') as f:
            f.write(python_str)

        # execute python
        factory.executePython()

    # testInput(os.path.join(sedmlDir, "sedMLBIOM21.sedml"))

    # Check sed-ml files
    for fname in sorted(os.listdir(SEDML_TEST_DIR)):
        if fname.endswith(".sedml"):
            testInput(os.path.join(SEDML_TEST_DIR, fname))

    # Check sedx archives
    for fname in sorted(os.listdir(OMEX_TEST_DIR)):
        if fname.endswith(".sedx"):
            testInput(os.path.join(OMEX_TEST_DIR, fname))

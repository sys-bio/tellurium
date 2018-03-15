"""
Main tellurium entry point.

The module tellurium provides support routines.
As part of this module an ExendedRoadRunner class is defined which provides helper methods for
model export, plotting or the Jarnac compatibility layer.
"""

##############################################
# Core imports
##############################################

from __future__ import print_function, division, absolute_import

import sys
import os
import random
import warnings
import importlib
import json
import numpy as np
import antimony
import matplotlib

PLOTTING_ENGINE_NULL = 'null'
PLOTTING_ENGINE_MATPLOTLIB = 'matplotlib'
PLOTTING_ENGINE_PLOTLY = 'plotly'

__default_plotting_engine = PLOTTING_ENGINE_MATPLOTLIB

# enable fixes for Spyder (no Plotly support, no Agg support)
SPYDER = False
if any('SPYDER' in name for name in os.environ):
    SPYDER = True

# use Agg backend in notebooks or when Tkinter is not present
try:
    get_ipython()
    if not SPYDER:
        matplotlib.use('Agg')
except:
    try:
        import Tkinter
    except ImportError:
        if not SPYDER:
          matplotlib.use('Agg')


##############################################
# Ipython helpers
##############################################

# determine if we're running in IPython
__in_ipython = True
__plotly_enabled = False
if not SPYDER:
    try:
        get_ipython()

        # init plotly notebook mode
        try:
            import plotly
            plotly.offline.init_notebook_mode(connected=True)
            __plotly_enabled = True
            __default_plotting_engine = PLOTTING_ENGINE_PLOTLY
        except:
            warnings.warn("plotly could not be initialized. Unable to use Plotly for plotting.")
    except:
        __in_ipython = False


def inIPython():
    """ Checks if tellurium is used in IPython.

    Returns true if tellurium is being using in
    an IPython environment, false otherwise.
    :return: boolean
    """
    global __in_ipython
    return __in_ipython


def getDefaultPlottingEngine():
    """ Get the default plotting engine.
    Options are 'matplotlib' or 'plotly'.
    :return:
    """
    global __default_plotting_engine
    return __default_plotting_engine


def setDefaultPlottingEngine(engine):
    """ Set the default plotting engine. Overrides current value.

    :param engine: A string describing which plotting engine to use. Valid values are 'matplotlib' and 'plotly'.
    """
    if engine not in [PLOTTING_ENGINE_PLOTLY,
                      PLOTTING_ENGINE_MATPLOTLIB,
                      PLOTTING_ENGINE_NULL]:
        raise ValueError('Plotting engine is not supported: {}'.format(engine))
    global __default_plotting_engine
    __default_plotting_engine = engine


def disablePlotting():
    setDefaultPlottingEngine(PLOTTING_ENGINE_NULL)


__save_plots_to_pdf = False  # flag which decides if plotted to pdf


def setSavePlotsToPDF(value):
    """ Sets whether plots should be saved to PDF. """
    global __save_plots_to_pdf
    __save_plots_to_pdf = value


##############################################
# Plotting helpers
##############################################
import matplotlib.pyplot as plt

# make this the default style for matplotlib
# plt.style.use('fivethirtyeight')

from .plotting import getPlottingEngineFactory as __getPlottingEngineFactory, plot, show, nextFigure, tiledFigure, newTiledFigure, newLowerTriFigure, clearTiledFigure


def getPlottingEngineFactory(engine=None):
    global __save_plots_to_pdf
    if engine is None:
        engine = getDefaultPlottingEngine()
    factory = __getPlottingEngineFactory(engine)
    factory.save_plots_to_pdf = __save_plots_to_pdf
    return factory


__plotting_engines = {}


def getPlottingEngine(engine=None):
    global __plotting_engines
    if engine is None:
        engine = getDefaultPlottingEngine()
    if not engine in __plotting_engines:
        __plotting_engines[engine] = getPlottingEngineFactory(engine)()
    return __plotting_engines[engine]


getPlottingEngineFactory.__doc__ = __getPlottingEngineFactory.__doc__


##############################################
# Remaining imports
##############################################
import roadrunner

try:
    import tesedml as libsedml
except ImportError as e:
    try:
        import libsedml
    except ImportError:
        libsedml = None
        roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
        warnings.warn("'libsedml' could not be imported", ImportWarning, stacklevel=2)

try:
    try:
        import tesbml as libsbml
    except ImportError:
        import libsbml
except ImportError as e:
    libsbml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
    warnings.warn("'libsbml' could not be imported", ImportWarning, stacklevel=2)

try:
    import phrasedml
except ImportError as e:
    phrasedml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
    warnings.warn("'phrasedml' could not be imported", ImportWarning, stacklevel=2)

try:
    import sbol
except ImportError as e:
    sbol = None
    warnings.warn("'pySBOL' could not be imported, cannot import/export SBOL files", ImportWarning, stacklevel=2)

try:
    from sbml2matlab import sbml2matlab
except ImportError as e:
    sbml2matlab = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
    warnings.warn("'sbml2matlab' could not be imported", ImportWarning)

from . import teconverters


# ---------------------------------------------------------------------
# Group: Utility
# ---------------------------------------------------------------------

def getVersionInfo():
    """ Returns version information for tellurium included packages.

    :returns: list of tuples (package, version)
    """
    versions = [
        ('tellurium', getTelluriumVersion()),
        ('roadrunner', roadrunner.__version__),
        ('antimony', antimony.__version__),
    ]
    if libsbml:
        versions.append(('libsbml', libsbml.getLibSBMLDottedVersion()))
    if libsedml:
        versions.append(('libsedml', libsedml.getLibSEDMLVersionString()))
    if phrasedml:
        versions.append(('phrasedml', phrasedml.__version__))
    if sbol:
        versions.append(('pySBOL', sbol.__version__))
    return versions


def printVersionInfo():
    """ Prints version information for tellurium included packages.

    see also: :func:`getVersionInfo`
    """
    versions = getVersionInfo()
    for v in versions:
        print(v[0], ':', v[1])


def getTelluriumVersion():
    """ Version number of tellurium.

    :returns: version
    :rtype: str
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'VERSION.txt'), 'r') as f:
            version = f.read().rstrip()
    except:
        with open(os.path.join(os.path.dirname(__file__), 'VERSION.txt'), 'r') as f:
            version = f.read().rstrip()
    return version


def noticesOff():
    """Switch off the generation of notices to the user.
    Call this to stop roadrunner from printing warning message to the console.

    See also :func:`noticesOn`
    """
    roadrunner.Logger.setLevel(roadrunner.Logger.LOG_WARNING)


def noticesOn():
    """ Switch on notice generation to the user.

    See also :func:`noticesOff`
    """
    roadrunner.Logger.setLevel(roadrunner.Logger.LOG_NOTICE)


# ---------------------------------------------------------------------
# Group: Loading Models
# ---------------------------------------------------------------------

__te_models = {}
def __set_model(model_name, rr):
    __te_models[model_name] = rr

def model(model_name):
    """Retrieve a model which has already been loaded.

    :param model_name: the name of the model
    :type model_name: str
    """
    if not model_name in __te_models:
        raise KeyError('No such model has been loaded: {}'.format(model_name))
    return __te_models[model_name]

def _checkAntimonyReturnCode(code):
    """ Helper for checking the antimony response code.
    Raises Exception if error in antimony.

    :param code: antimony response
    :type code: int
    """
    if code < 0:
        raise Exception('Antimony: {}'.format(antimony.getLastError()))

def colorCycle(color,polyNumber):
    """ Adjusts contents of self.color as needed for plotting methods."""
    if len(color) < polyNumber:
        for i in range(polyNumber - len(color)):
            color.append(color[i])
    else:
        for i in range(len(color) - polyNumber):
            del color[-(i+1)]
    return color

def sample_plot(result):
    color = ['#0F0F3D', '#141452', '#1A1A66', '#1F1F7A', '#24248F', '#2929A3',
             '#2E2EB8', '#3333CC', '#4747D1', '#5C5CD6']
    if len(color) != result.shape[1]:
        color = colorCycle(color,10)
    for i in range(result.shape[1] - 1):
        plt.plot(result[:, 0], result[:, i + 1], color=color[i],
                 linewidth=2.5, label="SomeLabel")
    plt.xlabel('time')
    plt.ylabel('concentration')
    plt.suptitle("Sample Plot")
    plt.legend()
    plt.show()

def plotImage(img):
    imgplot = plt.imshow(img)
    plt.show()
    plt.close()

def custom_plot(x, y, min_y,max_y, label_name , **kwargs):
    ax = kwargs.pop('ax', plt.gca())
    base_line, = ax.plot(x, y, label=label_name,**kwargs)
    ax.fill_between(x, min_y, max_y, facecolor=base_line.get_color(), alpha=0.3)
    # Now add the legend with some customizations.


def plot_stochastic_result(result):
    plt.close()
    if(len(result) < 1):
        return
    col_names = result[0][0]
    sim_result = np.array([item[1] for item in result])
    mean_result = sim_result.mean(0)
    min_result = sim_result.min(0)
    max_result = sim_result.max(0)

    for col in range(1,len(col_names)):
        X = mean_result[:,0]
        Y = mean_result[:,col]

        min_y = min_result[:,col]
        max_y = max_result[:,col]
        custom_plot(X,Y,min_y,max_y,col_names[col])

    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend()
    plt.show()

def distributed_stochastic_simulation(sc,stochastic_model_object, num_simulations, model_type="antimony"):
    def stochastic_work(model_object):
        import tellurium as te
        if model_type == "antimony":
            model_roadrunner = te.loada(model_object.model)
        else:
            model_roadrunner = te.loadSBMLModel(model_object.model)
        model_roadrunner.integrator = model_object.integrator
        # seed the randint method with the current time
        random.seed()
        # it is now safe to use random.randint
        model_roadrunner.setSeed(random.randint(1000, 99999))
        model_roadrunner.integrator.variable_step_size = model_object.variable_step_size
        model_roadrunner.reset()
        simulated_data = model_roadrunner.simulate(model_object.from_time, model_object.to_time, model_object.step_points)
        return([simulated_data.colnames,np.array(simulated_data)])

    return(sc.parallelize([stochastic_model_object]*num_simulations,num_simulations).map(stochastic_work).collect())


def plot_distributed_stochastic(plot_data):
    fig = getPlottingEngine().newFigure(title='Stochastic Result')
    for each_data in plot_data:
        for i_column in range(1,len(each_data[0])):
            name = each_data[0][i_column]
            fig.addXYDataset([i_data[0] for i_data in each_data[1]],[i_data[i_column] for i_data in each_data[1]],  name=name)
    fig.plot()

def distributed_parameter_scanning(sc,list_of_models, function_name,antimony="antimony"):
    def spark_work(model_with_parameters):
        import tellurium as te
        if(antimony == "antimony"):
            model_roadrunner = te.loada(model_with_parameters[0])
        else:
            model_roadrunner = te.loadSBMLModel(model_with_parameters[0])
        parameter_scan_initilisation = te.ParameterScan(model_roadrunner,**model_with_parameters[1])
        simulator = getattr(parameter_scan_initilisation, function_name)
        return(simulator())

    return(sc.parallelize(list_of_models,len(list_of_models)).map(spark_work).collect())

def distributed_sensitivity_analysis(sc,senitivity_analysis_model,calculation=None):
    def spark_sensitivity_analysis(model_with_parameters):
        import tellurium as te

        sa_model = model_with_parameters[0]

        parameters = model_with_parameters[1]
        class_name = importlib.import_module(sa_model.filename)

        user_defined_simulator = getattr(class_name, dir(class_name)[0])
        sa_model.simulation = user_defined_simulator()

        if(sa_model.sbml):
            model_roadrunner = te.loadAntimonyModel(te.sbmlToAntimony(sa_model.model))
        else:
            model_roadrunner = te.loadAntimonyModel(sa_model.model)

        model_roadrunner.conservedMoietyAnalysis = sa_model.conservedMoietyAnalysis


        #Running PreSimulation
        model_roadrunner = sa_model.simulation.presimulator(model_roadrunner)

        #Running Analysis
        computations = {}
        model_roadrunner = sa_model.simulation.simulator(model_roadrunner,computations)

        _analysis = [None,None]

        #Setting the Parameter Variables
        _analysis[0] = {}
        for i_param,param_names in enumerate(sa_model.bounds.keys()):

            _analysis[0][param_names] = parameters[i_param]
            setattr(model_roadrunner, param_names, parameters[i_param])

        _analysis[1] = computations

        return _analysis


    if(senitivity_analysis_model.bounds is  None):
        print("Bounds are Undefined.")
        return

    #Get the Filename
    sc.addPyFile(senitivity_analysis_model.filename)
    senitivity_analysis_model.filename = os.path.basename(senitivity_analysis_model.filename).split(".")[0]


    params = []
    if(senitivity_analysis_model.allowLog):
        for bound_values in senitivity_analysis_model.bounds.values():
            if(len(bound_values) > 2):
                params.append(np.logspace(bound_values[0], bound_values[1], bound_values[2]))
            elif(len(bound_values == 2)):
                params.append(np.logspace(bound_values[0], bound_values[1], 3))
            else:
                print("Improper Boundaries Defined")
                return;
    else:
        for bound_values in senitivity_analysis_model.bounds.values():
            if(len(bound_values) > 2):
                params.append(np.linspace(bound_values[0], bound_values[1], bound_values[2]))
            elif(len(bound_values == 2)):
                params.append(np.linspace(bound_values[0], bound_values[1], 3))
            else:
                print("Improper Boundaries Defined")
                return;

    samples = perform_sampling(np.meshgrid(*params))
    samples = zip([senitivity_analysis_model]*len(samples),samples)
    if(calculation is "avg"):
        group_rdd = sc.parallelize(samples,len(samples)).map(spark_sensitivity_analysis).\
            flatMap(lambda x: x[1].items()).groupByKey()

        KEYS = group_rdd.map(lambda x: (x[0])).collect()
        VALUES = group_rdd.map(lambda x: np.array(list(x[1])))
        values_array = np.array(VALUES.collect())
        MEANS = (np.average(values_array, axis=1))
        STD =  (np.std(values_array, axis=1))

        stats = {}
        for key_i,each_key in enumerate(KEYS):
            stats[each_key] = {}
            stats[each_key]["mean"] = MEANS[key_i]
            stats[each_key]["stdev"] = STD[key_i]
        return stats

    elif(type(calculation) is dict):
        bins = sc.broadcast(calculation)
        group_rdd = sc.parallelize(samples,len(samples)).map(spark_sensitivity_analysis)\
            .flatMap(lambda x: x[1].items()).map(
            lambda x: (x[0], [int(items[0] <= x[1] <= items[1]) for items in bins.value[x[0]]])).reduceByKey(
            lambda first, second: [x + y for x, y in zip(first, second)])

        return group_rdd.collect()

    else:
        return(sc.parallelize(samples,len(samples)).map(spark_sensitivity_analysis).collect())



def perform_sampling(mesh):
    samples = []
    mesh = [items.flatten() for items in mesh]
    for i in range(len(mesh[0])):
        samples.append([items[i] for items in mesh])
    return(samples)


def loada(ant):
    """Load model from Antimony string.

    See also: :func:`loadAntimonyModel`
    ::

        r = te.loada('S1 -> S2; k1*S1; k1=0.1; S1=10.0; S2 = 0.0')

    :param ant: Antimony model
    :type ant: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.ExtendedRoadRunner
    """
    return loadAntimonyModel(ant)


def loadAntimonyModel(ant):
    """Load Antimony model with tellurium.

    See also: :func:`loada`
    ::

        r = te.loadAntimonyModel('S1 -> S2; k1*S1; k1=0.1; S1=10.0; S2 = 0.0')

    :param ant: Antimony model
    :type ant: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.ExtendedRoadRunner
    """
    sbml = antimonyToSBML(ant)
    return roadrunner.RoadRunner(sbml)


def loads(ant):
    """Load SBML model with tellurium

    See also: :func:`loadSBMLModel`

    :param ant: SBML model
    :type ant: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.ExtendedRoadRunner
    """
    return loadSBMLModel(ant)


def loadSBMLModel(sbml):
    """ Load SBML model from a string or file.

    :param sbml: SBML model
    :type sbml: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.ExtendedRoadRunner
    """
    return roadrunner.RoadRunner(sbml)


def loadCellMLModel(cellml):
    """ Load CellML model with tellurium.

    :param cellml: CellML model
    :type cellml: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.ExtendedRoadRunner
    """
    sbml = cellmlToSBML(cellml)
    return roadrunner.RoadRunner(sbml)


# ---------------------------------------------------------------------
# Interconversion Methods
# ---------------------------------------------------------------------
def antimonyTosbml(ant):
    warnings.warn("'antimonyTosbml' is deprecated. Use 'antimonyToSBML' instead. Will be removed in tellurium v1.4",
                  DeprecationWarning, stacklevel=2)
    return antimonyToSBML(ant)


def antimonyToSBML(ant):
    """ Convert Antimony to SBML string.

    :param ant: Antimony string or file
    :type ant: str | file
    :return: SBML
    :rtype: str
    """
    if os.path.isfile(ant):
        code = antimony.loadAntimonyFile(ant)
    else:
        code = antimony.loadAntimonyString(ant)
    _checkAntimonyReturnCode(code)
    mid = antimony.getMainModuleName()
    return antimony.getSBMLString(mid)



def antimonyToCellML(ant):
    """ Convert Antimony to CellML string.

    :param ant: Antimony string or file
    :type ant: str | file
    :return: CellML
    :rtype: str
    """
    if os.path.isfile(ant):
        code = antimony.loadAntimonyFile(ant)
    else:
        code = antimony.loadAntimonyString(ant)
    _checkAntimonyReturnCode(code)
    mid = antimony.getMainModuleName()
    return antimony.getCellMLString(mid)


def sbmlToAntimony(sbml):
    """ Convert SBML to antimony string.

    :param sbml: SBML string or file
    :type sbml: str | file
    :return: Antimony
    :rtype: str
    """
    isfile = False
    try:
        isfile = os.path.isfile(sbml)
    except:
        pass
    if isfile:
        code = antimony.loadSBMLFile(sbml)
    else:
        code = antimony.loadSBMLString(str(sbml))
    _checkAntimonyReturnCode(code)
    return antimony.getAntimonyString(None)


def sbmlToCellML(sbml):
    """ Convert SBML to CellML string.

    :param sbml: SBML string or file
    :type sbml: str | file
    :return: CellML
    :rtype: str
    """
    if os.path.isfile(sbml):
        code = antimony.loadSBMLFile(sbml)
    else:
        code = antimony.loadSBMLString(sbml)
    _checkAntimonyReturnCode(code)
    return antimony.getCellMLString(None)

def cellmlToAntimony(cellml):
    """ Convert CellML to antimony string.

    :param cellml: CellML string or file
    :type cellml: str | file
    :return: antimony
    :rtype: str
    """
    if os.path.isfile(cellml):
        code = antimony.loadCellMLFile(cellml)
    else:
        code = antimony.loadCellMLString(cellml)
    _checkAntimonyReturnCode(code)
    return antimony.getAntimonyString(None)


def cellmlToSBML(cellml):
    """ Convert CellML to SBML string.

    :param cellml: CellML string or file
    :type cellml: str | file
    :return: SBML
    :rtype: str
    """
    if os.path.isfile(cellml):
        code = antimony.loadCellMLFile(cellml)
    else:
        code = antimony.loadCellMLString(cellml)
    _checkAntimonyReturnCode(code)
    return antimony.getSBMLString(None)

def exportInlineOmex(inline_omex, export_location):
    """ Export an inline OMEX string to a COMBINE archive.

    :param inline_omex: String containing inline OMEX describing models and simulations.
    :param export_location: Filepath of Combine archive to create.
    """
    from .teconverters import saveInlineOMEX
    saveInlineOMEX(inline_omex, export_location)


def executeInlineOmex(inline_omex):
    """ Execute inline phrasedml and antimony.

    :param inline_omex: String containing inline phrasedml and antimony.
    """
    in_omex = teconverters.inlineOmex.fromString(inline_omex)
    in_omex.executeOmex()


def executeInlineOmexFromFile(filepath):
    """ Execute inline OMEX with simulations described in phrasedml and models described in antimony.

    :param filepath: Path to file containing inline phrasedml and antimony.
    """
    with open(filepath) as f:
        executeInlineOmex(f.read())

def convertCombineArchive(location):
    """ Read a COMBINE archive and convert its contents to an
    inline Omex.

    :param location: Filesystem path to the archive.
    """
    from .teconverters import inlineOmexImporter
    return inlineOmexImporter.fromFile(location).toInlineOmex()

def convertAndExecuteCombineArchive(location):
    """ Read and execute a COMBINE archive.

    :param location: Filesystem path to the archive.
    """
    from .teconverters import inlineOmexImporter
    inlineomex = inlineOmexImporter.fromFile(location).toInlineOmex()
    executeInlineOmex(inlineomex)

def extractFileFromCombineArchive(archive_path, entry_location):
    """ Extract a single file from a COMBINE archive and return it as a string.
    """
    warnings.warn('Use libcombine instead.', DeprecationWarning)
    # TODO: port this function
    import tecombine
    archive = tecombine.CombineArchive()
    if not archive.initializeFromArchive(archive_path):
        raise RuntimeError('Failed to initialize archive')
    try:
        entry = archive.getEntryByLocation(entry_location)
    except:
        raise RuntimeError('Could not find entry {}'.format(entry_location))
    return archive.extractEntryToString(entry_location)

def addFileToCombineArchive(archive_path, file_name, entry_location, file_format, master, out_archive_path):
    """ Add a file to an existing COMBINE archive on disk and save the result as a new archive.

    :param archive_path: The path to the archive.
    :param file_name: The name of the file to add.
    :param entry_location: The location to store the entry in the archive.
    :param file_format: The format of the file. Can use tecombine.KnownFormats.lookupFormat for common formats.
    :param master: Whether the file should be marked master.
    :param out_archive_path: The path to the output archive.
    """
    addFilesToCombineArchive(archive_path, [file_name], [entry_location], [file_format], [master], out_archive_path)

def addFilesToCombineArchive(archive_path, file_names, entry_locations, file_formats, master_attributes, out_archive_path):
    """ Add multiple files to an existing COMBINE archive on disk and save the result as a new archive.

    :param archive_path: The path to the archive.
    :param file_names: List of extra files to add.
    :param entry_locations: List of destination locations for the files in the output archive.
    :param file_format: List of formats for the resp. files.
    :param master_attributes: List of true/false values for the resp. master attributes of the files.
    :param out_archive_path: The path to the output archive.
    """
    import tecombine, tempfile
    input_archive = tecombine.CombineArchive()
    if not input_archive.initializeFromArchive(archive_path):
        raise RuntimeError('Failed to initialize archive')

    tempfiles = []

    output_archive = tecombine.CombineArchive()

    description = input_archive.getMetadataForLocation('.')
    if description:
        output_archive.addMetadata('.', description)

    for entry in (input_archive.getEntry(k) for k in range(input_archive.getNumEntries())):
        fhandle, fname = tempfile.mkstemp()
        tempfiles.append(fname)
        input_archive.extractEntry(entry.getLocation(), fname)
        if not entry.getLocation() in entry_locations:
            output_archive.addFile(
                                  fname,
                                  entry.getLocation(),
                                  entry.getFormat(),
                                  entry.getMaster())
    # add the extra files
    for file_name, entry_location, file_format, master in zip(file_names, entry_locations, file_formats, master_attributes):
        output_archive.addFile(file_name, entry_location, file_format, master)

    # if the archive already exists, clear it
    if os.path.exists(out_archive_path):
        if os.path.isfile(out_archive_path):
            os.remove(out_archive_path)
        elif os.path.isdir(out_archive_path):
            raise RuntimeError('Tried to write archive to {}, which is a directory.'.format(out_archive_path))
        else:
            raise RuntimeError('Could not write archive to {}.'.format(out_archive_path))
    # write archive
    output_archive.writeToFile(out_archive_path)

    # delete temp files
    for t in tempfiles:
        os.remove(t)


# ---------------------------------------------------------------------
# Math Utilities
# ---------------------------------------------------------------------
def getEigenvalues(m):
    """ Eigenvalues of matrix.

    Convenience method for computing the eigenvalues of a matrix m
    Uses numpy eig to compute the eigenvalues.

    :param m: numpy array
    :returns: numpy array containing eigenvalues
    """
    from numpy import linalg
    w, v = linalg.eig(m)
    return w


# ---------------------------------------------------------------------
# Plotting Utilities
# ---------------------------------------------------------------------
def plotArray(result, loc='upper right', show=True, resetColorCycle=True,
             xlabel=None, ylabel=None, title=None, xlim=None, ylim=None,
             xscale='linear', yscale="linear", grid=False, labels=None, **kwargs):
    """ Plot an array.

    The first column of the array must be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object. Note that you can add plotting options as named key values after
    the array. To add a legend, include the label legend values:

    te.plotArray (m, labels=['Label 1, 'Label 2', etc])

    Make sure you include as many labels as there are curves to plot!

    Use show=False to add multiple curves. Use color='red' to use the same color for every curve.
    ::

        import numpy as np
        result = np.array([[1,2,3], [7.2,6.5,8.8], [9.8, 6.5, 4.3]])
        te.plotArray(result, title="My graph', xlim=((0, 5)))
    """
    warnings.warn("plotArray is deprecated, use plot instead", DeprecationWarning)

    # FIXME: unify r.plot & te.plot (lots of code duplication)
    # reset color cycle (columns in repeated simulations have same color)
    if resetColorCycle:
        plt.gca().set_prop_cycle(None)

    if 'linewidth' not in kwargs:
            kwargs['linewidth'] = 2.0

    # get the labeles
    Ncol = result.shape[1]
    if labels is None:
        labels = result.dtype.names

    for k in range(1, Ncol):
        if loc is None or labels is None:
            # no legend or labels
            p = plt.plot(result[:, 0], result[:, k], **kwargs)
        else:
            p = plt.plot(result[:, 0], result[:, k], label=labels[k-1], **kwargs)

    # labels
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    # axis and grids
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.grid(grid)

    # show legend
    if loc is not None and labels is not None:
        plt.legend(loc=loc)
    # show plot
    if show:
        plt.show()
    return p

def plotWithLegend(r, result=None, loc='upper left', show=True, **kwargs):
    warnings.warn("'plotWithLegend' is deprecated. Use 'r.plot' instead. Will be removed in tellurium v1.4",
                  DeprecationWarning, stacklevel=2)
    return r.plot(result=result, loc=loc, show=show, **kwargs)


# ---------------------------------------------------------------------
# Test Models
# ---------------------------------------------------------------------
def loadTestModel(string):
    """Loads particular test model into roadrunner.
    ::

        rr = te.loadTestModel('feedback.xml')

    :returns: RoadRunner instance with test model loaded
    """
    import roadrunner.testing
    return roadrunner.testing.getRoadRunner(string)


def getTestModel(string):
    """SBML of given test model as a string.
    ::

        # load test model as SBML
        sbml = te.getTestModel('feedback.xml')
        r = te.loadSBMLModel(sbml)
        # simulate
        r.simulate(0, 100, 20)

    :returns: SBML string of test model
    """
    import roadrunner.testing
    return roadrunner.testing.getData(string)


def listTestModels():
    """ List roadrunner SBML test models.
    ::

        print(te.listTestModels())

    :returns: list of test model paths
    """
    import roadrunner.testing
    modelList = []
    fileList = roadrunner.testing.dir('*.xml')
    for pathName in fileList:
        modelList.append(os.path.basename(pathName))
    return modelList

# ---------------------------------------------------------------
# Extended roadrunner
# ---------------------------------------------------------------

from .roadrunner import ExtendedRoadRunner

def _model_function_factory(key):
    """ Dynamic creation of model functions.

    :param key: function key, i.e. the name of the function
    :type key: str
    :return: function object
    :rtype: function
    """
    def f(self):
        return getattr(self.model, key).__call__()
    # set the name
    f.__name__ = key
    # copy the docstring
    f.__doc__ = getattr(roadrunner.ExecutableModel, key).__doc__
    return f

# Add model functions to ExendedRoadRunner class
for key in ExtendedRoadRunner._model_functions:
    setattr(ExtendedRoadRunner, key, _model_function_factory(key))


# Now we assign the ExtendedRoadRunner to RoadRunner
def RoadRunner(*args):
    # return roadrunner.RoadRunner(*args)
    return ExtendedRoadRunner(*args)

roadrunner.RoadRunner = ExtendedRoadRunner

def VersionDict():
    '''Return dict of version strings.'''
    import tesbml, tesedml, tecombine
    return {
        'tellurium': getTelluriumVersion(),
        'roadrunner': roadrunner.getVersionStr(roadrunner.VERSIONSTR_BASIC),
        'antimony': antimony.__version__,
        'phrasedml': phrasedml.__version__,
        'tesbml': libsbml.getLibSBMLDottedVersion(),
        'tesedml': tesedml.__version__,
        'tecombine': tecombine.__version__
        }

def DumpJSONInfo():
    '''Tellurium dist info. Goes into COMBINE archive.'''
    return json.dumps({
        'authoring_tool': 'tellurium',
        'info': 'Created with Tellurium (tellurium.analogmachine.org).',
        'version_info': VersionDict()})

def getAppDir():
    import os
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return os.path.join(os.path.expanduser('~'), '.config', 'Tellurium')
    else:
        import appdirs
        return appdirs.user_data_dir('Tellurium', 'Tellurium')

_last_report = None
def setLastReport(report):
    '''Used by SED-ML to save the last report created (for validation).'''
    global _last_report
    _last_report = report

def getLastReport():
    '''Get the last report generated by SED-ML.'''
    global _last_report
    return _last_report

from .testcases import getSupportedTestCases

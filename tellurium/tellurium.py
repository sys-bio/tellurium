"""
The module tellurium provides support routines.
As part of this module an ExendedRoadRunner class is defined which provides helper methods for
model export, plotting or the Jarnac compatibility layer.
"""
from __future__ import print_function, division, absolute_import

import random
import os
import sys
import warnings
import importlib

# NOTE: not needed since we now require matplotlib >= 2.0.0
# check availability of property cycler (matplotlib 1.5ish)
# if True: # create dummy scope
#     import matplotlib
#     import matplotlib.pyplot as plt
#
#     print(dir(matplotlib))
#     fig = matplotlib.figure.Figure()
#     ax = fig.add_axes()
#     if not hasattr(ax, 'set_prop_cycle'):
#         warnings.warn("Your copy of matplotlib does not support color cycle control. Falling back to 'Picasso' mode. Please update to matplotlib 1.5 or later if you don't like modern art.")

__default_plotting_engine = 'matplotlib'

import antimony
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# determine if we're running in IPython
__in_ipython = True
__plotly_enabled = False
try:
    get_ipython()

    # init plotly notebook mode
    try:
        import plotly
        plotly.offline.init_notebook_mode(connected=True)
        __plotly_enabled = True
        __default_plotting_engine = 'plotly'
    except:
        warnings.warn("Plotly could not be initialized. Unable to use Plotly for plotting.")
except:
    __in_ipython = False

def inIPython():
    """ Returns true if tellurium is being using in
    an IPython environment, false otherwise.
    """
    global __in_ipython
    return __in_ipython

def getDefaultPlottingEngine():
    """ Get the default plotting engine. Can be 'matplotlib' or 'plotly'."""
    global __default_plotting_engine
    return __default_plotting_engine

def setDefaultPlottingEngine(value):
    """ Set the default plotting engine. Overrides current value.

    :param value: A string describing which plotting engine to use. Valid values are 'matplotlib' and 'pyplot'.
    """
    global __default_plotting_engine
    __default_plotting_engine = value

__save_plots_to_pdf = False
def setSavePlotsToPDF(value):
    """Sets whether plots should be saved to PDF"""
    global __save_plots_to_pdf
    __save_plots_to_pdf = value

import matplotlib.pyplot as plt

# make this the default style for matplotlib
# plt.style.use('fivethirtyeight')

from .plotting import getPlottingEngineFactory as __getPlottingEngineFactory

def getPlottingEngineFactory(engine=getDefaultPlottingEngine()):
    global __save_plots_to_pdf
    factory = __getPlottingEngineFactory(engine)
    factory.save_plots_to_pdf = __save_plots_to_pdf
    return factory

__plotting_engines = {}
def getPlottingEngine(engine=getDefaultPlottingEngine()):
    global __plotting_engines
    if not engine in __plotting_engines:
        __plotting_engines[engine] = getPlottingEngineFactory(engine)()
    return __plotting_engines[engine]

getPlottingEngineFactory.__doc__ = __getPlottingEngineFactory.__doc__

import roadrunner

try:
    import tesedml as libsedml
    # import libsedml before libsbml to handle
    # https://github.com/fbergmann/libSEDML/issues/21
except ImportError as e:
    libsedml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
    warnings.warn("'libsedml' could not be imported", ImportWarning, stacklevel=2)

try:
    import tesbml as libsbml
    # try to deactivate the libsbml timestamp if possible
    # see discussion https://groups.google.com/forum/?utm_medium=email&utm_source=footer#!msg/libsbml-development/Yy78LSwOHzU/9t5PcpD2AAAJ
    # try:
    #     libsbml.XMLOutputStream.setWriteTimestamp(False)
    # except AttributeError:
    #     warnings.warn("'libsbml' timestamps can not be deactivated in this libsbml version", ImportWarning, stacklevel=2)

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
        ('snbw_viewer', 'No information for sbnw viewer'),
    ]
    if libsbml:
        versions.append(('libsbml', libsbml.getLibSBMLDottedVersion()))
    if libsedml:
        versions.append(('libsedml', libsedml.getLibSEDMLVersionString()))
    if phrasedml:
        versions.append(('phrasedml', phrasedml.__version__))
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


def saveToFile(filePath, str):
    """ Save string to file.

    see also: :func:`readFromFile`

    :param filePath: file path to save to
    :param str: string to save
    """
    with open(filePath, 'w') as f:
        f.write(str)


def readFromFile(filePath):
    """ Load a file and return contents as a string.

    see also: :func:`saveToFile`

    :param filePath: file path to read from
    :returns: string representation of the contents of the file
    """
    with open(filePath, 'r') as f:
        string = f.read()
    return string


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

def distributed_sensitivity_analysis(sc,senitivity_analysis_model):
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

        r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S2 = 10')

    :param ant: Antimony model
    :type ant: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.RoadRunner
    """
    return loadAntimonyModel(ant)


def loadAntimonyModel(ant):
    """Load Antimony model with tellurium.

    See also: :func:`loada`

    :param ant: Antimony model
    :type ant: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.RoadRunner
    """
    sbml = antimonyToSBML(ant)
    return roadrunner.RoadRunner(sbml)


def loads(ant):
    """Load SBML model with tellurium

    See also: :func:`loadSBMLModel`

    :param ant: SBML model
    :type ant: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.RoadRunner
    """
    return loadSBMLModel(ant)


def loadSBMLModel(sbml):
    """ Load SBML model from a string or file.

    :param sbml: SBML model
    :type sbml: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.RoadRunner
    """
    return roadrunner.RoadRunner(sbml)


def loadCellMLModel(cellml):
    """ Load CellML model with tellurium.

    :param cellml: CellML model
    :type cellml: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.RoadRunner
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
    if os.path.isfile(sbml):
        code = antimony.loadSBMLFile(sbml)
    else:
        code = antimony.loadSBMLString(sbml)
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
    """ Execute inline phrasedml and antimony.

    :param inline_omex: String containing inline phrasedml and antimony.
    :param export_location: Filepath of Combine archive to export
    """
    from .teconverters import saveInlineOMEX
    saveInlineOMEX(inline_omex, export_location)

def executeInlineOmex(inline_omex):
    """ Execute inline phrasedml and antimony.

    :param inline_omex: String containing inline phrasedml and antimony.
    """
    omex = teconverters.inlineOmex.fromString(inline_omex).executeOmex()

def executeInlineOmexFromFile(filepath):
    """ Execute inline phrasedml and antimony.

    :param filepath: Path to file containing inline phrasedml and antimony.
    """
    with open(filepath) as f:
        executeInlineOmex(f.read())

def convertCombineArchive(location):
    """ Read a Combine archive and convert its contents to an
    inline Omex.

    :param location: Filesystem path to the archive.
    """
    from .teconverters import inlineOmexImporter
    return inlineOmexImporter.fromFile(location).toInlineOmex()

def convertAndExecuteCombineArchive(location):
    """ Read and execute a combine archive.

    :param location: Filesystem path to the archive.
    """
    from .teconverters import inlineOmexImporter
    inlineomex = inlineOmexImporter.fromFile(location).toInlineOmex()
    executeInlineOmex(inlineomex)

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



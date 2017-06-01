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
import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

import matplotlib
matplotlib.use('Agg')

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
import antimony

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

# from . import teconverters

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


def working():
    print("YES!!!")

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
    sb,pml = teconverters.partitionInlineOMEXString(inline_omex)
    pml = '\n'.join(pml)
    omex = teconverters.inlineOmex({'main.xml':pml},'main.xml',sb)
    omex.exportToCombine(export_location)

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

def convertAndExecuteCombineArchive(location):
    """ Read and execute a combine archive.

    :param location: Filesystem path to the archive.
    """
    from .teconverters import inlineOmexImporter
    executeInlineOmex(inlineOmexImporter.fromFile(location).toInlineOmex())

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


# ---------------------------------------------------------------------
# Extended RoadRunner class
# ---------------------------------------------------------------------
class ExtendedRoadRunner(roadrunner.RoadRunner):

    def __init__(self, *args, **kwargs):
        super(ExtendedRoadRunner, self).__init__(*args, **kwargs)

    # ---------------------------------------------------------------------
    # Model access
    # ---------------------------------------------------------------------
    # def getBoundarySpeciesConcentrations(self):
    #     return self.model.getBoundarySpeciesConcentrations()
    # getBoundarySpeciesConcentrations.__doc__ = roadrunner.ExecutableModel.getBoundarySpeciesConcentrations.__doc__

    # These model functions are attached after class creation
    _model_functions = [
        'getBoundarySpeciesConcentrations',
        'getBoundarySpeciesConcentrations',
        'getBoundarySpeciesIds',
        'getNumBoundarySpecies',

        'getFloatingSpeciesConcentrations',
        'getFloatingSpeciesIds',
        'getNumFloatingSpecies',

        'getGlobalParameterIds',
        'getGlobalParameterValues',
        'getNumGlobalParameters',

        'getCompartmentIds',
        'getCompartmentVolumes',
        'getNumCompartments',

        'getConservedMoietyValues',
        'getNumConservedMoieties',
        'getNumDepFloatingSpecies',
        'getNumIndFloatingSpecies',

        'getReactionIds',
        'getReactionRates',
        'getNumReactions',
        'getNumEvents',
        'getNumRateRules'
     ]

    # ---------------------------------------------------------------------
    # Jarnac compatibility layer
    # ---------------------------------------------------------------------
    def fjac(self):
        return self.getFullJacobian()
    fjac.__doc__ = roadrunner.RoadRunner.getFullJacobian.__doc__

    def sm(self):
        return self.getFullStoichiometryMatrix()
    sm.__doc__ = roadrunner.RoadRunner.getFullStoichiometryMatrix.__doc__

    def rs(self):
        return self.model.getReactionIds()
    rs.__doc__ = roadrunner.ExecutableModel.getReactionIds.__doc__

    def fs(self):
        return self.model.getFloatingSpeciesIds()
    fs.__doc__ = roadrunner.ExecutableModel.getFloatingSpeciesIds.__doc__

    def bs(self):
        return self.model.getBoundarySpeciesIds()
    bs.__doc__ = roadrunner.ExecutableModel.getBoundarySpeciesIds.__doc__

    def ps(self):
        return self.model.getGlobalParameterIds()
    ps.__doc__ = roadrunner.ExecutableModel.getGlobalParameterIds.__doc__

    def vs(self):
        return self.model.getCompartmentIds()
    vs.__doc__ = roadrunner.ExecutableModel.getCompartmentIds.__doc__

    def dv(self):
        return self.model.getStateVectorRate()
    dv.__doc__ = roadrunner.ExecutableModel.getStateVector.__doc__

    def rv(self):
        return self.model.getReactionRates()
    rv.__doc__ = roadrunner.ExecutableModel.getReactionRates.__doc__

    def sv(self):
        return self.model.getFloatingSpeciesConcentrations()
    sv.__doc__ = roadrunner.ExecutableModel.getFloatingSpeciesConcentrations.__doc__

    # ---------------------------------------------------------------------
    # Export Utilities
    # ---------------------------------------------------------------------
    def __getSBML(self, current):
        if current is True:
            return self.getCurrentSBML()
        else:
            return self.getSBML()

    def getAntimony(self, current=False):
        """ Antimony string of the original model loaded into roadrunner.

        :param current: return current model state
        :type current: bool
        :return: Antimony
        :rtype: str
        """
        sbml = self.__getSBML(current)
        return sbmlToAntimony(sbml)

    def getCurrentAntimony(self):
        """ Antimony string of the current model state.

        See also: :func:`getAntimony`
        :return: Antimony
        :rtype: str
        """
        return self.getAntimony(current=True)

    def getCellML(self, current=False):
        """ CellML string of the original model loaded into roadrunner.

        :param current: return current model state
        :type current: bool
        :returns: CellML string
        :rtype: str
        """
        sbml = self.__getSBML(current)
        return sbmlToCellML(sbml)

    def getCurrentCellML(self):
        """ CellML string of current model state.

        See also: :func:`getCellML`
        :returns: CellML string
        :rtype: str
        """
        return self.getCellML(current=True)

    def getMatlab(self, current=False):
        """ Matlab string of the original model loaded into roadrunner.

        See also: :func:`getCurrentMatlab`
        :returns: Matlab string
        :rtype: str
        """
        sbml = self.__getSBML(current)
        if sbml2matlab is not None:
            return sbml2matlab(sbml)
        else:
            warnings.warn("'sbml2matlab' could not be imported, no support for Matlab code generation",
                          RuntimeWarning, stacklevel=2)
            return ""

    def getCurrentMatlab(self):
        """ Matlab string of current model state.

        :param current: return current model state
        :type current: bool
        :returns: Matlab string
        :rtype: str
        """
        return self.getMatlab(current=True)

    def exportToSBML(self, filePath, current=True):
        """ Save current model as SBML file.

        :param current: export current model state
        :type current: bool
        :param filePath: file path of SBML file
        :type filePath: str
        """
        saveToFile(filePath, self.__getSBML(current))

    def exportToAntimony(self, filePath, current=True):
        """ Save current model as Antimony file.

        :param current: export current model state
        :type current: bool
        :param filePath: file path of Antimony file
        :type filePath: str
        """
        saveToFile(filePath, self.getAntimony(current))

    def exportToCellML(self, filePath, current=True):
        """ Save current model as CellML file.

        :param current: export current model state
        :type current: bool
        :param filePath: file path of CellML file
        :type filePath: str
        """
        saveToFile(filePath, self.getCellML(current))

    def exportToMatlab(self, filePath, current=True):
        """ Save current model as Matlab file.
        To save the original model loaded into roadrunner use
        current=False.

        :param self: RoadRunner instance
        :type self: RoadRunner.roadrunner
        :param filePath: file path of Matlab file
        :type filePath: str
        """
        saveToFile(filePath, self.getMatlab(current))

    # ---------------------------------------------------------------------
    # Reset Methods
    # ---------------------------------------------------------------------
    def resetToOrigin(self):
        """ Reset model to state when first loaded.

        This resets the model back to the state when it was FIRST loaded,
        this includes all init() and parameters such as k1 etc.

        identical to:
            r.reset(roadrunner.SelectionRecord.ALL)
        """
        self.reset(roadrunner.SelectionRecord.ALL)

    def resetAll(self):
        """ Reset all model variables to CURRENT init(X) values.

        This resets all variables, S1, S2 etc to the CURRENT init(X) values. It also resets all
        parameters back to the values they had when the model was first loaded.
        """
        self.reset(roadrunner.SelectionRecord.TIME |
                   roadrunner.SelectionRecord.RATE |
                   roadrunner.SelectionRecord.FLOATING |
                   roadrunner.SelectionRecord.GLOBAL_PARAMETER)

    # ---------------------------------------------------------------------
    # Routines flattened from model, aves typing and easier finding of methods
    # ---------------------------------------------------------------------
    def getRatesOfChange(self):
        """ Rate of change of all state variables in the model.

        :returns: rate of change of all state variables (eg species) in the model.
        """
        if self.conservedMoietyAnalysis:
            m1 = self.getLinkMatrix()
            m2 = self.model.getStateVectorRate()
            return m1.dot(m2)
        else:
            return self.model.getStateVectorRate()

    # ---------------------------------------------------------------------
    # Plotting Utilities
    # ---------------------------------------------------------------------
    def draw(self, **kwargs):
        """ Draws an SBMLDiagram of the current model.

        To set the width of the output plot provide the 'width' argument.
        Species are drawn as white circles (boundary species
        shaded in blue), reactions as grey squares.
        Currently only the drawing of medium-size networks is supported.
        """
        if any([ os.access( os.path.join( p, 'dot' ), os.X_OK ) for p in os.environ['PATH'].split( os.pathsep )]):
            warnings.warn("Graphviz is not installed in your machine. 'draw' command cannot produce a diagram",
                Warning, stacklevel=2)
        else:
            from visualization.sbmldiagram import SBMLDiagram
            diagram = SBMLDiagram(self.getSBML())
            diagram.draw(**kwargs)

    def plot(self, result=None, loc='upper right', show=True,
             xlabel=None, ylabel=None, title=None, xlim=None, ylim=None,
             xscale='linear', yscale="linear", grid=False, ordinates=None, **kwargs):
        warnings.warn("RoadRunner.plot is deprecated. Please use te.plot(data) instead.", DeprecationWarning)
        """ Plot roadrunner simulation data.

        Plot is called with simulation data to plot as the first argument. If no data is provided the data currently
        held by roadrunner generated in the last simulation is used. The first column is considered the x axis and
        all remaining columns the y axis.
        If the result array has no names, than the current r.selections are used for naming. In this case the
        dimension of the r.selections has to be the same like the number of columns of the result array.

        Curves are plotted in order of selection (columns in result).

        In addition to the listed keywords plot supports all matplotlib.pyplot.plot keyword arguments,
        like color, alpha, linewidth, linestyle, marker, ...
        ::

            sbml = te.getTestModel('feedback.xml')
            r = te.loadSBMLModel(sbml)
            s = r.simulate(0, 100, 201)
            r.plot(s, loc="upper right", linewidth=2.0, lineStyle='-', marker='o', markersize=2.0, alpha=0.8,
                   title="Feedback Oscillation", xlabel="time", ylabel="concentration", xlim=[0,100], ylim=[-1, 4])

        :param result: results data to plot
        :type result: numpy array
        :param loc: location of plot legend (standard matplotlib arguments). If loc=None or loc=False no legend is shown.
        :type loc: str or None
        :param show: show the plot, use show=False to plot multiple simulations in one plot
        :type show: bool
        :param xlabel: x-axis label
        :type xlabel: str
        :param ylabel: y-axis label
        :type ylabel: str
        :param title: plot title
        :type title: str
        :param xlim: limits on x-axis
        :type xlim: tuple [start, end]
        :param ylim: limits on y-axis
        :type ylim: tuple [start, end]
        :param xscale: 'linear' or 'log' scale for x-axis
        :type xscale: 'str'
        :param yscale: 'linear' or 'log' scale for y-axis
        :type yscale: 'str'
        :param grid: show grid
        :type grid: bool
        :param kwargs: additional matplotlib keywords like marker, lineStyle, color, alpha, ...
        :return:
        :rtype:
        """

        if result is None:
            result = self.getSimulationData()

        # Use Tellurium plotting interface
        getPlottingEngine().plotTimecourse(result, ordinates=ordinates)
        return

        # Old code:
        # if loc is False:
        #     loc = None
        #
        # if 'linewidth' not in kwargs:
        #     kwargs['linewidth'] = 2.0
        #
        # # get the names
        # names = result.dtype.names
        # if names is None:
        #     names = self.selections
        #
        # # check if set_prop_cycle is supported
        # if hasattr(plt.gca(), 'set_prop_cycle'):
        #     # reset color cycle (repeated simulations have the same colors)
        #     plt.gca().set_prop_cycle(None)
        #
        # # make plot
        # Ncol = result.shape[1]
        # if len(names) != Ncol:
        #     raise Exception('Legend names must match result array')
        # for k in range(1, Ncol):
        #     if loc is None:
        #         # no labels if no legend
        #         plt.plot(result[:, 0], result[:, k], **kwargs)
        #     else:
        #         plt.plot(result[:, 0], result[:, k], label=names[k], **kwargs)
        #
        #     cmap = plt.get_cmap('Blues')
        #
        # # labels
        # if xlabel is None:
        #     xlabel = names[0]
        # plt.xlabel(xlabel)
        # if ylabel is not None:
        #     plt.ylabel(ylabel)
        # if title is not None:
        #     plt.title(title)
        # if xlim is not None:
        #     plt.xlim(xlim)
        # if ylim is not None:
        #     plt.ylim(ylim)
        # # axis and grids
        # plt.xscale(xscale)
        # plt.yscale(yscale)
        # plt.grid(grid)
        #
        # # show legend
        # if loc is not None:
        #     plt.legend(loc=loc)
        # # show plot
        # if show:
        #     plt.show()
        # return plt

    def plotWithLegend(self, result=None, loc='upper left', show=True, **kwargs):
        warnings.warn("'plotWithLegend' is deprecated. Use 'plot' instead. Will be removed in tellurium v1.4",
                      DeprecationWarning, stacklevel=2)
        return self.plot(result=result, loc=loc, show=show, **kwargs)

    def simulateAndPlot(self, start, end, points, **kwargs):
        """ Run simulation and plot the results.

        :param start: start time of simulation
        :param end: end time of simulation
        :param points: number of points in simulation
        :returns: simulation results
        """
        warnings.warn("'simulateAndPlot' is deprecated. Use the 'simulate' followed by 'plot' instead. " +
                      "Will be removed in tellurium v1.4",
                      DeprecationWarning, stacklevel=2)
        result = self.simulate(start, end, points, **kwargs)
        self.plot(result)
        return result

    # ---------------------------------------------------------------------
    # Stochastic Simulation Methods
    # ---------------------------------------------------------------------
    def getSeed(self, integratorName="gillespie"):
        """ Current seed used by the integrator with integratorName.
        Defaults to the seed of the gillespie integrator.

        :param integratorName: name of the integrator for which the seed should be retured
        :type integratorName: str
        :returns: current seed
        :rtype: float
        """
        integrator = self.getIntegratorByName(integratorName)
        return integrator.getValue('seed')

    def setSeed(self, seed, integratorName="gillespie"):
        """ Set seed in integrator with integratorName.
        Defaults to the seed of the gillespie integrator.

        Raises Error if integrator does not have key 'seed'.

        :param seed: seed to set
        :param integratorName: name of the integrator for which the seed should be retured
        :type integratorName: str
        """
        # there are some issues converting big Python (greater than 4,294,967,295) integers
        # to C integers on 64 bit machines. If its converted to float before, works around the issue.
        self.setIntegratorSetting(integratorName=integratorName, settingName="seed", value=float(seed))

    def gillespie(self, *args, **kwargs):
        """ Run a Gillespie stochastic simulation.

        Sets the integrator to gillespie and performs simulation.
        ::

            rr = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 40')
            # Simulate from time zero to 40 time units
            result = rr.gillespie (0, 40)
            # Simulate on a grid with 10 points from start 0 to end time 40
            rr.reset()
            result = rr.gillespie (0, 40, 10)
            # Simulate from time zero to 40 time units using the given selection list
            # This means that the first column will be time and the second column species S1
            rr.reset()
            result = rr.gillespie (0, 40, selections=['time', 'S1'])
            # Simulate from time zero to 40 time units, on a grid with 20 points
            # using the give selection list
            rr.reset()
            result = rr.gillespie (0, 40, 20, ['time', 'S1'])
            rr.plot(result)

        :param seed: seed for gillespie
        :type seed: int
        :param args: parameters for simulate
        :param kwargs: parameters for simulate
        :returns: simulation results
        """
        integratorName = self.integrator.getName()
        self.setIntegrator('gillespie')
        s = self.simulate(*args, **kwargs)
        self.setIntegrator(integratorName)
        return s


# ---------------------------------------------------------------
# End of routines
# ---------------------------------------------------------------
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


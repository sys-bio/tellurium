"""
The module tellurium provides support routines.
As part of this module an ExendedRoadRunner class is defined which provides helper methods for
model export, plotting or the Jarnac compatibility layer.
"""
from __future__ import print_function, division

import os
import warnings
import roadrunner
import antimony
import matplotlib.pyplot as plt
import tephrasedml


try:
    import libsbml
except ImportError as e:
    libsbml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
    warnings.warn("'libsbml' could not be imported", ImportWarning, stacklevel=2)
try:
    import libsedml
except ImportError as e:
    libsedml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
    warnings.warn("'libsedml' could not be imported", ImportWarning, stacklevel=2)

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

# ---------------------------------------------------------------------
# plot hold
# ---------------------------------------------------------------------
# FIXME: What is this? Add some explanation of the tehold global parameter.
# why global parameter? this is really bad style.

tehold = False  # Same as matlab hold

# For some reason we can only access the tehold variable via methods
def setHold(myHold):
    global tehold    
    tehold = myHold


def getHold():
    global tehold
    return tehold


# ---------------------------------------------------------------------
# group: utility
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
    with open(os.path.join(os.path.dirname(__file__), '..', 'VERSION.txt'), 'r') as f:
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
# Loading Models Methods
# ---------------------------------------------------------------------
def _checkAntimonyReturnCode(code):
    """ Helper for checking the antimony response code.
    Raises Exception if error in antimony.

    :param code: antimony response
    :type code: int
    """
    if code < 0:
        raise Exception('Antimony: {}'.format(antimony.getLastError()))


def loada(ant):
    """ Load model from Antimony string.

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
    """ Load Antimony model with tellurium.

    See also: :func:`loada`

    :param ant: Antimony model
    :type ant: str | file
    :returns: RoadRunner instance with model loaded
    :rtype: roadrunner.RoadRunner
    """
    sbml = antimonyToSBML(ant)
    return roadrunner.RoadRunner(sbml)


def loadSBMLModel(sbml):
    """Load SBML model with tellurium

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


# ---------------------------------------------------------------------
# SEDML Utilities
# ---------------------------------------------------------------------
def experiment(ant, phrasedml):
    """ Create experiment from antimony and phrasedml string.

    :param ant: Antimony string of model
    :type ant: str
    :param phrasedml: phrasedml simulation description
    :type phrasedml: str
    :returns: SEDML experiment description
    """
    return tephrasedml.tePhrasedml(ant, phrasedml)


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
def plotArray(*args, **kwargs):
    """ Plot an array.

    The first column of the array will be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object. Note that you can add
    plotting options as named key values after the array.
    For example to add a legend, include the label key value:
    te.plotArray (m, label='A label') then use pylab.legend()
    to make sure the legend is shown.
    ::

        import numpy as np
        result = np.array([[1,2,3], [7.2,6.5,8.8], [9.8, 6.5, 4.3]])
        te.plotArray(result)
    """
    global tehold
    p = plt.plot(args[0][:, 0], args[0][:, 1:], linewidth=2.5, **kwargs)
    # If user is building a legend don't show the plot yet
    if 'label' in kwargs:
        return p
    if not tehold:
        plt.show()
    return p


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

    # def getConservedMoietyIds(self):
    #     warnings.warn('Use getDependentFloatingSpecies instead, will be removed in v1.4',
    #                   DeprecationWarning, stacklevel=2)
    #     return self.getDependentFloatingSpecies()

    # ---------------------------------------------------------------------
    # Plotting Utilities
    # ---------------------------------------------------------------------
    def draw(self, **kwargs):
        """ Draws an SBMLDiagram of the current model.
        To set the width of the output plot provide the 'width' argument.
        Species are drawn as white circles (boundary species
        shaded in blue), reactions as grey squares.
        """
        from visualization.sbmldiagram import SBMLDiagram
        diagram = SBMLDiagram(self.getSBML())
        diagram.draw(**kwargs)

    def plot(self, result=None, loc='upper right', show=True,
             xlabel=None, ylabel=None, title=None, xlim=None, ylim=None, **kwargs):
        """Plot data generated by a simulation.
        Plot results from a simulation carried out by the simulate or gillespie
        functions. This is a roadrunner method.
        Data is a numpy array where the first column is considered the x axis and all remaining columns the y axis.
        If no data is provided the data currently held by roadrunner generated in the last simulation is used.

        Curves are plotted in order of selection (columns in result)

        Supports all matplotlib.pyplot.plot keyword arguments, like
            color
            alpha
            linewidth
            linestyle
            marker
        ::

            sbml = te.getTestModel('feedback.xml')
            r = te.loadSBMLModel(sbml)
            s = r.simulate(0, 100, 201)
            r.plot(s, loc="upper right", linewidth=2.0, lineStyle='-', marker='o', markersize=2.0, alpha=0.8,
                   title="Feedback Oscillation", xlabel="time", ylabel="concentration", xlim=[0,100], ylim=[-1, 4])

        :param result: results data to plot
        :param loc: location of plot legend
        :param show: show the plot
        """
        if result is None:
            result = self.getSimulationData()

        if 'linewidth' not in kwargs:
            kwargs['linewidth'] = 2.0

        # get the names
        names = result.dtype.names
        if names is None:
            names = self.selections

        # make plot
        Ncol = result.shape[1]
        if len(names) != Ncol:
            raise Exception('Legend names must match result array')
        for k in range(1, Ncol):
            if loc is None:
                # no labels if no legend
                plt.plot(result[:, 0], result[:, k], **kwargs)
            else:
                plt.plot(result[:, 0], result[:, k], label=names[k], **kwargs)

            cmap = plt.get_cmap('Blues')

        # labels
        if xlabel is None:
            xlabel = names[0]
        plt.xlabel(xlabel)
        if ylabel is not None:
            plt.ylabel(ylabel)
        if title is not None:
            plt.title(title)
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)

        # show legend
        if loc is not None:
            plt.legend(loc=loc)
        # show plot
        if show:
            plt.show()
        return plt

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
        self.setIntegrator('gillespie')
        return self.simulate(*args, **kwargs)


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


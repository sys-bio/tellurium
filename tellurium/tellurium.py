"""
Support routines for tellurium.

A subset of methods is attached to the roadrunner instance. These are methods which extend the
roadrunner functionality. These functions have `rr` as the first argument and the format

::

    def myRoadRunnerFunction(rr, *args, **kwargs):
       '''

        :param rr: RoadRunner instance
        :type rr: RoadRunner.roadrunner

        '''
        pass

These are attached to RoadRunner at the end of the module via
::

    roadrunner.RoadRunner.myRoadRunnerFunction = myRoadRunnerFunction
"""

# ---------------------------------------------------------------------
# imports
# ---------------------------------------------------------------------
from __future__ import print_function, division

import os
import warnings
import roadrunner
import roadrunner.testing
import antimony
import matplotlib.pyplot as plt

import tecombine as combine
import tesedml
import tephrasedml

try:
    import libsbml
except ImportError as e:
    libsbml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
try:
    import libsedml
except ImportError as e:
    libsedml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))

try:
    import phrasedml
except ImportError as e:
    phrasedml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))

try:
    from sbml2matlab import sbml2matlab
except ImportError as e:
    sbml2matlab = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))

# ---------------------------------------------------------------------
# plot hold
# ---------------------------------------------------------------------
# FIXME: What is this? Add some explanation of the tehold global parameter.
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
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'VERSION.txt'), 'r') as f:
            version = f.read().rstrip()
    except IOError:
        warnings.warn("version could not be read from VERSION.txt")
        version = None
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


def _checkAntimonyReturnCode(code):
    """ Helper for checking the antimony response code.
    Raises Exception if error in antimony.

    :param code: antimony response
    :type code: int
    """
    if code < 0:
        raise Exception('Antimony: {}'.format(antimony.getLastError()))


# ---------------------------------------------------------------------
# Loading Models Methods
# ---------------------------------------------------------------------
def loada(ant):
    """ Load model from Antimony string.

    See also: :func:`loadAntimonyModel`
    ::

        r = loada('S1 -> S2; k1*S1; k1 = 0.1; S2 = 10')

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
    import warnings
    warnings.warn('Use antimonyToSBML instead, will be removed in v1.4',
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
    

class ExtendedRoadRunner(roadrunner.RoadRunner):

    def __init__(self, *args, **kwargs):
        super(ExtendedRoadRunner, self).__init__(*args, **kwargs)

        # ---------------------------------------------------------------------
        # Routines to support the Jarnac compatibility layer
        # ---------------------------------------------------------------------
        self.fjac = self.getFullJacobian
        self.sm = self.getFullStoichiometryMatrix
        self.rs = self.model.getReactionIds
        self.fs = self.model.getFloatingSpeciesIds
        self.bs = self.model.getBoundarySpeciesIds
        self.ps = self.model.getGlobalParameterIds
        self.vs = self.model.getCompartmentIds
        self.dv = self.model.getStateVectorRate
        self.rv = self.model.getReactionRates
        self.sv = self.model.getFloatingSpeciesConcentrations

    # ---------------------------------------------------------------------
    # Export Utilities
    # ---------------------------------------------------------------------
    def getCurrentAntimony(self):
        """ Antimony string of the current model state.

        :return: Antimony
        :rtype: str
        """
        return sbmlToAntimony(self.getCurrentSBML())

    def getCurrentCellML(self):
        """ CellML string of current model state.

        :returns: CellML string
        :rtype: str
        """
        return sbmlToCellML(self.getCurrentSBML())

    def getCurrentMatlab(self):
        """ Matlab string of current model state.

        :returns: Matlab string
        :rtype: str
        """
        return sbml2matlab(self.getCurrentSBML())

    def exportToSBML(self, filePath):
        """ Save current model as SBML file.

        :param filePath: file path of matlab file
        :param filePath: str
        """
        saveToFile(filePath, self.getCurrentSBML())

    def exportToAntimony(self, filePath):
        """ Save current model as Antimony file.

        :param filePath: file path of Antimony file
        :type filePath: str
        """
        saveToFile(filePath, self.getCurrentAntimony())

    def exportToCellML(self, filePath):
        """ Save current model as CellML file.

        :param filePath: file path of CellML file
        """
        saveToFile(filePath, self.getCurrentCellML())

    def exportToMatlab(self, filePath):
        """ Save current model as Matlab file.

        :param self: RoadRunner instance
        :type self: RoadRunner.roadrunner
        :param filePath: file path of Matlab file
        """
        saveToFile(filePath, self.getCurrentMatlab())

    # ---------------------------------------------------------------
    # Simulate Options
    # ---------------------------------------------------------------
    def setSteps(self, steps):
        """ Set steps in roadrunner simulateOptions.

        :param steps: steps in integration
        :type steps: int
        """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning
        self.simulateOptions.steps = steps

    def getSteps(self):
        """ Get number of steps from simulateOptions. """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning
        return self.simulateOptions.steps

    def setNumberOfPoints(self, numberOfPoints):
        """ Set number of points in roadrunner simulateOptions.

        :param numberOfPoints: number of points in result
        :type numberOfPoints: int
        """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning
        self.simulateOptions.steps = numberOfPoints - 1

    def getNumberOfPoints(self):
        """ Get number of points from rr.simulateOptions. """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning
        return self.simulateOptions.steps + 1

    def setStartTime(self, startTime):
        """ Set start in roadrunner simulateOptions.

        :param start: start time of integration
        :type start: float
        """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning("simulateOptions no longer supported")
        self.simulateOptions.start = startTime

    def getStartTime(self):
        """ Get start time from roadrunner simulateOptions. """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning("simulateOptions no longer supported")
        return self.simulateOptions.start

    def setEndTime(self, endTime):
        """ Set end in roadrunner simulateOptions.

        :param end: end time of integration
        :type end: float
        """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning("simulateOptions no longer supported")
        self.simulateOptions.end = endTime


    def getEndTime(self):
        """ Get end time from roadrunner simulateOptions. """
        warnings.warn('simulateOptions no longer supported, will be removed in v1.4',
                      DeprecationWarning, stacklevel=2)
        raise DeprecationWarning("simulateOptions no longer supported")
        return self.simulateOptions.start + self.simulateOptions.duration



def RoadRunner(*args):
    # return roadrunner.RoadRunner(*args)
    return ExtendedRoadRunner(*args)

roadrunner.RoadRunner = ExtendedRoadRunner


# ---------------------------------------------------------------------
# SEDML Utilities
# ---------------------------------------------------------------------
def experiment(antimonyStr, phrasedmlStr):
    """Create an experiment instance given an antimony string and a phrasedml string.

    :param antimonyStr: antimony string of model
    :param phrasedmlStr: phrasedml simulation description
    :returns: SEDML experiment description
    """
    return tephrasedml.tePhrasedml(antimonyStr, phrasedmlStr)


# ---------------------------------------------------------------------
# Math Utilities
# ---------------------------------------------------------------------
def getEigenvalues(m):
    """
    Eigenvalues of matrix.
    Convenience method for computing the eigenvalues of a matrix m
    Uses numpy eig to compute the eigenvalues.

    :param m: numpy array
    :returns: numpy array containing the eigenvalues
    """
    from numpy import linalg
    w, v = linalg.eig(m)
    return w

    
# ---------------------------------------------------------------------
# Stochastic Simulation Methods
# ---------------------------------------------------------------------
def getSeed(r):
    """ Current seed used by the random generator of the RoadRunner instance.
    ::

        myseed = rr.getSeed()

    :param r: RoadRunner instance.
    :returns: current seed
    """
    intg = r.getIntegrator("gillespie")
    if intg is None:
        raise ValueError("model is not loaded")
    return intg['seed']


def setSeed(r, seed):
    """Set seed for random number generator (used by gillespie for example).
    ::

        rr.setSeed(12345)

    :param r: RoadRunner instance.
    :param seed: seed to set
    """
    # FIXME: this should be via self not via a RoadRunner instance r
    intg = r.getIntegrator('gillespie')
    if intg is None:
        raise ValueError("model is not loaded")

    # there are some issues converting big Python (greater than 4,294,967,295) integers 
    # to C integers on 64 bit machines. If its converted to float before, works around the issue. 
    intg['seed'] = float(seed)


def gillespie(r, *args, **kwargs):
    """Run a Gillespie stochastic simulation.
    ::

        rr = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 40')

        # Simulate from time zero to 40 time units
        result = rr.gillespie (0, 40)

        # Simulate on a grid with 10 points from start 0 to end time 40
        result = rr.gillespie (0, 40, 10)

        # Simulate from time zero to 40 time units using the given selection list
        # This means that the first column will be time and the second column species S1
        result = rr.gillespie (0, 40, ['time', 'S1'])

        # Simulate from time zero to 40 time units, on a grid with 20 points
        # using the give selection list
        result = rr.gillespie (0, 40, 20, ['time', 'S1'])

    :param r: RoadRunner instance
    :param args: parameters for simulate
    :param kwargs: parameters for simulate
    :returns: simulation results
    """
    if r.integrator is None:
        raise ValueError("model is not loaded")
    
    prev = r.integrator.getName()

    if kwargs is not None:
        kwargs['integrator'] = 'gillespie'
    else:
        kwargs = {'integrator': 'gillespie'}

    result = r.simulate(*args, **kwargs)

    r.setIntegrator(prev)

    return result


# ---------------------------------------------------------------------
# Plotting Utilities
# ---------------------------------------------------------------------
def plot(rr, result=None, loc='upper left', show=True):
    """Plot data generated by a simulation.
    Plot results from a simulation carried out by the simulate or gillespie
    functions. This is a roadrunner method.
    Data is a numpy array where the first column is considered the x axis and all remaining columns the y axis.
    If no data is provided the data currently held by roadrunner generated in the last simulation is used.
    ::

        r.plot()

    :param rr: RoadRunner instance
    :param result: results data to plot
    :param loc: location of plot legend
    :param show: show the plot
    :returns: ?
    """
    if result is None:
        # Call Andy version if no results passed to call
        return rr.plotAS()
    else:
        return plotWithLegend(rr, result, loc, show=show)


def plotWithLegend(rr, result=None, loc='upper left', show=True):
    """Plot an array and include a legend.
    The first argument must be a roadrunner variable.
    The second argument must be an array containing data to plot.
    The first column of the array will
    be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object.
    ::

        plotWithLegend (r)

    :param rr: RoadRunner instance
    :param result: results to plot
    :param loc: location of plot legend
    :param show: show the plot
    :returns: plt object
    """
    import matplotlib.pyplot as p
    
    if not isinstance(rr, roadrunner.RoadRunner):
        raise Exception('First argument must be a roadrunner variable')

    if result is None:
        result = rr.getSimulationData()

    if result is None:
        raise Exception("no simulation result")

    if result.dtype.names is None:
        columns = result.shape[1]
        legendItems = rr.timeCourseSelections[1:]
        if columns-1 != len(legendItems):
           raise Exception('Legend list must match result array')
        for i in range(columns-1):
           plt.plot(result[:, 0], result[:, i+1], linewidth=2.5, label=legendItems[i])
    else:
        # result is structured array
        if len(result.dtype.names) < 1:
            raise Exception('no columns to plot')

        time = result.dtype.names[0]

        for name in result.dtype.names[1:]:
            p.plot(result[time], result[name], label=name)

    plt.legend(loc=loc)

    if show:
        plt.show()
    return plt


def simulateAndPlot(rr, startTime=0, endTime=5, numberOfPoints=500, **kwargs):
    """Run simulation and plot the results.
    ::

        simulateAndPlot (rr)
        simulateAndPlot (rr, 0, 10, 100)

    :param rr: RoadRunner instance
    :param startTime: start time of simulation
    :param endTime: end time of simulation
    :param numberOfPoints: number of points in simulation
    :returns: simulation results
    """
    # FIXME: arguments should have the same names like the named arguments in simulate (start, end, ...)
    result = rr.simulate(startTime, endTime, numberOfPoints, **kwargs)
    plotWithLegend(rr, result)
    return result
 

def plotArray(*args, **kwargs):
    """ Plot an array.
    The first column of the array will
    be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object. Note that you can add
    plotting options as named key values after the array. For
    example to add a legend, include the label key value:
    te.plotArray (m, label='A label') then use pylab.legend()
    to make sure the legend is shown. 
    ::

        result = numpy.array([[1,2,3], [7.2,6.5,8.8], [9.8, 6.5, 4.3]])
        plotArray(result)
    """
    global tehold 
    p = plt.plot(args[0][:, 0], args[0][:, 1:], linewidth=2.5, **kwargs)
    # If user is building a legend don't show the plot yet    
    if 'label' in kwargs:
        return p
    if tehold == False:    
        plt.show()
    return p

# ---------------------------------------------------------------------
# Test Models
# ---------------------------------------------------------------------
def loadTestModel(string):
    """Loads particular test model into roadrunner.
    ::

        rr = roadrunner.loadTestModel('feedback.xml')

    :returns: RoadRunner instance with test model loaded
    """
    return roadrunner.testing.getRoadRunner(string)


def getTestModel(string):
    """SBML of given test model as a string.
    ::

        # load test model as SBML
        sbml = te.getTestModel('feedback.xml')
        rr = te.loadSBMLModel(sbml)
        # simulate
        s = rr.simulate(0, 100, 200)

    :returns: SBML string of test model
    """
    return roadrunner.testing.getData(string)


def listTestModels():
    """ List roadrunner SBML test models.
    ::

        print(roadrunner.listTestModels())

    :returns: list of test model paths
    """
    modelList = []
    fileList = roadrunner.testing.dir('*.xml')
    for pathName in fileList:
        modelList.append(os.path.basename(pathName))
    return modelList


# ---------------------------------------------------------------------
# Test Models
# ---------------------------------------------------------------------
def resetToOrigin(rr):
    """Reset model to state when first loaded.
    This resets the model back to the state when it was FIRST loaded,
    this includes all init() and parameters such as k1 etc.
    ::

        r.resetToOrigin()

    identical to:
        r.reset(roadrunner.SelectionRecord.ALL)
    """
    rr.reset(roadrunner.SelectionRecord.ALL)


def resetAll(rr):
    """Reset all model variables to CURRENT init(X) values.
    This resets all variables, S1, S2 etc to the CURRENT init(X) values. It also resets all
    parameters back to the values they had when the model was first loaded.
    ::

        rr.resetAll()
    """
    rr.reset(roadrunner.SelectionRecord.TIME |
             roadrunner.SelectionRecord.RATE |
             roadrunner.SelectionRecord.FLOATING |
             roadrunner.SelectionRecord.GLOBAL_PARAMETER)

# --------------------------------------------------------------------- 
# Routines flattened from model, aves typing and easier finding of methods
# ---------------------------------------------------------------------
def getRatesOfChange(rr):
    """ Rate of change of all state variables in the model.

    :returns: rate of change of all state variables (eg species) in the model.
    """
    if rr.conservedMoietyAnalysis:
        m1 = rr.getLinkMatrix()
        m2 = rr.model.getStateVectorRate()
        return m1.dot(m2)
    else:
        return rr.model.getStateVectorRate()


def getConservedMoietyIds(self):
    warnings.warn('Use getDependentFloatingSpecies instead, will be removed in v1.4',
                  DeprecationWarning, stacklevel=2)
    return self.getDependentFloatingSpecies()


# ---------------------------------------------------------------
# End of routines
# Now we assign the routines to the roadrunner instance
# ---------------------------------------------------------------
# FIXME: handle in more general way via the names.

"""
roadrunner.RoadRunner.getCurrentMatlab = getCurrentMatlab
roadrunner.RoadRunner.getCurrentAntimony = getCurrentAntimony
roadrunner.RoadRunner.getCurrentCellML = getCurrentCellML
roadrunner.RoadRunner.exportToMatlab = exportToMatlab
roadrunner.RoadRunner.exportToAntimony = exportToAntimony
roadrunner.RoadRunner.exportToSBML = exportToSBML
roadrunner.RoadRunner.exportToCellML = exportToCellML
"""

# Helper Routines
roadrunner.RoadRunner.getSeed = getSeed
roadrunner.RoadRunner.setSeed = setSeed
roadrunner.RoadRunner.gillespie = gillespie
roadrunner.RoadRunner.getRatesOfChange = getRatesOfChange

roadrunner.RoadRunner.plotAS = roadrunner.RoadRunner.plot
roadrunner.RoadRunner.plot = plot

roadrunner.noticesOff = noticesOff
roadrunner.noticesOn = noticesOn  
roadrunner.getTestModel = getTestModel
roadrunner.loadTestModel = loadTestModel
roadrunner.listTestModels = listTestModels

roadrunner.RoadRunner.resetToOrigin = resetToOrigin
roadrunner.RoadRunner.resetAll = resetAll

roadrunner.RoadRunner.getConservedMoietyIds = getConservedMoietyIds

# -------------------------------------------------------
# SimulateOptions
"""
roadrunner.RoadRunner.setStartTime = setStartTime
roadrunner.RoadRunner.getStartTime = getStartTime
roadrunner.RoadRunner.setEndTime = setEndTime
roadrunner.RoadRunner.getEndTime = getEndTime
roadrunner.RoadRunner.setNumberOfPoints = setNumberOfPoints
roadrunner.RoadRunner.getNumberOfPoints = getNumberOfPoints
roadrunner.RoadRunner.setSteps = setSteps
roadrunner.RoadRunner.getSteps = getSteps
"""

# ---------------------------------------------------------------------
# Routines to support the Jarnac compatibility layer
# ---------------------------------------------------------------------
#
# def getRs(rr):
#     """ Returns the list of reaction Identifiers.
#
#     See also: :func:`rs`, :func:`getReactionIds`
#
#     :returns: reaction identifiers
#     """
#     return rr.model.getReactionIds()
#
#
# def getFs(rr):
#     """ Returns list of floating species identifiers.
#
#     See also: :func:`fs`, :func:`getFloatingSpeciesIds`
#
#     :returns: floating species identifiers
#     """
#     return rr.model.getFloatingSpeciesIds()
#
#
# def getBs(rr):
#     """ Returns list of boundary species identifiers.
#
#     See also: :func:`bs`, :func:`getBoundarySpeciesIds`
#
#     :returns: boundary species identifiers
#     """
#     return rr.model.getBoundarySpeciesIds()
#
#
# def getPs(rr):
#     """ Returns list of global parameters in the model.
#
#     See also: :func:`ps`, :func:`getGlobalParameterIds`
#
#     :returns: global parameters
#     """
#     return rr.model.getGlobalParameterIds()
#
#
# def getVs(rr):
#     """ Returns the list of compartment identifiers.
#
#     See also: :func:`vs`, :func:`getCompartmentIds`
#
#     :returns: compartment identifiers
#     """
#     return rr.model.getCompartmentIds()
#
#
# def getDv(rr):
#     """ Returns the list of rates of change.
#
#     See also: :func:`dv`, :func:`getStateVectorRate`
#
#     :returns: rate of change
#     """
#     return rr.model.getStateVectorRate()
#
#
# def getRv(rr):
#     """ Returns the list of reaction rates.
#
#     See also: :func:`rv`, :func:`getReactionRates`
#
#     :returns: reaction rates
#     """
#     return rr.model.getReactionRates()
#
#
# def getSv(rr):
#     """ Returns the list of floating species concentrations.
#
#     See also: :func:`rr`, :func:`getFloatingSpeciesConcentrations`
#
#     :returns: floating species concentrations
#     """
#     return rr.model.getFloatingSpeciesConcentrations()
#
#
#
# # WORK IN PROGRESS - DO NOT REMOVE
# # Jarnac compatibility layer
# jarnac_layer = {
#     'fjac': roadrunner.RoadRunner.getFullJacobian,
#     'sm': roadrunner.RoadRunner.getFullStoichiometryMatrix,
#     'rs': roadrunner.ExecutableModel.getReactionIds,
#     'fs': roadrunner.ExecutableModel.getFloatingSpeciesIds,
#     'bs': roadrunner.ExecutableModel.getBoundarySpeciesIds,
#     'ps': roadrunner.ExecutableModel.getGlobalParameterIds,
#     'vs': roadrunner.ExecutableModel.getCompartmentIds,
#     'dv': roadrunner.ExecutableModel.getStateVectorRate,
#     'rv': roadrunner.ExecutableModel.getReactionRates,
#     'sv': roadrunner.ExecutableModel.getFloatingSpeciesConcentrations,
# }
# for key, value in jarnac_layer.iteritems():
#     setattr(roadrunner.RoadRunner, key, value)
#
#
# roadrunner.RoadRunner.fjac = roadrunner.RoadRunner.getFullJacobian
# roadrunner.RoadRunner.sm = roadrunner.RoadRunner.getFullStoichiometryMatrix
# roadrunner.RoadRunner.fs = getFs
# roadrunner.RoadRunner.bs = getBs
# roadrunner.RoadRunner.rs = getRs
# roadrunner.RoadRunner.ps = getPs
# roadrunner.RoadRunner.vs = getVs
# roadrunner.RoadRunner.dv = getDv
# roadrunner.RoadRunner.rv = getRv
# roadrunner.RoadRunner.sv = getSv
#

# -------------------------------------------------------
# Model flattening routines
# TODO: handle the pass trough docstrings
# FIXME: by the following trick all the documentation gets lost!
# i.e. the te.func() do not have any documentation associated.
# make sure help(func) returns the info of help(self.model.func) (see wrap in functools)

def getBoundarySpeciesConcentrations(rr):
    return rr.model.getBoundarySpeciesConcentrations()

def getBoundarySpeciesIds(rr):
    return rr.model.getBoundarySpeciesIds()

def getNumBoundarySpecies(rr):
    return rr.model.getNumBoundarySpecies()

def getFloatingSpeciesConcentrations(self):
    return self.model.getFloatingSpeciesConcentrations()

def getFloatingSpeciesIds(rr):
    return rr.model.getFloatingSpeciesIds()

def getNumFloatingSpecies(rr):
    return rr.model.getNumFloatingSpecies()

def getGlobalParameterIds(rr):
    return rr.model.getGlobalParameterIds()

def getGlobalParameterValues(rr):
    return rr.model.getGlobalParameterValues()

def getNumGlobalParameters(rr):
    return rr.model.getNumGlobalParameters()

def getCompartmentIds(rr):
    return rr.model.getCompartmentIds()

def getCompartmentVolumes(rr):
    return rr.model.getCompartmentVolumes()

def getNumCompartments(rr):
    return rr.model.getNumCompartments()

def getConservedMoietyValues(rr):
    return rr.model.getConservedMoietyValues()

def getNumConservedMoieties(rr):
    return rr.model.getNumConservedMoieties()

def getNumDepFloatingSpecies(rr):
    return rr.model.getNumDepFloatingSpecies()

def getNumIndFloatingSpecies(rr):
    return rr.model.getNumIndFloatingSpecies()

def getNumReactions(rr):
    return rr.model.getNumReactions()

def getReactionIds(rr):
    return rr.model.getReactionIds()

def getReactionRates(rr):
    return rr.model.getReactionRates()

def getNumEvents(rr):
    return rr.model.getNumEvents()

def getNumRateRules(rr):
    return rr.model.getNumRateRules()

roadrunner.RoadRunner.getBoundarySpeciesConcentrations = getBoundarySpeciesConcentrations
roadrunner.RoadRunner.getBoundarySpeciesIds = getBoundarySpeciesIds
roadrunner.RoadRunner.getNumBoundarySpecies = getNumBoundarySpecies

roadrunner.RoadRunner.getFloatingSpeciesConcentrations = getFloatingSpeciesConcentrations
roadrunner.RoadRunner.getFloatingSpeciesIds = getFloatingSpeciesIds
roadrunner.RoadRunner.getNumFloatingSpecies = getNumFloatingSpecies

roadrunner.RoadRunner.getGlobalParameterIds = getGlobalParameterIds
roadrunner.RoadRunner.getGlobalParameterValues = getGlobalParameterValues
roadrunner.RoadRunner.getNumGlobalParameters = getNumGlobalParameters

roadrunner.RoadRunner.getCompartmentIds = getCompartmentIds
roadrunner.RoadRunner.getCompartmentVolumes = getCompartmentVolumes
roadrunner.RoadRunner.getNumCompartments = getNumCompartments


roadrunner.RoadRunner.getNumConservedMoieties = getNumConservedMoieties
roadrunner.RoadRunner.getNumConservedMoieties = getNumConservedMoieties
roadrunner.RoadRunner.getNumConservedMoieties = getNumConservedMoieties

roadrunner.RoadRunner.getNumReactions = getNumReactions
roadrunner.RoadRunner.getReactionIds = getReactionIds
roadrunner.RoadRunner.getReactionRates = getReactionRates
roadrunner.RoadRunner.getNumEvents = getNumEvents
roadrunner.RoadRunner.getNumRateRules = getNumRateRules
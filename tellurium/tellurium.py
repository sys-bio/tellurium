##@Module Tellurium

# -*- coding: utf-8 -*-
"""
Support routines for tellurium

@author: Herbert M Sauro
"""
# FIXME: many functions are called with self as first argument (but are no methods)
# -> should be named r (RoadRunner instance)

from __future__ import print_function, division

import os
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
    """Returns version information for tellurium included packages.

    :returns: list of tuples (package, version)
    """
    # FIXME: method name not reflecting function (get vs. print)
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
        import os
        f = open(os.path.join(os.path.dirname(__file__), 'VERSION.txt'), 'r')
        version = f.read().rstrip()
        f.close()
    except IOError:
        # FIXME: the version should be encoded in exactly one place (hard coding is bad hack)
        version = "1.3.0"
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
    f = open(filePath, 'w')
    f.write(str)
    f.close()


def readFromFile(filePath):
    """ Load a file and return contents as a string.

    see also: :func:`saveToFile`

    :param filePath: file path to read from
    :returns: string representation of the contents of the file
    """
    f = open(filePath, 'r')
    return f.read()


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
    """Current seed used by the random generator of the RoadRunner instance.
    ::

        myseed = rr.getSeed()

    :param r: RoadRunner instance.
    :returns: current seed
    """
    # FIXME: this should be via self not via a RoadRunner instance r
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


def RoadRunner(*args):
    return roadrunner.RoadRunner(*args)


# ---------------------------------------------------------------------
# Plotting Utilities
# ---------------------------------------------------------------------
def plotWithLegend(r, result=None, loc='upper left', show=True):
    """Plot an array and include a legend.
    The first argument must be a roadrunner variable.
    The second argument must be an array containing data to plot.
    The first column of the array will
    be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object.
    ::

        plotWithLegend (r)

    :param r: RoadRunner instance
    :param result: results to plot
    :param loc: location of plot legend
    :param show: show the plot
    :returns: plt object
    """
    import matplotlib.pyplot as p
    
    if not isinstance(r, roadrunner.RoadRunner):
        raise Exception('First argument must be a roadrunner variable')

    if result is None:
        result = r.getSimulationData()

    if result is None:
        raise Exception("no simulation result")

    if result.dtype.names is None:
        columns = result.shape[1]
        legendItems = r.timeCourseSelections[1:]
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


def simulateAndPlot(r, startTime=0, endTime=5, numberOfPoints=500, **kwargs):
    """Run simulation and plot the results.
    ::

        simulateAndPlot (rr)
        simulateAndPlot (rr, 0, 10, 100)

    :param r: RoadRunner instance
    :param startTime: start time of simulation
    :param endTime: end time of simulation
    :param numberOfPoints: number of points in simulation
    :returns: simulation results
    """
    # FIXME: arguments should have the same names like the named arguments in simulate (start, end, ...)
    result = r.simulate(startTime, endTime, numberOfPoints, **kwargs)
    plotWithLegend(r, result)
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


def plot(self, result=None, loc='upper left', show=True):
    """Plot data generated by a simulation.
    Plot results from a simulation carried out by the simulate or gillespie
    functions. This is a roadrunner method.
    Data is a numpy array where the first column is considered the x axis and all remaining columns the y axis.
    If no data is provided the data currently held by roadrunner generated in the last simulation is used.
    ::

        r.plot()

    :param self: RoadRunner instance
    :param result: results data to plot
    :param loc: location of plot legend
    :param show: show the plot
    :returns: ?
    """
    if result is None:
        # Call Andy version if no results passed to call
        return self.plotAS()
    else:
        return plotWithLegend(self, result, loc, show=show)


# ---------------------------------------------------------------------
# Export Utilities
# ---------------------------------------------------------------------
def getMatlab(self):
    """Matlab string of current model.

    :returns: Matlab string
    """
    return sbml2matlab(self.getCurrentSBML())


def exportToMatlab(self, fileName):
    """Save current model as Matlab file.
    ::

        rr.exportToMatlab ('mymodel.m')

    :param fileName: file path of matlab file
    :returns: ?
    """
    saveToFile(fileName, self.getMatlab())


def getAntimony(self):
    """Antimony string of the current model state.
    ::

        print(rr.getAntimony())

    :returns: antimony string
    """
    return sbmlToAntimony(self.getCurrentSBML())


# ---------------------------------------------------------------------
# Test Models
# ---------------------------------------------------------------------
def loadTestModel (str):
    """Loads particular test model into roadrunner.
    ::

        rr = roadrunner.loadTestModel('feedback.xml')

    :returns: RoadRunner instance with test model loaded
    """
    return roadrunner.testing.getRoadRunner(str)


def getTestModel(str):
    """SBML of given test model as a string.
    ::

        # load test model as SBML
        sbml = te.getTestModel('feedback.xml')
        rr = te.loadSBMLModel(sbml)
        # simulate
        s = rr.simulate(0, 100, 200)

    :returns: SBML string of test model
    """
    return roadrunner.testing.getData(str)


def listTestModels():
    """List roadrunner SBML test models.
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
def resetToOrigin(self):
    """Reset model to state when first loaded.
    This resets the model back to the state when it was FIRST loaded,
    this includes all init() and parameters such as k1 etc.
    ::

        te.resetToOrigin()

    identical to:
        te.reset(roadrunner.SelectionRecord.ALL)
    """
    self.reset(roadrunner.SelectionRecord.ALL)


def resetAll(self):
    """Reset all model variables to CURRENT init(X) values.
    This resets all variables, S1, S2 etc to the CURRENT init(X) values. It also resets all
    parameters back to the values they had when the model was first loaded.
    ::

        rr.resetAll()
    """
    self.reset(roadrunner.SelectionRecord.TIME |
               roadrunner.SelectionRecord.RATE |
               roadrunner.SelectionRecord.FLOATING |
               roadrunner.SelectionRecord.GLOBAL_PARAMETER)


# --------------------------------------------------------------------- 
# Routines to support the Jarnac compatibility layer
# ---------------------------------------------------------------------
def getSm(self):
    """Returns the full reordered stoichiometry matrix.
    Short-cut sm, e.g.
    ::

        print(rr.sm())

    :returns: full reordered stoichiometry matrix
    """
    return self.getFullStoichiometryMatrix()


def getRs(self):
    """Returns the list of reaction Identifiers.
    Short-cut rs, e.g.
    ::

        print(rr.rs())

    :returns: reaction identifiers
    """
    return self.model.getReactionIds()


def getFs(self):
    """Returns list of floating species identifiers.
    Short-cut fs, e.g.
    ::

        print(rr.fs())

    :returns: floating species identifiers
    """
    return self.model.getFloatingSpeciesIds()


def getBs(self):
    """Returns list of boundary species identifiers.
    Short-cut bs, e.g.
    ::

        print(rr.bs())

    :returns: boundary species identifiers
    """
    return self.model.getBoundarySpeciesIds()


def getPs(self):
    """Returns list of global parameters in the model.
    Short-cut ps, e.g.
    ::
    
        print(rr.ps())

    :returns: global parameters
    """
    return self.model.getGlobalParameterIds()


def getVs(self):
    """  
    Returns the list of compartment identifiers.
    Short-cut vs, e.g.
    ::

        print(rr.vs())

    :returns: compartment identifiers
    """
    return self.model.getCompartmentIds()


def getDv(self):
    """Returns the list of rates of change.
    Short-cut dv, e.g.
    ::

        print(rr.dv())

    :returns: rate of change
    """
    return self.model.getStateVectorRate()


def getRv(self):
    """  Returns the list of reaction rates.
    Short-cut rv, e.g.
    ::

        print(rr.rv())

    :returns: reaction rates
    """
    return self.model.getReactionRates()


def getSv(self):
    """Returns the list of floating species concentrations.
    Short-cut sv, e.g.
    ::

        print(rr.sv())

    :returns: floating species concentrations
    """
    return self.model.getFloatingSpeciesConcentrations()


def getfJac(self):
    """Returns the full Jacobian for the current model at the current state.
    Short-cut fjac, e.g.
    ::

        print(rr.fjac())

    :returns: Jacobian at current state
    """
    return self.getFullJacobian()


# --------------------------------------------------------------------- 
# Routines flattened from model, aves typing and easier finding of methods
# ---------------------------------------------------------------------
def getRatesOfChange(self):
    """Rate of change of all state variables in the model.

    :returns: rate of change of all state variables (eg species) in the model.
    """
    if self.conservedMoietyAnalysis:
        m1 = self.getLinkMatrix()
        m2 = self.model.getStateVectorRate()
        return m1.dot(m2)
    else:
        return self.model.getStateVectorRate()


# FIXME: by the following trick all the documentation gets lost!
# i.e. the te.func() do not have any documentation associated.
# make sure help(func) returns the info of help(self.model.func) (see wrap in functools)

def getBoundarySpeciesConcentrations(self):
    return self.model.getBoundarySpeciesConcentrations()

def getBoundarySpeciesIds(self):
    return self.model.getBoundarySpeciesIds()
    
def getNumBoundarySpecies(self):
    return self.model.getNumBoundarySpecies()

def getFloatingSpeciesConcentrations(self):
    return self.model.getFloatingSpeciesConcentrations ()
    
def getFloatingSpeciesIds(self):
    return self.model.getFloatingSpeciesIds()
    
def getNumFloatingSpecies(self):
    return self.model.getNumFloatingSpecies()
    
def getGlobalParameterIds(self):
    return self.model.getGlobalParameterIds()
    
def getGlobalParameterValues(self):
    return self.model.getGlobalParameterValues() 
    
def getNumGlobalParameters(self):
    return self.model.getNumGlobalParameters() 

def getCompartmentIds(self):
    return self.model.getCompartmentIds()
        
def getCompartmentVolumes(self):
    return self.model.getCompartmentVolumes()
        
def getNumCompartments(self):
    return self.model.getNumCompartments()

def getConservedMoietyIds(self):
    raise RuntimeError('getConservedMoietyIds deprecated; Use r.getDependentFloatingSpecies')
    return self.model.getConservedMoietyIds()
            
def getConservedMoietyValues(self):
    return self.model.getConservedMoietyValues()
            
def getNumConservedMoieties(self):
    return self.model.getNumConservedMoieties()
            
def getNumDepFloatingSpecies(self):
    return self.model.getNumDepFloatingSpecies()
            
def getNumIndFloatingSpecies(self):
    return self.model.getNumIndFloatingSpecies()

def getNumReactions(self):
    return self.model.getNumReactions()
    
def getReactionIds(self):
    return self.model.getReactionIds()
    
def getReactionRates(self):
    return self.model.getReactionRates()
    
def getNumEvents(self):
    return self.model.getNumEvents()
 
#def getValue (self, name):
#    return self.model.getalue (name)
    
#def setValue (self, name, value):
#    self.model.setvalue (name, value)
    
def setStartTime(self, startTime):
    self.model.setTime(startTime)
   
def setEndTime(self, endTime):
    self.simulateOptions.end = endTime

def getStartTime(self):
    return self.simulateOptions.start
    
def getEndTime(self):
    return self.simulateOptions.start + self.simulateOptions.duration

def getNumberOfPoints(self):
    return self.simulateOptions.steps + 1
    
def setNumberOfPoints(self, numberOfPoints):
    self.simulateOptions.steps = numberOfPoints - 1

def getNumRateRules(self):
    return self.model.getNumRateRules()


# ---------------------------------------------------------------
# End of routines
# Now we assign the routines to the roadrunner instance
# ---------------------------------------------------------------
    
# Helper Routines we attach to roadrunner   
roadrunner.RoadRunner.getSeed = getSeed
roadrunner.RoadRunner.setSeed = setSeed
roadrunner.RoadRunner.gillespie = gillespie
roadrunner.RoadRunner.getRatesOfChange = getRatesOfChange
roadrunner.RoadRunner.exportToMatlab = exportToMatlab
roadrunner.RoadRunner.getMatlab = getMatlab
roadrunner.RoadRunner.getAntimony = getAntimony
roadrunner.RoadRunner.plotAS = roadrunner.RoadRunner.plot
roadrunner.RoadRunner.plot = plot

roadrunner.noticesOff = noticesOff
roadrunner.noticesOn = noticesOn  
roadrunner.getTestModel = getTestModel
roadrunner.loadTestModel = loadTestModel
roadrunner.listTestModels = listTestModels

roadrunner.RoadRunner.resetToOrigin = resetToOrigin
roadrunner.RoadRunner.resetAll = resetAll

# -------------------------------------------------------
# Model flattening routines
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

roadrunner.RoadRunner.getConservedMoietyIds = getConservedMoietyIds
roadrunner.RoadRunner.getNumConservedMoieties = getNumConservedMoieties
roadrunner.RoadRunner.getNumConservedMoieties = getNumConservedMoieties
roadrunner.RoadRunner.getNumConservedMoieties = getNumConservedMoieties

roadrunner.RoadRunner.getNumReactions = getNumReactions
roadrunner.RoadRunner.getReactionIds = getReactionIds
roadrunner.RoadRunner.getReactionRates = getReactionRates
roadrunner.RoadRunner.getNumEvents = getNumEvents

#roadrunner.RoadRunner.getValue = getValue
#roadrunner.RoadRunner.setValue = setValue
roadrunner.RoadRunner.setStartTime = setStartTime
roadrunner.RoadRunner.setEndTime = setEndTime
roadrunner.RoadRunner.getStartTime = getStartTime
roadrunner.RoadRunner.getEndTime = getEndTime
roadrunner.RoadRunner.getNumberOfPoints = getNumberOfPoints
roadrunner.RoadRunner.setNumberOfPoints = setNumberOfPoints
roadrunner.RoadRunner.getNumRateRules = getNumRateRules

# -------------------------------------------------------
# Jarnac compatibility layer
roadrunner.RoadRunner.sm = getSm
roadrunner.RoadRunner.fs = getFs
roadrunner.RoadRunner.bs = getBs
roadrunner.RoadRunner.rs = getRs
roadrunner.RoadRunner.ps = getPs
roadrunner.RoadRunner.vs = getVs
roadrunner.RoadRunner.fjac = getfJac

roadrunner.RoadRunner.dv = getDv
roadrunner.RoadRunner.rv = getRv
roadrunner.RoadRunner.sv = getSv

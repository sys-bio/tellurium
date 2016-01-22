##@Module Tellurium

# -*- coding: utf-8 -*-
"""
Support routines for tellurium

@author: Herbert M Sauro
"""
# FIXME: many functions are called with self as first argument (but are no methods)
# -> should be named r (RoadRunner instance)

from __future__ import print_function, division

import matplotlib.pyplot as plt
import roadrunner
import roadrunner.testing
import antimony
import tellurium
import os


try:
    import tecombine as combine
except ImportError as e:
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
try:
    import SedmlToRr
except ImportError as e:
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))    
try:
    import tephrasedml
except ImportError as e:
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
try:
    from sbml2matlab import sbml2matlab
except ImportError as e:
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
    """
    Prints version information for tellurium supported packages.

    :returns: None
    """
    # FIXME: method name not reflecting function (get vs. print)
    print("tellurium: ", getTelluriumVersion())
    print("roadrunner:", roadrunner.__version__)
    print("antimony:", antimony.__version__)
    print("snbw_viewer: No information for sbnw viewer")
    

##\brief Returns version number of tellurium
#
#\return Returns a string representing the version number
def getTelluriumVersion():
    """
    Version number of tellurium.
    :returns: version string
    """
    try:
        import os
        f = open(os.path.join(os.path.dirname(__file__), 'VERSION.txt'), 'r')
        ver = f.read().rstrip()
        f.close()
    except IOError:
        # FIXME: the version should be encoded in exactly one place (bad hack)
        ver = "1.3.0"
    return ver

__version__ = getTelluriumVersion()


##\brief Turn off warning messages. 
# Call this to stop roadrunner from printing warning message to the console
def noticesOff():
    """
    Switch off the generation of notices to the user.
    Call this to stop roadrunner from printing warning message to the console.
    """
    roadrunner.Logger.setLevel(roadrunner.Logger.LOG_WARNING)


##\brief Turn on warning messages. 
# Call this to enable roadrunner to print warning messages to the console
def noticesOn():
    """
    Switch on notice generation to the user.
    """
    roadrunner.Logger.setLevel(roadrunner.Logger.LOG_NOTICE)
    
##@}
 
  
# ---------------------------------------------------------------------
##\ingroup filefunctions
#@{

##\brief Save a string to a file
#
#Example: saveToFile ('c:\\myfile.txt', strVariable)
#
#\param[in] fileName The current time in the simulation
#\param[in] str The step size to use in the integration
#\return Saves a string to a file
def saveToFile(fileName, str):
    """
    Save string to a file.

    saveToFile ('c:\\myfile.txt', strVariable)

    :param fileName: file path to save to
    :param str: string to save
    :returns None
    """
    f = open(fileName, 'w')
    f.write(str)
    f.close()

##\brief Reads a text file into a string
#
#Example: str = readFromFile ('c:\\myfile.txt')
#
#\param[in] fileName The current time in the simulation
#\return Returns a string representing the contents of the text file
def readFromFile (fileName):
    """
    Load a file and return contents as a string.

    str = readFromFile ('c:\\myfile.txt')

    :param fileName: file path to read from
    :returns string representation of the contents of the file
    """
    f = open(fileName, 'r')
    return f.read()
##@} 


# ---------------------------------------------------------------------   
##\ingroup loadingModels
#@{

##\brief Load an SBML model into roadRunner
#
#Example: rr = loadSBMLModel ('c:\\myfile.txt')
#
#\param[in] sbml A filename or a string containing SBML
#\return Returns a reference to the roadrunner model
def loadSBMLModel(sbml):
    """
    Load an SBML model into roadRunner.

    :param sbml: SBML filename, SBML string or SBML uri
    :returns reference to roadrunner model
    """
    rr = roadrunner.RoadRunner(sbml)
    return rr


##\brief Reads an Antimony string into roadrunner
#
#Example: rr = loadAntimonyModel (modelStr)
#
#\param[in] antStr A string containing a Antimony model
#\return Returns a reference to the roadrunner model
def loadAntimonyModel(antStr):
    """
    Load model from antimony string.
    
    r = loadAntModel(antimonyStr)

    :param antStr antimony string
    :returns reference to roadrunner model
    """
    err = antimony.loadAntimonyString(antStr)
 
    if err < 0:
        raise Exception('Antimony: ' + antimony.getLastError())
       
    mid = antimony.getMainModuleName()
    sbmlStr = antimony.getSBMLString(mid)
    rr = roadrunner.RoadRunner(sbmlStr)
    
    antimony.clearPreviousLoads()
    
    return rr


##\brief Reads an Antimony string into roadrunner, short-cut to loadAntimonyModel()
#
#Example: rr = loada ('S1 -> S2; k1*S1; k1 = 0.1; S2 = 10')
#
#\param[in] antStr A string containing a Antimony model
#\return Returns reference to the roadrunner model
def loada (antStr):
    """
    Load model from antimony string.

    r = loadAntModel(antimonyStr)

    :param antStr: antimony string
    :returns reference to roadrunner model
    """
    return loadAntimonyModel(antStr)


##\brief Reads a CellML string into roadrunner
#\return Returns a reference to the roadrunner model  
def loadCellMLModel(cellML):
    """
    Load a cellml model into roadrunner.

    r = loadCellMLModel ('mymodel.cellml')

    :param cellML: model to load, can be file or string
    :returns reference to roadrunner model
    """
    import os
    if os.path.isfile(cellML):
        sbmlstr = cellmlFileToSBML(cellML)
    else:
        sbmlstr = cellmlStrToSBML(cellML)
    return roadrunner.RoadRunner(sbmlstr)
##@}
 
# ---------------------------------------------------------------------
##\ingroup interconversion
#@{


##\brief Converts an Antimony model into SBML
#\return Returns the SBML model as a string
def antimonyTosbml(antStr):
    """Convert antimony string to SBML string.

    sbmlStr = antimonyTosbml(antimonyStr)

    :param antStr: antimony string of model
    :returns: SBML model as string

    """
    err = antimony.loadAntimonyString(antStr)
    if err < 0:
        raise Exception('Antimony: ' + antimony.getLastError())

    mid = antimony.getMainModuleName()
    return antimony.getSBMLString(mid)


##\brief Converts a SBML model to Antimony
#\return Returns the Antimony model as a string
def sbmlToAntimony(str):
    """
    Convert SBML string to antimony string.

    sbmlStr = sbmlToAntimony(antimonyStr)

    :param str: SBML model as string
    :returns antimony string of model
    """
    err = antimony.loadSBMLString(str)
    if err < 0:
        raise Exception('Antimony: ' + antimony.getLastError())

    return antimony.getAntimonyString(None)


def cellmlFileToAntimony(CellMLFileName):
    """
    Convert cellml file to antimony string.
    
    ant = cellMLToAntimony('mymodel.cellml')

    :param CellMLFileName: CellML file
    :returns antimony string of model
    """
    if antimony.loadCellMLFile(CellMLFileName) == -1:
        raise Exception('Error calling loadCellMLFile')
    antimony.loadCellMLFile(CellMLFileName)
    return antimony.getAntimonyString(None)
 
    
def cellmlFileToSBML(CellMLFileName):
    """
    Convert cellml file to SBML string.
    
    sbmlStr = cellMLToSBML('mymodel.cellml')

    :param CellMLFileName: CellML file
    :returns SBML string of model
    """
    if antimony.loadCellMLFile(CellMLFileName) < 0:
        raise Exception('Error calling loadCellMLFile' + antimony.getLastError())
    return antimony.getSBMLString(None)


def cellmlStrToAntimony(CellMLStr):
    """
    Convert cellml string to antimony string:
    
    ant = cellMLStrToAntimony('mymodel.cellml')

    :param CellMLStr: CellML string
    :returns antimony string of model
    """
    if antimony.loadCellMLFile(CellMLStr) < 0:
        raise Exception('Error calling cellMLStrToAntimony' + antimony.getLastError())
    return antimony.getAntimonyString(None)
    
    
def cellmlStrToSBML (CellMLStr):
    """
    Convert cellml string to SBML string.
    
    sbmlStr = cellMLStrToSBML('mymodel.cellml')

    :param CellMLStr: CellML string
    :returns antimony string of model
    """
    if antimony.loadCellMLFile(CellMLStr) < 0:
        raise Exception('Error calling cellMLStrToSBML' + antimony.getLastError())
    return antimony.getSBMLString(None)
##@}

# ---------------------------------------------------------------------
##\ingroup phrasedmlSupport
#@{
 
##\brief Links a PhrasedML string with an antimony model
#
#\return Returns an experiment instance
def experiment(antimonyStr, phrasedmlStr):
    """
    Create an experiment instance given an antimony string and a phrasedml string.

    :param antimonyStr: antimony string of model
    :param antimonyStr: phrasedml simulation description
    :returns SEDML experiment description
    """
    return tephrasedml.tePhrasedml(antimonyStr, phrasedmlStr)

##@} 

# ---------------------------------------------------------------------
##\ingroup math
#@{


##\brief Compute the eigenvalues for numpy array
#
#Example: mat = rr.getEigenvalues(matrix)
#
#\param[in] m numpy array
#\return Returns a numpy array containing the eigenvalues
def getEigenvalues(m):
    """
    Eigenvalues of matrix.
    Convenience method for computing the eigenvalues of a matrix m
    Uses numpy eig to compute the eigenvalues.

    :param m: numpy array
    :returns numpy array containing the eigenvalues
    """
    from numpy import linalg
    w, v = linalg.eig(m)
    return w
##@} 

    
# ---------------------------------------------------------------------
##\ingroup stochastic
#@{

##\brief Return the current seed used by the internal random number generator
#
#Example: myseed = rr.getSeed()
#
#\return The seed value
def getSeed(r):
    """
    Current seed used by the random generator of the RoadRunner instance.

    :param r: RoadRunner instance.
    :returns current seed
    """
    # FIXME: this should be via self not via a RoadRunner instance r
    intg = r.getIntegrator("gillespie")
    if intg is None:
        raise ValueError("model is not loaded")
    return intg['seed']


##\brief Set the seed used by the internal random number generator
#
#Example: rr.setSeed(12345)
#
def setSeed(r, seed):
    """
    Set seed for random number generator (used by gillespie for example).

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


##\brief Run a Gillespie simulation
#
#Example: result = rr.gillespie (0, 100)
#
def gillespie(r, *args, **kwargs):
    """
    Run a Gillespie stochastic simulation.  
    
    Examples:
    
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

    :param r: RoadRunner intance
    :param *args & **kwargs: parameters for simulate
    :returns simulation results
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
##@} 


def RoadRunner(*args):
    return roadrunner.RoadRunner(*args)

# ---------------------------------------------------------------------
##\ingroup plotting
#@{


#\cond
def plotWithLegend(r, result=None, loc='upper left', show=True):
    """
    Plot an array and include a legend. The first argument must be a roadrunner variable. 
    The second argument must be an array containing data to plot. The first column of the array will
    be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object.
    
    plotWithLegend (r)

    :param r: RoadRunner instance
    :param result: results to plot
    :param loc: location of plot legend
    :param show: show the plot
    :returns plt object
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


#\endcond

#\cond
def simulateAndPlot(r, startTime=0, endTime=5, numberOfPoints=500, **kwargs):
    """
    Run simulation and plot the results.

    simulateAndPlot (rr)
    simulateAndPlot (rr, 0, 10, 100)

    :param r: RoadRunner instance
    :param startTime: start time of simulation
    :param endTime: end time of simulation
    :param numberOfPoints: number of points in simulation
    :returns simulation results
    """
    # FIXME: arguments should have the same names like the named arguments in simulate (start, end, ...)
    result = r.simulate(startTime, endTime, numberOfPoints, **kwargs)
    plotWithLegend(r, result)
    return result
#\endcond
 
   
##\brief Plot a numpy array where the first column is considered the x axis and all remaining columns the y axis.
#
#Example: te.plotArray (m, label='Flux')
#\param[in] result Numpy Array
#\return Returns the plot object
def plotArray(*args, **kwargs):
    """
    Plot an array.
    The first column of the array will
    be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object. Note that you can add
    plotting options as named key values after the array. For
    example to add a legend, include the label key value:
    te.plotArray (m, label='A label') then use pylab.legend()
    to make sure the legend is shown. 
    
    result = numpy.array([[1,2,3], [7.2,6.5,8.8], [9.8, 6.5, 4.3]])
    plotArray (result)
    """
    global tehold 
    p = plt.plot(args[0][:, 0], args[0][:, 1:], linewidth=2.5, **kwargs)
    # If user is building a legend don't show the plot yet    
    if 'label' in kwargs:
        return p
    if tehold == False:    
        plt.show()
    return p


##\brief Plot results from a simulation carried out by the simulate or gillespie functions. This is a roadrunner method.
#
# Plot data generated by a simulation:
#
#Example: rr.plot (result)
#
# Data is a numpy array where the first column is considered the x axis and all remaining columns the y axis.
#
# Plot data currently held by roadrunner that was generated in the last simulation.
#
#Example : rr.plot()
#
#\param[in] result Data returned from a simulate or gillespie call
#\return Returns the plot object
def plot(self, result=None, loc='upper left', show=True):
    """
    :param self: RoadRunner instance
    :param result: results to plot
    :param loc: location of plot legend
    :param show: show the plot
    :returns ?
    """
    if result is None:
        # Call Andy version if no results passed to call
        return self.plotAS()
    else:
        return plotWithLegend(self, result, loc, show=show)
##@}


# ---------------------------------------------------------------------
##\ingroup export
#@{

##\brief Returns a Matlab function that represents the current model
#
#Example: print rr.getMatlab()
#\return Returns a string representing the Matlab code
def getMatlab(self):
    """
    Matlab string of current model.
    :returns Matlab string
    """
    return sbml2matlab(self.getCurrentSBML())


##\brief Convenience method for exporting the current model as a Matlab function to a file
#
#Example: rr.exportToMatlab ('c:\\mymodel.m')
def exportToMatlab (self, fileName):
    """
    Save current model as Matlab file.

    rr.exportToMatlab ('mymodel.m')

    :param fileName: file path of matlab file
    :returns:
    """
    saveToFile(fileName, self.getMatlab())


##\brief Returns the Antimony script for the current model
#
#Example: print rr.getAntimony()
#\return Returns a string containing the Antimony script
def getAntimony(self):
    """
    Antimony string of the current model state.

    :returns antimony string
    """
    return sbmlToAntimony(self.getCurrentSBML())
##@}


# ---------------------------------------------------------------------
##\ingroup testmodels
#@{

##\brief Loads a particular test model into roadrunner
#
#Example: rr = roadrunner.loadTestModel ('feedback.xml') 
# 
#\return Returns a reference to roadrunner
def loadTestModel (str):
    """
    Loads the test model into roadrunner.

    :returns RoadRunner instance with test model loaded
    """
    return roadrunner.testing.getRoadRunner(str)


##\brief Returns the SBML for a particular test model
#
#Example: sbmlStr = roadrunner.getTestModel ('feedback.xml') 
# 
#\return Returns a string containing the test model in SBML format
def getTestModel(str):
    """
    Returns the test model as a string.

    :returns string of test model
    """
    return roadrunner.testing.getData(str)


##\brief Returns the list of possible test models
#
#Example: print roadrunner.listTestModels() 
# 
#\return Returns the list of available test model names
def listTestModels():
    """
    List roadrunner SBML test models.

    :returns list of test model paths
    """
    modelList = []
    fileList = roadrunner.testing.dir('*.xml')
    for pathName in fileList:
        modelList.append(os.path.basename(pathName))
    return modelList
##@}


# ---------------------------------------------------------------------
##\ingroup resetmethods
#@{

##\brief Reset the model back to the state it was when it was first loaded
#
#Example: rr.resetToOrigin ()
def resetToOrigin(self):
    """
    Reset model to state when first loaded.
    This resets the model back to the state when it was FIRST loaded,
    this includes all init() and parameters such as k1 etc.

    te.resetToOrigin()

    identical to:
        te.reset(roadrunner.SelectionRecord.ALL)
    """
    self.reset(roadrunner.SelectionRecord.ALL)


##\brief Reset all the state variables to the current initial condition values and the global parameters back to when the model was first loaded.
#
#Example: rr.resetAll ()
def resetAll(self):
    """
    Reset all model variables to CURRENT init(X) values.
    This resets all variables, S1, S2 etc to the CURRENT init(X) values. It also resets all
    parameters back to the values they had when the model was first loaded.
    """
    self.reset(roadrunner.SelectionRecord.TIME |
               roadrunner.SelectionRecord.RATE |
               roadrunner.SelectionRecord.FLOATING |
               roadrunner.SelectionRecord.GLOBAL_PARAMETER)
##@} 


# --------------------------------------------------------------------- 
# Routines to support the Jarnac compatibility layer
# ---------------------------------------------------------------------
##\ingroup jarnac
#@{

##\brief Get the stoichiometry matrix for the current model
#
# Can be further shortened to rr.sm()
#
#Example: mat = rr.getSm()
def getSm(self):
    """
    Returns the full reordered stoichiometry matrix.
    Short-cut sm, e.g.
    
    print rr.sm()
    :returns full reordered stoichiometry matrix
    """
    return self.getFullStoichiometryMatrix()


##\brief Get the names for the reactions in the current model
#
# Can be further shortened to rr.rs()
#
#Example: reactionNames = rr.getRs()  
def getRs(self):
    """
    Returns the list of reaction Identifiers.
    Short-cut rs, e.g.
    
    print(rr.rs())

    :returns reaction identifiers
    """
    return self.model.getReactionIds()


##\brief Get the names for the floating species in the current model
#
# Can be further shortened to rr.fs()
#
#Example: floatingSpeciesNames = rr.getFs()  
def getFs(self):
    """  
    Returns list of floating species identifiers.
    Short-cut fs, e.g.
    
    print (rr.fs())

    :returns floating species identifiers
    """
    return self.model.getFloatingSpeciesIds()


##\brief Get the names for the boundary species in the current model
#
# Can be further shortened to rr.bs()
#
#Example: boundarySpeciesNames = rr.getBs()  
def getBs(self):
    """  
    Returns list of boundary species identifiers.
    Short-cut bs, e.g.
    
    print(rr.bs())

    :returns boundary species identifiers
    """
    return self.model.getBoundarySpeciesIds()


##\brief Get the names for the rglobal parameters in the model
#
# Can be further shortened to rr.ps()
#
#Example: parameterNames = rr.getPs()  
def getPs(self):
    """  
    Returns list of global parameters in the model.
    Short-cut ps, e.g.
    
    print(rr.ps())

    :returns global parameters
    """
    return self.model.getGlobalParameterIds()


##\brief Get the names for the compartments in the current model
#
# Can be further shortened to rr.vs()
#
#Example: compartmentNames = rr.getVs()   
def getVs(self):
    """  
    Returns the list of compartment identifiers.
    Short-cut vs, e.g.

    print(rr.vs())

    :returns compartment identifiers
    """
    return self.model.getCompartmentIds()
    
  
##\brief Get all the rates of change in the current model
#
# Can be further shortened to rr.dv()
#
#Example: rateOfChange = rr.getDv()  
def getDv(self):
    """  
    Returns the list of rates of change.
    Short-cut dv, e.g.
    
    print(rr.dv())

    :returns rate of change
    """
    return self.model.getStateVectorRate()


##\brief Get all the reaction rates in the current model
#
# Can be further shortened to rr.rv()
#
#Example: reactionRates = rr.getRv()  
def getRv(self):
    """  
    Returns the list of reaction rates.
    Short-cut rv, e.g.
    
    print(rr.rv())

    :returns reaction rates
    """
    return self.model.getReactionRates()


##\brief Get all the floating species concentrations in the current model
#
#Example: reactionRates = rr.getSv()  
def getSv(self):
    """  
    Returns the list of floating species concentrations.
    Short-cut sv, e.g.
    
    print rr.sv()

    :returns floating species concentrations
    """
    return self.model.getFloatingSpeciesConcentrations()


##\brief Returns the full Jacobian for the currnet model at the current state
#
#Example: jacobian = rr.getfJac()  
def getfJac(self):
    """  
    Returns the full Jacobian for the current model at the current state.
    Short-cut fjac, e.g.
    
    print(rr.fjac())

    :returns Jacobian at current state
    """
    return self.getFullJacobian()

##@} 

# --------------------------------------------------------------------- 
# Routines flattened from model, aves typing and easier for finding the methods
# ---------------------------------------------------------------------
##\ingroup Get Information Routines
#@{
def getRatesOfChange(self):
    """
    Rate of change of all state variables in the model.

    returns: rate of change of all state variables (eg species) in the model.
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
    self.model.setTime (startTime)
    pass
   
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
##@}
    
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

# Model flattening routines, saves user from having
# to type r.model.methodname and from having to 
# recall where the method is

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

# ---------------------------------------------------------------
# Next comes general documentation
# ---------------------------------------------------------------

##\mainpage notitle
#\section Introduction
#Tellurium is a cross-platform and open source Python based environment that integrates a variety of useful packages for systems biology modeling. The IDE is based on the spyder2 IDE (https://code.google.com/p/spyderlib/)
#
#\par Simple Example:
#\par
#@code
#
#rr = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
#rr.simulate (0, 10, 100)
#rr.plot()
#
#@endcode
#
#\par More Complex Example:
#\par
#@code
#
#import tellurium at te
#
#r = te.loada ('''
#    # A dollar symbol means fix the species concentration
#        $S1 -> S2;  k1*S1; 
#     J2: S2 -> S3;  k2*S2 - k3*S3;
#         S3 -> $S4; k4*S3;
#    
#    k1 = 0.1; S1 = 10
#''')
#
#result = r.simulate (0, 10, 100, ['time', 'S1', 'S3', 'J1'])
#rr.plot (result)
#
#@endcode
#
#\par Screen-shot of Tellurium
#\par 
#\image html http://i.imgur.com/luH3rs6.png
#
##\defgroup utility Utility Methods
# \brief Various utility methods
#
# The most useful methods here are the notices routines. Roadrunner will offen issue warning or informational messages. For
# repeated simulation such messages will clutter up the outputs. noticesOff and noticesOn can be used to turn on an off the messages.
#
#Examples:<br>
#@code
#  # Repeat a simulation many times
#
#  # Load an SBML file
#  r = roadrunner.RoadRunner ('mymodel.xml')
#  # Turn of notices so they don't clutter the output
#  roadrunner.noticesOff()
#  for i in range (0:20):
#      result = r.simulate (0, 10)
#      r.plot (result)
#      r.model.k1 = r.model.k1 + 0.2
#  # Turn the notices back on
#  roadrunner.noticesOn()
#@endcode

##\defgroup filefunctions  File Help Functions
# \brief Save and Read file methods
#
# Use these routines to save or read text files to and from disk
#
#Examples:<br>
#@code
#
# r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
# saveToFile ('mymodel.m', r.getMatlab())
#
# sbmlstr = readFromFile ('mymodel.xml')
#@endcode

##\defgroup loadingModels  Loading Models
# \brief Methods to load models in different formats
#
# There are a variety of methods to load models into libRoadrunner. At the most basic level one can load the model directly using
# libRoadRunner:
#@code
#  r = roadrunner.RoadRunner ('mymodel.xml')
#@endcode
#
#Alternatively one can use these methods:
#@code
#  # This is the same as roadrunner.RoadRunner() but the method name is more suggestive of what it does
#  # Like RoadRunner, loadSBML can accept a file name or a SBML string as it argument
#
#  r = te.loadSBMLModel ('mymodel.xml')
#
#  # To load an Antimony model use:
#  r = te.loadAntimonyModel (antStr)
#
#  # Or alternatively
#  r = te.loadAntimonyModel ('mymodel.ant')
#
#  # The method loada is simply a shortcut to loadAntimonyModel
#  r = loada ('''
#      S1 -> S2; k1*S1;
#      S2 -> S3; k2*S2;
#      
#      k1= 0.1; k2 = 0.2; 
#      S1 = 10; S2 = 0; S3 = 0;
#  ''')
#  result = r.simulate (0, 10, 100)
#  r.plot (result)
#@endcode


##\defgroup interconversion  Interconversion Methods
# \brief Methods to interconvert different formats
#
# Use these routines interconvert verious standard formats
#
#Examples:<br>
#@code
#  # Convert an SBML model into Antimony
#
#  # Load an SBML file
#  sbmlStr = te.readFromFile ('mymodel.xml')
#  # Generate the Antimony format of the SBML model
#  print te.sbmlToAntimony (sbmlStr)
#@endcode
#<br>
#@code
#  # Convert an Antimony model into SBML
#
#  # Load an Antimony file
#  antStr = te.readFromFile ('mymodel.ant')
#  # Generate the SBML format of the Antimony model
#  print te.antimonyToSBML (antStr)
#@endcode

##\defgroup stochastic  Stochastic Simulation Methods
# \brief Methods to carry out stochastic simulations
#
# Use these routines to carry out Gillespie style stochastic simulations
#
#Examples:<br>
#@code
#
#  r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 40')
#  r.setSeed (87675)
#  result = r.gillespie (0, 100)
#  r.plot (result)
#@endcode
#
# Run two simulations and combine the two:
#
#@code{.py}
#  import numpy as np
#  import tellurium as te
#
#  r = te.loadSBMLModel ('mymodel.xml')
#  seed= r.getSeed()
#  result1 = r.gillespie (0, 100)
#  r.model.k1 = r.model.k1*20
#  result2 = r.gillespie (100, 200)
#  # Merge the two runs together
#  rr.plot (np.vstack ((result1, result))
#@endcode

##\defgroup math  Math Utilities
# \brief Useful math utilities
#
# Only one routine is currently available in this group which is a routine to compute the eigenvalues of given a matrix.
#
#Examples:<br>
#@code
#
#import numpy as np
#import tellurium as te
#
#m = np.matrix ([[1,2],[5,7]])
#
#print te.getEigenvalues (m)
#[-0.35889894  8.35889894]
#@endcode

##\defgroup plotting  Plotting Utilities
# \brief Useful plotting utilities
#
# Two useful plotting routines. They assume that the first column in the array is the x-axis and the second and subsequent columns represent curves on the y-axis.
#
#Examples:<br>
#@code
#
#  # Load a model and carry out a simulation generating 100 points
#  r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
#  result = r.simulate (0, 10, 100)
#
#  # No legend will be add to the plot, useful for plotting large 
#  # numbers of curves where a legend would get in the way
#  te.plotArray (result)
#
#  # To get a legend use the roadrunner plot command
#  r.plot (result)
#@endcode

##\defgroup resetmethods  Model Reset Methods
# \brief Model reset methods
#
# Use these routines reset your model back to particular states
#
#Examples:<br>
#@code
#  r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
#  result = r.simulate (0, 10, 100)
#  p.model.S1 = 2.0
#  result = r.simulate (0, 10, 100)
#  # Reset the model back to its original state
#  r.reset()
#@endcode
#
# If you wish to reset a model back to the state it was what it was loaded, use the resetToOrigin method
#
#@code
#  r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
#  result = r.simulate (0, 10, 100)
#  # Make lots of different kinds of changes to the model
#  # Reset the model back to the state it had when it was created
#  r.resetToOrigin()
#@endcode

##\defgroup export Matlab Export Utilities
##\brief Matlab export utilities
#
# Use these routines to convert your model into a Matlab function.
#
#Examples:<br>
#@code
#
# r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
# print r.getMatlab()
# r.exportToMatlab ("mymodel.m")
#@endcode

##\defgroup jarnac Short-cut methods
# \brief Useful short-cut methods

##\defgroup testmodels Test Models
# \brief Methods to acess the builtin test models
#
# RoadRunner has built into it a number of predefined models that can be use
# to easily try out roadrunner if so exmaple you don't have a model at hand.
#
#Examples:<br>
#@code
#  # To get the number of builtin models use lisTestModels
#  print roadrunner.listTestModels()
#  ['feedback.xml', 'test_1.xml']
#@endcode
#
# To load one of the test models use loadTestModel:
#@code
# r = roadrunner.loadTestModel ('feedback.xml')
# result = r.simulate (0, 10, 100)
# r.plot (result)
#@endcode
#
# If you need to obtain the SBML for the test model, use getTestModel
#
#@code
#  sbmlStr = roadrunner.getTestModel
#  saveToFile ('model.xml', sbmlStr)
#@endcode
#
#To look at one of the test model in Antimony form:
#
#@code
#  antstr = te.sbmlToAntimony (roadrunner.getTestModel ('feedback.xml'))
#  print antStr
#@endcode

# OLD CODE----------------------------------------
#def augmentRoadrunnerCtor():
#    """Hides the need to use Antimony directly from user
#    Overwrite the Roadrunner Constructor to accept Antimony string
#    
#    This is done at the begining of the tellurium startup
#    """
#    original_init = roadrplt.plot (result[:,0],result[:,1:], linewidth=2.5)unner.RoadRunner.__init__
#
#    def new_init(self, *args):
#        #get sbml and recompose args tuple
#        if (len(args) > 1 and antimony.loadAntimonyString(args[0]) >= 0):
#            args = ((antimonyTosbml(args[0]),) + args[1:])
#        elif (len(args) == 1 and antimony.loadAntimonyString(args[0]) >= 0):
#            args = (antimonyTosbml(args[0]),)
#        else:
#            pass
#            
#        original_init(self, *args)
#
#    roadrunner.RoadRunner.__init__ = new_init

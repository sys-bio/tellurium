# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:34:07 2013
Updated: July 18, 2014

@author: Herbert M Sauro

Supporting routines for tellurium

"""

import matplotlib.pyplot as plt
import roadrunner
import roadrunner.testing
import libantimony
import tellurium
try:
    from sbml2matlab import sbml2matlab
except ImportError as e:
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))

#get version from VERSION file
def getTelluriumVersion():
    import os
    f = open(os.path.dirname(tellurium.__file__) +'/VERSION.txt', 'r')
    ver = f.read().rstrip()
    f.close()
    return ver
    
# Save a string to a file
def saveToFile (fileName, str):
    """Save a string to a file. Takes two arguments, 
    the file name and the string to save:
    
    saveToFile ('c:\\myfile.txt', strVariable)"""
    outFile = open(fileName, 'w')
    outFile.write(str)
    outFile.close()
    
def readFromFile (fileName):
    """Load a file and return contents as a string, 

    str = readFromFile ('c:\\myfile.txt')"""
 
    file = open(fileName, 'r')
    return file.read()

def loadSBMLModel (sbml):
    rr = roadrunner.RoadRunner (sbml)
    return rr
    
    
def loadCellMLModel (cellML):
    import os
    """Load a cellml model into roadrunner, can
    be a file or string

    r = loadCellMLModel ('mymodel.cellml')"""
    
    if os.path.isfile (cellML):
       sbmlstr = cellmlFileToSBML (cellML)
    else:
       sbmlstr = cellmlStrToSBML (cellML)
    rr = roadrunner.RoadRunner (sbmlstr)
    return rr
    
    
# Load an Antimony file   
def loadAntimonyModel (antStr):
    """Load an Antimony string:
    
    r = loadAntModel (antimonyStr)
    """
    err = libantimony.loadAntimonyString (antStr)
 
    if (err < 0):
       raise Exception('Antimony: ' + libantimony.getLastError())
       
    Id = libantimony.getMainModuleName()
    sbmlStr = libantimony.getSBMLString(Id)
    rr = roadrunner.RoadRunner(sbmlStr)
    return rr


def antimonyTosbml (antStr):
    """Convert an antimony string into SBML:

    sbmlStr = antimonyTosbml (antimonyStr)
    """
    err = libantimony.loadAntimonyString (antStr)

    if (err < 0):
       raise Exception('Antimony: ' + libantimony.getLastError())

    Id = libantimony.getMainModuleName()
    return libantimony.getSBMLString(Id)
   
   
def sbmlToAntimony (str):
    """Convert a SBML string into Antimony:

    sbmlStr = sbmlToAntimony (antimonyStr)
    """
    err = libantimony.loadSBMLString (str)

    if (err < 0):
       raise Exception('Antimony: ' + libantimony.getLastError())

    return libantimony.getAntimonyString(None)
    
    
def cellmlFileToAntimony (CellMLFileName):
    """Load a cellml file and return the
    equivalent antimony string:
    
    ant = cellMLToAntimony('mymodel.cellml')
    """
    if libantimony.loadCellMLFile(CellMLFileName) == -1:
       raise Exception ('Error calling loadCellMLFile')
    libantimony.loadCellMLFile(CellMLFileName)
    return libantimony.getAntimonyString (None)
    
    
def cellmlFileToSBML (CellMLFileName):
    """Load a cellml file and return the
    equivalent SBML string:
    
    sbmlStr = cellMLToSBML('mymodel.cellml')
    """
    
    if libantimony.loadCellMLFile(CellMLFileName) < 0:
       raise Exception ('Error calling loadCellMLFile'+ libantimony.getLastError())
    return libantimony.getSBMLString (None)


def cellmlStrToAntimony (CellMLStr):
    """Convert a cellml string into the
    equivalent antimony string:
    
    ant = cellMLStrToAntimony('mymodel.cellml')
    """
    if libantimony.loadCellMLFile(CellMLStr) < 0:
       raise Exception ('Error calling cellMLStrToAntimony' + libantimony.getLastError())
    return libantimony.getAntimonyString (None)
    
    
def cellmlStrToSBML (CellMLStr):
    """Convert a cellml string into the
    equivalent SBML string:
    
    sbmlStr = cellMLStrToSBML('mymodel.cellml')
    """
    if libantimony.loadCellMLFile(CellMLStr) < 0:
       raise Exception ('Error calling cellMLStrToSBML' + libantimony.getLastError())
    return libantimony.getSBMLString (None)
    
    
def getEigenvalues (m):
    """
    Convenience method for computing the eigenvalues for a matrix, m
    Uses numpy eig to compute the eigenvalues
    """
    from numpy import linalg as LA
    w,v = LA.eig (m)
    return w
    

def getSeed (r):
    """
    Return the current seed used by the random generator
    """
    intg = r.getIntegrator("gillespie")
    if intg is None:
        raise ValueError("model is not loaded")
    return intg['seed']
        
def setSeed (r, seed):
    """
    Set the seed for the random number generator (used by gillespie for example)
    """
    intg = r.getIntegrator('gillespie')
    if intg is None:
        raise ValueError("model is not loaded")

    # there are some issues converting big Python (greater than 4,294,967,295) integers 
    # to C integers on 64 bit machines. If its converted to float before, works around the issue. 
    intg['seed'] = float(seed)

def gillespie (r, *args, **kwargs):
    """
    Run a Gillespie stochastic simulation. 
    Arguments are: roadrunner instance, startTime and endTime.
    The fourth argumentis is optional but if used specifies the number
    of points to generate, that is the simulation output will be
    spaced out on an even grid. A named sixth argument can also be included
    which is the seed value for the random number generator. 

    Examples:
    
    result = te.gillespie (r, 0, 40)
    
    result = te.gillespie (r, 0, 40, 10)
    
    rsult = te.gillespie (r, 0, 40, seed = 123)


    This method also accepts all of the arugments that simulate does. In fact, 
    this is idential to calling simulate with integrator='gillespie', except that
    it resets the integrator back to what it was before. 

    Simulate the optionally plot current SBML model. This is the one stop shopping method
    for simulation and ploting.
    
    simulate accepts a up to four positional arguments and a large number of keyword args.
    
    The first four (optional) arguments are treated as:
    
    1: Start Time, if this is a number.
    
    2: End Time, if this is a number.
    
    3: Number of Steps, if this is a number.
    
    4: List of Selections.
    
    All four of the positional arguments are optional. If any of the positional arguments are
    a list of string instead of a number, then they are interpreted as a list of selections.
    
    
    There are a number of ways to call simulate.
    
    1. With no arguments. In this case, the current set of `SimulateOptions` will
    be used for the simulation. The current set may be changed either directly
    via setSimulateOptions() or with one of the two alternate ways of calling
    simulate.
    
    2: With single `SimulateOptions` argument. In this case, all of the settings
    in the given options are copied and will be used for the current and future
    simulations.
    
    3: With the three positions arguments, `timeStart`, `timeEnd`, `steps`. In this case
    these three values are copied and will be used for the current and future simulations.
    
    4: With keyword arguments where keywords are the property names of the SimulateOptions
    class. To reset the model, simulate from 0 to 10 in 1000 steps and plot we can::
    
    rr.simulate(end=10, start=0, steps=1000, resetModel=True, plot=True)
    
    The options given in the 2nd and 3rd forms will remain in effect until changed. So, if
    one calls::
    
    rr.simulate (0, 3, 100)
    
    The start time of 0, end time of 3 and steps of 100 will remain in effect, so that if this
    is followed by a call to::
    
    rr.simulate()
    
    This simulation will use the previous values.
    
    simulate accepts the following list of keyword arguments:
    
    integrator
    A text string specifying which integrator to use. Currently supports "cvode"
    for deterministic simulation (default) and "gillespie" for stochastic
    simulation.
    
    sel or selections
    A list of strings specifying what values to display in the output.
    
    plot
    True or False
    If True, RoadRunner will create a basic plot of the simulation result using
    the built in plot routine which uses MatPlotLib.
    
    absolute
    A number representing the absolute difference permitted for the integrator
    tolerance.
    
    duration
    The duration of the simulation run, in the model's units of time.
    Note, setting the duration automatically sets the end time and visa versa.
    
    end
    The simulation end time. Note, setting the end time automatically sets
    the duration accordingly and visa versa.
    
    relative
    A float-point number representing the relative difference permitted.
    Defaults 0.0001
    
    resetModel (or just "reset"???)
    True or False
    Causes the model to be reset to the original conditions specified in
    the SBML when the simulation is run.
    
    start
    The start time of the simulation time-series data. Often this is 0,
    but not necessarily.
    
    steps
    The number of steps at which the output is sampled. The samples are evenly spaced.
    When a simulation system calculates the data points to record, it will typically
    divide the duration by the number of time steps. Thus, for N steps, the output
    will have N+1 data rows.
    
    stiff
    True or False
    Use the stiff integrator. Only use this if the model is stiff and causes issues
    with the regular integrator. The stiff integrator is slower than the conventional
    integrator.
    
    multiStep
    True or False
    Perform a multi step integration.
    * Experimental *
    Perform a multi-step simulation. In multi-step simulation, one may monitor the
    variable time stepping via the IntegratorListener events system.

    initialTimeStep
    A user specified initial time step. If this is <= 0, the integrator will attempt
    to determine a safe initial time step.
    
    Note, for each number of steps given to RoadRunner.simulate or RoadRunner.integrate
    the internal integrator may take many many steps to reach one of the external time steps.
    This value specifies an initial value for the internal integrator time step.
    
    minimumTimeStep
    Specify the minimum time step that the internal integrator will use.
    Uses integrator estimated value if <= 0.
    
    maximumTimeStep
    Specify the maximum time step size that the internal integrator will use.
    Uses integrator estimated value if <= 0.
    
    maximumNumSteps
    Specify the maximum number of steps the internal integrator will use before
    reaching the user specified time span. Uses the integrator default value if <= 0.
    
    seed
    Specify a seed to use for the random number generator for stochastic simulations.
    The seed is used whenever the integrator is reset, i.e. `r.reset()`.
    If no seed is specified, the current system time is used for seed. 
    
    
    :returns: a numpy array with each selected output time series being a
    :rtype: numpy.ndarray

    """
    if r.integrator is None:
        raise ValueError("model is not loaded")
    
    prev = r.integrator.name

    if kwargs is not None:
        kwargs['integrator'] = 'gillespie'
    else:
        kwargs = {'integrator' : 'gillespie'}

    result = r.simulate(*args, **kwargs)

    r.setIntegrator(prev)

    return result


#def augmentRoadrunnerCtor():
#    """Hides the need to use Antimony directly from user
#    Overwrite the Roadrunner Constructor to accept Antimony string
#    
#    This is done at the begining of the tellurium startup
#    """
#    original_init = roadrunner.RoadRunner.__init__
#
#    def new_init(self, *args):
#        #get sbml and recompose args tuple
#        if (len(args) > 1 and libantimony.loadAntimonyString(args[0]) >= 0):
#            args = ((antimonyTosbml(args[0]),) + args[1:])
#        elif (len(args) == 1 and libantimony.loadAntimonyString(args[0]) >= 0):
#            args = (antimonyTosbml(args[0]),)
#        else:
#            pass
#            
#        original_init(self, *args)
#
#    roadrunner.RoadRunner.__init__ = new_init

def RoadRunner(args):
    return roadrunner.RoadRunner(args)

def plotWithLegend (r, result):
    """
    Plot an array and include a legend. The first argument must be a roadrunner variable. 
    The second argument must be an array containing data to plot. The first column of the array will
    be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object.
    
    plotWithLegend (r, result)
    """
    if result.dtype.names is None:
       if not isinstance (r, roadrunner.RoadRunner):
          raise Exception ('First argument must be a roadrunner variable')
       columns = result.shape[1]
       legendItems = r.selections[1:]       
       if columns-1 != len (legendItems):
           raise Exception ('Legend list must match result array')
       for i in range(columns-1):
           plt.plot (result[:,0], result[:,i+1], linewidth=2.5, label=legendItems[i])
       plt.legend (loc='upper left')    
       plt.show()
       return plt
    else:
        str = """The result array must be unstructured. Use the command: 
        roadrunner.Config.setValue(rr.Config.SIMULATEOPTIONS_STRUCTURED_RESULT, False)
        to set the right mode."""       
        raise Exception (str)
   
def simulateAndPlot (rr, startTime=0, endTime=5, numberOfPoints=500):
    """
    Carry out a simulation and plot the results. Returns the result to the caller 
    
    Example:
    
    simulateAndPlot (rr)
    
    simulateAndPlot (rr, 0, 10, 100)
    """
    result = rr.simulate (startTime, endTime, numberOfPoints)
    tellurium.plotWithLegend (rr, result)   
    return result
    
# Plot a numpy array
def plotArray (result):
    """
    Plot an array. The first column of the array will
    be the x-axis and remaining columns the y-axis. Returns
    a handle to the plotting object.
    
    result = numpy.array([[1,2,3],[7.2,6.5,8.8], [9.8, 6.5, 4.3]])
    plotArray (result)
    """
    plt.plot (result[:,0],result[:,1:], linewidth=2.5)
    plt.show()
    return plt

def plot (result):
    return plotArray (result)
    
def exportToMatlab (r, filename):
    if not isinstance (r, roadrunner.RoadRunner):
        raise Exception ('First argument must be a roadrunner variable')
    matlab_str = sbml2matlab(r.getCurrentSBML())
    saveToFile (filename, matlab_str)    

def getTestModel (str):
    """
    Returns the model as a string from the test directory
    """
    return roadrunner.testing.getData (str)
    
def loadTestModel(str):
    """
    Loads the test model into roadrunner and returns a roadrunner variable
    """
    return roadrunner.RoadRunner (getTestModel (str)) 
 
def noticesOff ():
    """
    Switch off the generation of notices to the user
    """
    roadrunner.Logger.setLevel(roadrunner.Logger.LOG_WARNING)
    
def noticesOn ():
    """
    Switch on notice generation to the user
    """
    roadrunner.Logger.setLevel(roadrunner.Logger.LOG_NOTICE)

def getRatesOfChange (self):
    """
    Returns the rate of change of all state variables  (eg species) in the model
    """
    return self.model.getStateVectorRate()
 
 # Helper Routines we attach to roadrunner   
roadrunner.RoadRunner.getSeed = getSeed
roadrunner.RoadRunner.setSeed = setSeed
roadrunner.RoadRunner.gillespie = gillespie
roadrunner.RoadRunner.getRatesOfChange = getRatesOfChange
roadrunner.noticesOff = noticesOff
roadrunner.noticesOn = noticesOn   

#augmentRoadrunnerCtor()

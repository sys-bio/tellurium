##@Module Tellurium
#This module allows access to the rr_c_api.dll from python"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:34:07 2013
Updated: July 30, 2014

@author: Herbert M Sauro

Supporting routines for tellurium

"""

import matplotlib.pyplot as plt
import roadrunner
import roadrunner.testing
import libantimony
import tellurium
import numpy
import os
import glob

try:
    from sbml2matlab import sbml2matlab
except ImportError as e:
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))

# ---------------------------------------------------------------------
##\ingroup utility
#@{

##\brief Returns the version number for Tellurium
#
##\brief Set the seed used by the internal random number generator
#
#Example: print te.getTelluriumVersion()
#
#\return Returns a string representing the version number
def getTelluriumVersion():
    import os
    f = open(os.path.dirname(tellurium.__file__) +'/VERSION.txt', 'r')
    ver = f.read().rstrip()
    f.close()
    return ver
    
##\brief Turn off warning messages. Call this to stop roadrunner from printing warning message to the console
#
#Example: roadrunner.noticesOff()
#
def noticesOff ():
    """
    Switch off the generation of notices to the user
    """
    roadrunner.Logger.setLevel(roadrunner.Logger.LOG_WARNING)
    
##\brief Turn on warning messages. Call this to enable roadrunner to print warning messages to the console
#
#Example: roadrunner.noticesOn()
#
def noticesOn ():
    """
    Switch on notice generation to the user
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
def saveToFile (fileName, str):
    """Save a string to a file. Takes two arguments, 
    the file name and the string to save:
    
    saveToFile ('c:\\myfile.txt', strVariable)"""
    outFile = open(fileName, 'w')
    outFile.write(str)
    outFile.close()

##\brief Reads a text file into a string
#
#Example: str = readFromFile ('c:\\myfile.txt')
#
#\param[in] fileName The current time in the simulation
#\return Returns a string representing the contents of the text file
def readFromFile (fileName):
    """Load a file and return contents as a string, 

    str = readFromFile ('c:\\myfile.txt')"""
 
    file = open(fileName, 'r')
    return file.read()
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
def loadSBMLModel (sbml):
    rr = roadrunner.RoadRunner (sbml)
    return rr
    
##\brief Reads an Antimony string into roadrunner
#
#Example: rr = loadAntimonyModel (modelStr)
#
#\param[in] antStr A string containing a Antimony model
#\return Returns a reference to the roadrunner model
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
    
    libantimony.clearPreviousLoads()
    
    return rr

##\brief Reads an Antimony string into roadrunner, short-cut to loadAntimonyModel()
#
#Example: rr = loada ('S1 -> S2; k1*S1; k1 = 0.1; S2 = 10')
#
#\param[in] antStr A string containing a Antimony model
#\return Returns a reference to the roadrunner model
def loada (antStr):
    return loadAntimonyModel (antStr)
   
##\brief Reads a CellML string into roadrunner
#\return Returns a reference to the roadrunner model  
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
##@}    
 
# ---------------------------------------------------------------------
##\ingroup interconversion
#@{

##\brief Converts an Antimony model into SBML
#\return Returns the SBML model as a string
def antimonyTosbml (antStr):
    """Convert an antimony string into SBML:

    sbmlStr = antimonyTosbml (antimonyStr)
    """
    err = libantimony.loadAntimonyString (antStr)

    if (err < 0):
       raise Exception('Antimony: ' + libantimony.getLastError())

    Id = libantimony.getMainModuleName()
    return libantimony.getSBMLString(Id)    
 
##\brief Converts a SBML model to Antimony
#\return Returns the Antimony model as a string
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
def getEigenvalues (m):
    """
    Convenience method for computing the eigenvalues for a matrix, m
    Uses numpy eig to compute the eigenvalues
    """
    from numpy import linalg as LA
    w,v = LA.eig (m)
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
def getSeed (r):
    """
    Return the current seed used by the random generator
    """
    intg = r.getIntegrator("gillespie")
    if intg is None:
        raise ValueError("model is not loaded")
    return intg['seed']
        
##\brief Set the seed used by the internal random number generator
#
#Example: rr.setSeed(12345)
#
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

##\brief Run a Gillespie simulation
#
#Example: result = rr.gillespie (0, 100)
#
def gillespie (r, *args, **kwargs):
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
##@} 

def RoadRunner(args):
    return roadrunner.RoadRunner(args)

# ---------------------------------------------------------------------
##\ingroup plotting
#@{

#\cond
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
#\endcond
 
#\cond  
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
#\endcond
    
##\brief Plot a numpy array where the first column is considered the x axis and all remaining columns the y axis.
#
#Example: te.plotArray (result)
#\param[in] result Numpy Array
#\return Returns the plot object
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
def plot (self, result=None):
    if result is None:
	   # Call Andy version if no results passed to call
       return self.plotAS()
    else:
       return plotWithLegend (self, result)
##@} 
 
# ---------------------------------------------------------------------
##\ingroup export
#@{

##\brief Returns a Matlab function that represents the current model
#
#Example: print rr.getMatlab()
#\return Returns a string representing the Matlab code
def getMatlab (self):
    """
    Returns Matlab string for current model
    """
    return sbml2matlab(self.getCurrentSBML())
  
##\brief Convenience method for exporting the current model as a Matlab function to a file
#
#Example: rr.exportToMatlab ('c:\\mymodel.m')
def exportToMatlab (self, fileName):
    """
    Save the current model as a Matlab file to the give file name
    
    eg
    rr.exportToMatlab ('mymodel.m')
    """
    saveToFile (fileName, self.getMatlab())
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
    Loads the test model into roadrunner
    """
    return roadrunner.testing.getRoadRunner(str)

##\brief Returns the SBML for a particular test model
#
#Example: sbmlStr = roadrunner.getTestModel ('feedback.xml') 
# 
#\return Returns a string containing the test model in SBML format
def getTestModel (str):
    """
    Returns the model as a string from the test directory
    """
    return roadrunner.testing.getData (str)
    
##\brief Returns the list of possible test models
#
#Example: print roadrunner.listTestModels() 
# 
#\return Returns the list of available test model names
def listTestModels():
    # Get the path where roadrunner is installed
	  d = os.path.abspath(roadrunner.__file__)
	  rpath = os.path.dirname (d)
	  # The test files are located in testing
	  rpath = rpath + '\\testing'
	  tmp = os.getcwd()
	  os.chdir (rpath)
	  modelList = glob.glob ('*.xml')
	  os.chdir (tmp)
	  return modelList
##@} 	
	
# ---------------------------------------------------------------------
def getRatesOfChange (self):
    """
    Returns the rate of change of all state variables  (eg species) in the model
    """
    if self.conservedMoietyAnalysis:
       m1 = self.getLinkMatrix()
       m2 = self.model.getStateVectorRate()
       return m1.dot (m2) 
    else:
      return self.model.getStateVectorRate()

# ---------------------------------------------------------------------
##\ingroup resetmethods
#@{

##\brief Reset the model back to the state it was when it was first loaded
#
#Example: rr.resetToOrigin ()
def resetToOrigin(self):
    """ This resets the model back to the state is was when it 
    was FIRST loaded, this includes all init() and parameters such as k1 etc.
    """
    self.reset(SelectionRecord.ALL)

##\brief Reset all the state variables to the current initial condition values
#
#Example: rr.reset ()
def reset(self):
    """
    This resets the variables, S1, S2 etc to the CURRENT init(X) values. 
    It DOES NOT CHANGE the parameters, k1, etc
    """
    self.reset(SelectionRecord.TIME | SelectionRecord.RATE | SelectionRecord.FLOATING)

##\brief Reset all the state variables to the current initial condition values and the global parameters back to when the model was first loaded.
#
#Example: rr.reset ()
def resetAll (self):    
    """
    This resets all variables, S1, S2 etc to the CURRENT init(X) values. It also resets all
    parameter back to the values they had when the model was first loaded 
    """
    
    self.reset(SelectionRecord.TIME | SelectionRecord.RATE | SelectionRecord.FLOATING | SelectionRecord.PARAMETER)
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
def getSm (self):
    """
    Returns the full reordered stoichiometry matrix.

    Short-cut sm, eg
    
    print rr.sm()
    """
    return self.getFullStoichiometryMatrix()
 
##\brief Get the names for the reactions in the current model
#
# Can be further shortened to rr.rs()
#
#Example: reactionNames = rr.getRs()  
def getRs (self):
    """
    Returns the list of reaction Identifiers

    Short-cut rs, eg
    
    print rr.rs()
    """
    return self.model.getReactionIds()
    
##\brief Get the names for the floating species in the current model
#
# Can be further shortened to rr.fs()
#
#Example: floatingSpeciesNames = rr.getFs()  
def getFs (self):
    """  
    Returns the list of floating species identifiers

    Short-cut fs, eg
    
    print rr.fs()
    """
    return self.model.getFloatingSpeciesIds()

##\brief Get the names for the boundary species in the current model
#
# Can be further shortened to rr.bs()
#
#Example: boundarySpeciesNames = rr.getBs()  
def getBs (self):
    """  
    Returns the list of boundary species identifiers

    Short-cut bs, eg
    
    print rr.bs()
    """
    return self.model.getBoundarySpeciesIds()


##\brief Get the names for the rglobal parameters in the model
#
# Can be further shortened to rr.ps()
#
#Example: parameterNames = rr.getPs()  
def getPs (self):
    """  
    Returns the list of global parameters in the model

    Short-cut ps, eg
    
    print rr.ps()
    """
    return self.model.getGlobalParameterIds()
 
##\brief Get the names for the compartments in the current model
#
# Can be further shortened to rr.vs()
#
#Example: compartmentNames = rr.getVs()   
def getVs (self):
    """  
    Returns the list of compartment identifiers

    Short-cut vs, eg
    
    print rr.vs()
    """
    return self.model.getCompartmentIds()
    
  
##\brief Get all the rates of change in the current model
#
# Can be further shortened to rr.dv()
#
#Example: rateOfChange = rr.getDv()  
def getDv (self):
    """  
    Returns the list of rates of change

    Short-cut dv, eg
    
    print rr.dv()
    """
    return self.model.getStateVectorRate()
    
##\brief Get all the reaction rates in the current model
#
# Can be further shortened to rr.rv()
#
#Example: reactionRates = rr.getRv()  
def getRv (self):
    """  
    Returns the list of reaction rates
    
    Short-cut rv, eg
    
    print rr.rv()
    """
    return self.model.getReactionRates()

##\brief Get all the floating species concentrations in the current model
#

#
#Example: reactionRates = rr.getSv()  
def getSv (self):
    """  
    Returns the list of flaoting species concentrations

    Short-cut sv, eg
    
    print rr.sv()
    """
    return self.model.getFloatingSpeciesConcentrations()
##@} 

 # Helper Routines we attach to roadrunner   
roadrunner.RoadRunner.getSeed = getSeed
roadrunner.RoadRunner.setSeed = setSeed
roadrunner.RoadRunner.gillespie = gillespie
roadrunner.RoadRunner.getRatesOfChange = getRatesOfChange
roadrunner.RoadRunner.exportToMatlab = exportToMatlab
roadrunner.RoadRunner.getMatlab = getMatlab
roadrunner.RoadRunner.plotAS = roadrunner.RoadRunner.plot
roadrunner.RoadRunner.plot = plot

roadrunner.noticesOff = noticesOff
roadrunner.noticesOn = noticesOn  
roadrunner.loadTestModel = loadTestModel
roadrunner.listTestModels = listTestModels

roadrunner.RoadRunner.resetToOrigin = resetToOrigin
roadrunner.RoadRunner.reset = reset
roadrunner.RoadRunner.resetAll = resetAll

# Jarnac compatibility layer
roadrunner.RoadRunner.sm = getSm
roadrunner.RoadRunner.fs = getFs
roadrunner.RoadRunner.bs = getBs
roadrunner.RoadRunner.rs = getRs
roadrunner.RoadRunner.ps = getPs
roadrunner.RoadRunner.vs = getVs

roadrunner.RoadRunner.dv = getDv
roadrunner.RoadRunner.rv = getRv
roadrunner.RoadRunner.sv = getSv

#augmentRoadrunnerCtor()

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

##\defgroup filefunctions  File Help Functions
# \brief Save and Read file methods

##\defgroup loadingModels  Loading Models
# \brief Methods to load models in different formats

##\defgroup interconversion  Interconversion Methods
# \brief Methods to interconvert different formats

##\defgroup stochastic  Stochastic Simulation Methods
# \brief Methods to carry out stochastic simulations

##\defgroup math  Math Utilities
# \brief Useful math utilities

##\defgroup plotting  Plotting Utilities
# \brief Useful plotting utilities

##\defgroup resetmethods  Model Reset Methods
# \brief Model reset methods

##\defgroup export Matlab Export Utilities
# \brief Matlab export utilities

##\defgroup jarnac Short-cut methods
# \brief Useful short-cut methods

##\defgroup testmodels Test Models
# \brief Methods to acess the builtin test models


# OLD CODE----------------------------------------
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

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
from sbml2matlab import sbml2matlab

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
    Return the current seed using by the random generator
    """
    return r.integrator['seed']
    
def setSeed (r, seed):
    """
    Set the seed for the random number generator (used by gillespie for example)
    """
    if r.integrator == None:
       r.setIntegrator ('gillespie')
    else:
       r.setIntegrator ('gillespie')
       r.integrator['seed'] = seed

def gillespie (r, startTime, endTime, numberOfPoints=None, seed=None):
    """Run a Gillespie stochastic simulation. 
    Arguments are: roadrunner instance, startTime and endTime.
    The fourth argumentis is optional but if used specifies the number
    of points to generate, that is the simulation output will be
    spaced out on an even grid. A named sixth argument can also be included
    which is the seed value for the random number generator. Be careful
    
    Examples:
    
    result = te.gillespie (r, 0, 40)
    
    result = te.gillespie (r, 0, 40, 10)
    
    rsult = te.gillespie (r, 0, 40, seed = 123)
    """
    r.setIntegrator('gillespie')
            
    if numberOfPoints is None:
       if seed is None:
          result = r.simulate (startTime, endTime)        
       else:
          result = r.simulate (startTime, endTime, seed=seed)         
    else:
       if seed is None:
          result = r.simulate (startTime, endTime, numberOfPoints)
       else:
          result = r.simulate (startTime, endTime, numberOfPoints, seed=seed) 
    r.setIntegrator ('cvode')                  
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
 
roadrunner.RoadRunner.getSeed = getSeed
roadrunner.RoadRunner.setSeed = setSeed
roadrunner.RoadRunner.gillespie = gillespie
   
#augmentRoadrunnerCtor()

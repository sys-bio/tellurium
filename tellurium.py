# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:34:07 2013
Updated march 25, 2014

@author: Herbert M Sauro

Supporting routines to help users easily 
pass Antimony models to roadRunner

"""

import matplotlib.pyplot as plt
import roadrunner
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
    
# Load an Antimony file   
def loadAntimonyModel (antStr):
    """Load an Antimony string:
    
    r = loadAntimonyModel(antStr)
    """
    return roadrunner.RoadRunner(antStr)

def sbmlFromAntimony (antStr):
    """Load an Antimony string:

    sbmlStr = sbmlFromAntimony(antimonyStr)
    """
    err = libantimony.loadAntimonyString (antStr)

    if (err < 0):
       raise Exception('Antimony: ' + libantimony.getLastError())

    Id = libantimony.getMainModuleName()
    return libantimony.getSBMLString(Id)
    

def augmentRoadrunnerCtor():
    """Hides the need to use Antimony directly from user
    Overwrite the Roarunner Constructor to accept Antimony string
    
    This is done atthe begining of the tellurium startup
    """
    original_init = roadrunner.RoadRunner.__init__

    def new_init(self, *args):
        #get sbml and recompose args tuple
        if (len(args) > 1 and libantimony.loadAntimonyString(args[0]) >= 0):
            args = ((sbmlFromAntimony(args[0]),) + args[1:])
        elif (len(args) == 1 and libantimony.loadAntimonyString(args[0]) >= 0):
            print "here"
            args = (sbmlFromAntimony(args[0]),)
        else:
            pass
            
        original_init(self, *args)

    roadrunner.RoadRunner.__init__ = new_init

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

augmentRoadrunnerCtor()
print ("Importing tellurium as 'te' v"+ getTelluriumVersion())


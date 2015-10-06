# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 16:19:44 2015

@author: Kiri Choi
"""

import os.path
import sys, StringIO
import antimony
import roadrunner
import tellurium as te
import zipfile
import tempfile
import re
try:
    import phrasedml
except ImportError as e:
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
try:
    import tecombine as combine
except ImportError as e:
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))

class tePhrasedml(object):
    def __init__(self, antimonyStr, phrasedmlStr):
        modelispath = False
        if type(antimonyStr) != str:
            raise Exception("Invalid Antimony string/model path")
        else:
            if os.path.exists(antimonyStr): #incomplete - load model path directly.
                modelispath = True
            else:
                pass
        if type(phrasedmlStr) != str:
            raise Exception("Invalid PhrasedML string")
                
        tePhrasedml.modelispath = modelispath
        tePhrasedml.antimonyStr = antimonyStr
        tePhrasedml.phrasedmlStr = phrasedmlStr
        
    def execute(self):
        outputstr = self.createpython()
        
        try:
            exec(outputstr)
        except Exception as e:
            raise e
        
    def createpython(self): # Create and return Python script given antimony and phrasedml strings
        rePath = r"(\w*).load\('(.*)'\)"
        reLoad = r"(\w*) = roadrunner.RoadRunner\(\)"
        reModel = r"(\w*) = model (.*)"
        phrasedmllines = self.phrasedmlStr.splitlines()
        for i,s in enumerate(phrasedmllines):
            reSearchModel = re.split(reModel, s)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[2]).replace('"', '')
                modelsource = str(modelsource).replace("'", '')
                modelsource = str(modelsource).replace(".xml", '')
        
        sedmlstr = phrasedml.convertString(self.phrasedmlStr)
        
        fd1, sedmlfilepath = tempfile.mkstemp()        
        os.write(fd1, sedmlstr)
        
        pysedml = te.SedmlToRr.sedml_to_python(sedmlfilepath)
        if self.modelispath == False:
            lines = pysedml.splitlines()
            for i,s in enumerate(lines):
                reSearchPath = re.split(rePath, s)
                if len(reSearchPath) > 1:
                    del lines[i]
            for i,s in enumerate(lines):
                reSearchLoad = re.split(reLoad, s)
                if len(reSearchLoad) > 1:
                    s = s.replace("roadrunner.RoadRunner()", "te.loada(" + str(modelsource)+ ")")
                    lines[i] = s
                    
            if not "import tellurium" in pysedml:
                if "import roadrunner" in pysedml:
                    for i,s in enumerate(lines):
                        if "import roadrunner" in s:
                            del lines[i]
                            lines.insert(i, "import tellurium as te")
                        else:
                            pass
        
        pysedml = '\n'.join(lines)
        
        # List of replacements
        pysedml = pysedml.replace('"compartment"', '"compartment_"')
        pysedml = pysedml.replace("'compartment'", "'compartment_'")
        
        
        outputstr = str(modelsource) + " = '''" + self.antimonyStr + "'''\n\n" + pysedml
        
        os.close(fd1)
        os.remove(sedmlfilepath)
        
        return outputstr
        
    def printpython(self):
        outputstr = self.createpython()
        print outputstr
    
    def exportAsCombine(self, outputpath): # parameter outputpath must be a full path of a zip file you wish to create
        # Temporary failsafe - Should be revised once libphrasedml adopts returning of model name
        reModel = r"(\w*) = model (.*)"
        lines = self.phrasedmlStr.splitlines()
        for i,s in enumerate(lines):
            reSearchModel = re.split(reModel, s)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[2]).replace('"', '')
                modelsource = str(modelsource).replace("'", '')
                if ".xml" or ".sbml" not in modelsource:
                    modelpath = modelsource + ".xml"
                    s = s.replace(modelsource, modelpath)
                    lines[i] = s
        
        revphrasedml = '\n'.join(lines)
        combine.export(outputpath, self.antimonyStr, modelpath, revphrasedml)
                
    def getAntimonyString(self):
        return self.antimonyStr
        
    def getPhrasedmlString(self):
        return self.phrasedmlStr
        
    def getSedmlString(self):
        return phrasedml.convertString(self.phrasedmlStr)
    
    
    
    
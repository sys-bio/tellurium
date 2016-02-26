# -*- coding: utf-8 -*-
"""
SEDML support for PhraSED-ML: The Paraphrased Human-Readable Adaptation of SED-ML
PhraSED-ML is a language and a library that provide a text-based way to read, summarize,
and create SED-ML files. A basic phraSED-ML script will look like this:
::

  mod1 = model "sbml_model.xml"
  sim1 = simulate uniform(0,10,100)
  task1 = run sim1 on mod1
  plot time vs S1

Provides a simple description language to create the SED-ML parts
- models
- simulations
- tasks
- output
"""

from __future__ import print_function, division

import os.path
import tempfile
import re
import roadrunner
import tellurium as te
import tecombine
import tesedml

try:
    import phrasedml
except ImportError as e:
    phrasedml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))


class tePhrasedml(object):
    """ SEDML helper class.

    This class is responsible for the creation of executable tellurium code
    phrasedml descriptions. Main function is a code factory.
    Very similar to the more general tesedml which creates python executable code
    from from given SED-ML.
    """

    def __init__(self, antimonyStr, phrasedmlStr):
        """ Constructor from antimony string and phrasedml string.

        :param antimonyStr: list of antimony model string
        :type antimonyStr: list
        :param phrasedmlStr: list of phrasedml string
        :type phrasedmlStr: list
        """
        modelispath = []
        if type(antimonyStr) != list:
                raise Exception("antimony models must given as a list")
        for i in range(len(antimonyStr)):
            if type(antimonyStr[i]) != str:
                raise Exception("invalid Antimony string/model path")
            else:
                if os.path.exists(antimonyStr[i]):
                    modelispath.append(True)
                else:
                    modelispath.append(False)
        if type(phrasedmlStr) != list:
            raise Exception("sedml files must given as a list")

        self.modelispath = modelispath
        self.antimonyStr = antimonyStr
        self.phrasedmlStr = phrasedmlStr

    def execute(self, selPhrasedml):
        """ Executes created python code.
        See :func:`createpython`
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str
        """
        execStr = self.createpython(selPhrasedml)
        try:
            # This calls exec. Be very sure that nothing bad happens here.
            exec execStr
        except Exception as e:
            raise e

    def createpython(self, selPhrasedml):
        """ Create and return python script given phrasedml string.
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str

        :returns: python string to execute
        :rtype: str
        """
        antInd = None
        rePath = r"(\w*).load\('(.*)'\)"
        reLoad = r"(\w*) = roadrunner.RoadRunner\(\)"
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        phrasedmllines = selPhrasedml.splitlines()
        for k, line in enumerate(phrasedmllines):
            reSearchModel = re.split(reModel, line)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])
                modelname = os.path.basename(modelsource)
                modelname = str(modelname).replace(".xml", '')
        for i in range(len(self.antimonyStr)):
            r = te.loada(self.antimonyStr[i])
            modelName = r.getModel().getModelName()
            if modelName == modelsource:
                antInd = i
        
        if antInd == None:
            raise Exception("Cannot find the model name referenced in the PhraSEDML string")
        else:
            pass
        phrasedml.setReferencedSBML(modelsource, te.antimonyToSBML(self.antimonyStr[antInd]))
        sedmlstr = phrasedml.convertString(selPhrasedml)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())

        phrasedml.clearReferencedSBML()

        fd1, sedmlfilepath = tempfile.mkstemp()
        os.write(fd1, sedmlstr)
        pysedml = tesedml.sedmlToPython(sedmlfilepath)

        # perform some replacements in the sedml
        if self.modelispath[antInd] is False:
            lines = pysedml.splitlines()
            for k, line in enumerate(lines):
                reSearchPath = re.split(rePath, line)
                if len(reSearchPath) > 1:
                    del lines[k]

            for k, line in enumerate(lines):
                reSearchLoad = re.split(reLoad, line)
                if len(reSearchLoad) > 1:
                    line = line.replace("roadrunner.RoadRunner()", "te.loada(" + str(modelname) + ")")
                    lines[k] = line

            if "import tellurium" not in pysedml:
                if "import roadrunner" in pysedml:
                    for k, line in enumerate(lines):
                        if "import roadrunner" in line:
                            del lines[k]
                            lines.insert(k, "import tellurium as te")
                        else:
                            pass

        pysedml = '\n'.join(lines)

        # List of replacements
        pysedml = pysedml.replace('"compartment"', '"compartment_"')
        pysedml = pysedml.replace("'compartment'", "'compartment_'")

        outputstr = str(modelname) + " = '''" + self.antimonyStr[antInd] + "'''\n\n" + pysedml

        os.close(fd1)
        os.remove(sedmlfilepath)

        return outputstr

    def printpython(self, selPhrasedml):
        """ Prints the created python string by :func:`createpython`. 
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str        
        """
        execStr = self.createpython(selPhrasedml)
        print(execStr)

    def exportAsCombine(self, outputpath):
        """ Export as a combine archive.

        :param outputpath: full path of the combine zip file to create
        :type outputpath: str
        """

        # export the combine archive
        tecombine.export(outputpath, self.antimonyStr, self.phrasedmlStr)

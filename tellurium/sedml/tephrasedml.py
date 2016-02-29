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
import re
import tempfile

import tellurium as te
import tellurium.tecombine
import phrasedml
import tesedml


class experiment(object):
    """ Phrasedml experiment.

    This class is responsible for the creation of executable tellurium code
    phrasedml descriptions. Main function is a code factory.
    Very similar to the more general tesedml which creates python executable code
    from from given SED-ML.
    """

    def __init__(self, antimonyStr, phrasedmlStr):
        """ Create experiment from antimony and phrasedml string.

<<<<<<< HEAD:tellurium/sedml/tephrasedml.py
            :param ant: Antimony string of model
            :type ant: str
            :param phrasedml: phrasedml simulation description
            :type phrasedml: str
            :returns: SEDML experiment description
=======
        :param antimonyStr: list of antimony model string
        :type antimonyStr: list
        :param phrasedmlStr: list of phrasedml string
        :type phrasedmlStr: list
>>>>>>> master:tellurium/tephrasedml.py
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

<<<<<<< HEAD:tellurium/sedml/tephrasedml.py
    def getAntimonyString(self):
        """ Get antimony string.

        :returns: antimony string
        :rtype: str
        """
        return self.antimonyStr

    def getSbmlString(self):
        """ Get SBML string.

        :returns: SBML string
        :rtype: str
        """
        return te.antimonyToSBML(self.antimonyStr)

    def getPhrasedmlString(self):
        """ Get phrasedml string.

        :returns: phrasedml string
        :rtype: str
        """
        return self.phrasedmlStr

    def getSedmlString(self):
        """ Get sedml string.

        :returns: sedml
        :rtype: str
        """
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        phrasedmllines = self.phrasedmlStr.splitlines()
        for line in phrasedmllines:
            reSearchModel = re.split(reModel, line)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])

        phrasedml.setReferencedSBML(modelsource, te.antimonyToSBML(self.antimonyStr))
        sedmlstr = phrasedml.convertString(self.phrasedmlStr)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())
        phrasedml.clearReferencedSBML()

        return sedmlstr

    def execute(self, show=True):
=======
    def execute(self, selPhrasedml):
>>>>>>> master:tellurium/tephrasedml.py
        """ Executes created python code.
        See :func:`createpython`
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str
        """
<<<<<<< HEAD:tellurium/sedml/tephrasedml.py
        execStr = self.createpython()
        if show:
            print('*'*80)
            print('EXECUTED')
            print('*'*80)
            print(execStr)
            print('*'*80)
=======
        execStr = self.createpython(selPhrasedml)
>>>>>>> master:tellurium/tephrasedml.py
        try:
            # This calls exec. Be very sure that nothing bad happens here.
            exec execStr
        except Exception as e:
            raise e

<<<<<<< HEAD:tellurium/sedml/tephrasedml.py
    def createpython(self):
        """ Create and return python script given antimony and phrasedml strings.

        This creates the full model decription including the
        antimony and phrasedml strings.
=======
    def createpython(self, selPhrasedml):
        """ Create and return python script given phrasedml string.
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str
>>>>>>> master:tellurium/tephrasedml.py

        :returns: python string to execute
        :rtype: str
        """
<<<<<<< HEAD:tellurium/sedml/tephrasedml.py
        # TODO: remove the tempfiles !

        # create xml and sedml
=======
        antInd = None
>>>>>>> master:tellurium/tephrasedml.py
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
<<<<<<< HEAD:tellurium/sedml/tephrasedml.py

                sbml_str = te.antimonyToSBML(self.antimonyStr)
                phrasedml.setReferencedSBML(modelsource, sbml_str)
=======
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
>>>>>>> master:tellurium/tephrasedml.py

        # create temporary archive
        import tempfile
        tempdir = tempfile.mkdtemp(suffix="_sedml")

        expArchive = os.path.join(tempdir, "{}.sedx".format(modelname))
        print("Combine Archive:", expArchive)
        self.exportAsCombine(expArchive)

        # Create python code
        pysedml = tesedml.sedmlToPython(expArchive)
        # outputstr = str(modelname) + " = '''" + self.antimonyStr + "'''\n\n" + pysedml

        return pysedml

<<<<<<< HEAD:tellurium/sedml/tephrasedml.py
    def exportAsCombine(self, exportPath):
=======
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
>>>>>>> master:tellurium/tephrasedml.py
        """ Export as a combine archive.

        This is the clean way to execute it.
        A combine archive is created which afterwards is handeled by the SEDML to python script.

        :param exportPath: full path of the combine zip file to create
        :type exportPath: str
        """
<<<<<<< HEAD:tellurium/sedml/tephrasedml.py
        # Temporary failsafe - Should be revised once libphrasedml adopts returning of model name
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        # rePlot = r"""plot ('|")(.*)('|") (.*)"""
        lines = self.phrasedmlStr.splitlines()
        for i, s in enumerate(lines):
            reSearchModel = re.split(reModel, s)
            # reSearchPlot = re.split(rePlot, s)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])
                modelname = os.path.basename(modelsource)
                if ".xml" or ".sbml" not in modelsource:
                    modelname = modelname + ".xml"
                s = s.replace(modelsource, modelname)
                lines[i] = s

                # if len(reSearchPlot) > 1:
                #    plottitle = str(reSearchPlot[2])

        revphrasedml = '\n'.join(lines)

        # export the combine archive
        phrasedml.setReferencedSBML(modelname, te.antimonyToSBML(self.antimonyStr))
        tellurium.tecombine.export(exportPath, self.antimonyStr, modelname, revphrasedml)
        phrasedml.clearReferencedSBML()

    def printpython(self):
        """ Prints the created python string by :func:`createpython`. """
        print(self.createpython())



=======

        # export the combine archive
        tecombine.export(outputpath, self.antimonyStr, self.phrasedmlStr)
>>>>>>> master:tellurium/tephrasedml.py

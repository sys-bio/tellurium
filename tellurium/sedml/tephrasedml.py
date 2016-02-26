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
    """ SEDML helper class.

    This class is responsible for the creation of executable tellurium code
    phrasedml descriptions. Main function is a code factory.
    Very similar to the more general tesedml which creates python executable code
    from from given SED-ML.
    """

    def __init__(self, antimonyStr, phrasedmlStr):
        """ Create experiment from antimony and phrasedml string.

            :param ant: Antimony string of model
            :type ant: str
            :param phrasedml: phrasedml simulation description
            :type phrasedml: str
            :returns: SEDML experiment description
        """
        modelispath = False
        if type(antimonyStr) != str:
            raise Exception("Invalid Antimony string/model path")
        else:
            if os.path.exists(antimonyStr):
                # incomplete - load model path directly.
                modelispath = True
            else:
                pass
        if type(phrasedmlStr) != str:
            raise Exception("Invalid PhrasedML string")

        self.modelispath = modelispath
        self.antimonyStr = antimonyStr
        self.phrasedmlStr = phrasedmlStr

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
        """ Executes created python code.
        See :func:`createpython`
        """
        execStr = self.createpython()
        if show:
            print('*'*80)
            print('EXECUTED')
            print('*'*80)
            print(execStr)
            print('*'*80)
        try:
            # This calls exec. Be very sure that nothing bad happens here.
            exec execStr
        except Exception as e:
            raise e

    def createpython(self):
        """ Create and return python script given antimony and phrasedml strings.

        This creates the full model decription including the
        antimony and phrasedml strings.

        :returns: python string to execute
        :rtype: str
        """
        # create xml and sedml
        rePath = r"(\w*).load\('(.*)'\)"
        reLoad = r"(\w*) = roadrunner.RoadRunner\(\)"
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        phrasedmllines = self.phrasedmlStr.splitlines()
        for k, line in enumerate(phrasedmllines):
            reSearchModel = re.split(reModel, line)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])
                modelname = os.path.basename(modelsource)
                modelname = str(modelname).replace(".xml", '')

                sbml_str = te.antimonyToSBML(self.antimonyStr)
                phrasedml.setReferencedSBML(modelsource, sbml_str)

        # create archive
        expArchive = os.path.join(os.getcwd(), "{}.sedx".format(modelname))
        print("Combine Archive:", expArchive)
        self.exportAsCombine(expArchive)

        # Create python code
        pysedml = tesedml.sedmlToPython(expArchive)
        # outputstr = str(modelname) + " = '''" + self.antimonyStr + "'''\n\n" + pysedml

        return pysedml

    def exportAsCombine(self, exportPath):
        """ Export as a combine archive.

        This is the clean way to execute it.
        A combine archive is created which afterwards is handeled by the SEDML to python script.

        :param exportPath: full path of the combine zip file to create
        :type exportPath: str
        """
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




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
import tellurium.tecombine as tecombine
import phrasedml
import tesedml


class experiment(object):
    """ Phrasedml experiment.

    This class is responsible for the creation of executable tellurium code
    phrasedml descriptions. Main function is a code factory.
    Very similar to the more general tesedml which creates python executable code
    from from given SED-ML.
    """

    def __init__(self, antimonyList, phrasedmlList):
        """ Create experiment from lists of antimony and phrasedml strings.

        :param antimonyList: list of antimony model string
        :type antimonyList: list
        :param phrasedmlList: list of phrasedml string
        :type phrasedmlList: list
        """
        modelispath = []
        if isinstance(antimonyList, basestring):
            antimonyList = [antimonyList]
        if isinstance(phrasedmlList, basestring):
            phrasedmlList = [phrasedmlList]

        for aStr in antimonyList:
            if not isinstance(aStr, basestring):
                raise IOError("invalid Antimony string/model path")
            else:
                if os.path.exists(aStr):
                    modelispath.append(True)
                else:
                    modelispath.append(False)

        self.modelispath = modelispath
        self.antimonyList = antimonyList
        self.phrasedmlList = phrasedmlList

    def execute(self, selPhrasedml):
        """ Executes created python code.
        See :func:`createpython`
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str
        """
        execStr = self.createpython(selPhrasedml)

        # This calls exec. Be very sure that nothing bad happens here.
        exec execStr


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

        # find index
        for k, antStr in enumerate(self.antimonyList):
            r = te.loada(antStr)
            modelName = r.getModel().getModelName()
            if modelName == modelsource:
                antInd = k

        phrasedml.setReferencedSBML(modelsource, te.antimonyToSBML(self.antimonyList[antInd]))
        sedmlstr = phrasedml.convertString(selPhrasedml)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())

        phrasedml.clearReferencedSBML()
        f = tempfile.NamedTemporaryFile('w', suffix=".sedml")
        f.write(sedmlstr)
        f.flush()
        pysedml = tesedml.sedmlToPython(f.name)

        # perform some replacements in the sedml
        if self.modelispath[antInd] is False:
            lines = pysedml.splitlines()
            for k, line in enumerate(lines):
                reSearchPath = re.split(rePath, line)
                if len(reSearchPath) > 1:
                    del lines[k]

        if antInd is None:
            raise Exception("Cannot find the model name referenced in the PhraSEDML string")

        # create temporary archive
        tempdir = tempfile.mkdtemp(suffix="_sedml")

        expArchive = os.path.join(tempdir, "{}.sedx".format(modelname))
        print("Combine Archive:", expArchive)
        self.exportAsCombine(expArchive)

        # Create python code
        pysedml = tesedml.sedmlToPython(expArchive)

        # outputstr = str(modelname) + " = '''" + self.antimonyList[antInd] + "'''\n\n" + pysedml
        return pysedml


    def printpython(self, selPhrasedml):
        """ Prints the created python string by :func:`createpython`. 
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str        
        """
        execStr = self.createpython(selPhrasedml)
        print(execStr)

    def exportAsCombine(self, outputpath):
        """ Export as a combine archive.

        This is the clean way to execute it.
        A combine archive is created which afterwards is handeled by the SEDML to python script.

        :param exportPath: full path of the combine zip file to create
        :type exportPath: str
        """
        # export the combine archive
        tecombine.export(outputpath, self.antimonyList, self.phrasedmlList)


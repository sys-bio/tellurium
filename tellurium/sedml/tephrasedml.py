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
import warnings

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

    def execute(self, selPhrasedml=None, workingDir=None):
        """ Executes the python code created for the given phrasedml.
        The workingDir sets the path variable where the combine
        archive and files are generated for execution.

        See :func:`createpython`
        
        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str
        """
        if selPhrasedml is None:
            warnings.warn("No phrasedmlStr provided in experiment.execute()")
        execStr = self._toPython(selPhrasedml, workingDir=workingDir)
        # This calls exec. Be very sure that nothing bad happens here.
        exec execStr

    def _toPython(self, phrasedmlStr, workingDir=None):
        """ Create and return python script given phrasedml string.
        
        :param phrasedmlStr: Name of PhraSEDML string defined in the code
        :type phrasedmlStr: str

        :returns: python string to execute
        :rtype: str
        """
        import tempfile

        if phrasedmlStr == None:

            if len(self.phrasedmlList) == 1:
                phrasedmlStr = self.phrasedmlList[0]
                warnings.warn("No phrasedml string selected, defaulting to first phrasedml.")
            else:
                raise IOError('No phrasedmlStr selected.')

        rePath = r"(\w*).load\('(.*)'\)"
        # reLoad = r"(\w*) = roadrunner.RoadRunner\(\)"

        # model info from phrasedml
        modelsource, modelname = self._modelInfoFromPhrasedml(phrasedmlStr)
        # print('Model name:', modelname)

        # find index of antimony str
        antIndex = None
        for k, antStr in enumerate(self.antimonyList):
            r = te.loada(antStr)
            modelName = r.getModel().getModelName()
            if modelName == modelsource:
                antIndex = k
        if antIndex is None:
            raise Exception("Cannot find the model name referenced in the PhraSEDML string")

        phrasedml.setReferencedSBML(modelsource, te.antimonyToSBML(self.antimonyList[antIndex]))
        sedmlstr = phrasedml.convertString(phrasedmlStr)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())

        phrasedml.clearReferencedSBML()
        f = tempfile.NamedTemporaryFile('w', suffix=".sedml")
        f.write(sedmlstr)
        f.flush()
        pysedml = tesedml.sedmlToPython(f.name)

        # perform some replacements in the sedml
        if self.modelispath[antIndex] is False:
            lines = pysedml.splitlines()
            for k, line in enumerate(lines):
                reSearchPath = re.split(rePath, line)
                if len(reSearchPath) > 1:
                    del lines[k]

        # Create the combine archive and use it for execution
        if workingDir is None:
            workingDir = tempfile.mkdtemp(suffix="_sedml")

        expArchive = os.path.join(workingDir, "{}.sedx".format(modelname))
        print("Combine Archive:", expArchive)
        self.exportAsCombine(expArchive)

        # Create python code
        pysedml = tesedml.sedmlToPython(expArchive)

        # outputstr = str(modelname) + " = '''" + self.antimonyList[antInd] + "'''\n\n" + pysedml
        return pysedml

    def printPython(self, phrasedmlStr=None):
        """ Prints the created python string by :func:`createpython`. 
        
        :param phrasedmlStr: Name of PhraSEDML string defined in the code
        :type phrasedmlStr: str
        """
        execStr = self._toPython(phrasedmlStr)
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

    @staticmethod
    def _modelInfoFromPhrasedml(phrasedmlStr):
        """ Find model information in phrasedml String. """
        # find model source, name
        reModel = r"""(\w+)\s*=\s*model\s*('|")(.*)('|")"""
        lines = phrasedmlStr.splitlines()
        for k, line in enumerate(lines):
            reSearchModel = re.split(reModel, line)
            if (len(reSearchModel) > 1):
                # FIXME: work with multiple antimony models
                modelsource = str(reSearchModel[3])
                modelname = os.path.basename(modelsource)
                modelname = str(modelname).replace(".xml", '')
                break
        else:
            raise IOError('No model definition in phrasedml string: {}'.format(phrasedmlStr))

        return modelsource, modelname
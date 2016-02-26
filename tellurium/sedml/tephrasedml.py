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

import roadrunner
import tellurium.tellurium.tellurium as te

import tellurium.sedml.tesedml
import tellurium.tecombine

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

        :param antimonyStr: antimony model string
        :type antimonyStr: str
        :param phrasedmlStr: phrasedml string
        :type phrasedmlStr: str
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

    def exportAsCombine(self, outputpath):
        """ Export as a combine archive.

        This is the clean way to execute it.
        A combine archive is created which afterwards is handeled by the SEDML to python script.

        :param outputpath: full path of the combine zip file to create
        :type outputpath: str
        """
        # TODO:

        # FIXME: why is this not using the combine archive (tecombine)
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
        tellurium.tecombine.export(outputpath, self.antimonyStr, modelname, revphrasedml)
        phrasedml.clearReferencedSBML()



    def execute(self):
        """ Executes created python code.
        See :func:`createpython`
        """
        execStr = self.createpython()
        try:
            # This calls exec. Be very sure that nothing bad happens here.
            exec execStr
        except Exception as e:
            raise e

    def createpython(self):
        """ Create and return python script given antimony and phrasedml strings.
        Uses the tesedml.create

        :returns: python string to execute
        :rtype: str
        """
        # created sedml
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

        phrasedml.setReferencedSBML(modelsource, te.antimonyToSBML(self.antimonyStr))
        sedmlstr = phrasedml.convertString(self.phrasedmlStr)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())

        phrasedml.clearReferencedSBML()

        fd1, sedmlfilepath = tempfile.mkstemp()
        os.write(fd1, sedmlstr)
        pysedml = tellurium.sedml.tesedml.sedmlToPython(sedmlfilepath)

        # perform some replacements in the sedml
        if self.modelispath is False:
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

        outputstr = str(modelname) + " = '''" + self.antimonyStr + "'''\n\n" + pysedml

        os.close(fd1)
        os.remove(sedmlfilepath)

        return outputstr

    def printpython(self):
        """ Prints the created python string by :func:`createpython`. """
        execStr = self.createpython()
        print(execStr)




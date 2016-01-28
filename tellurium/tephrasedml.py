# -*- coding: utf-8 -*-
"""
SEDML support for phrasedml.

@author: Kiri Choi
"""

# FIXME: the following should be instance variables (or singleton class)
#         tePhrasedml.modelispath = modelispath
#         tePhrasedml.antimonyStr = antimonyStr
#         tePhrasedml.phrasedmlStr = phrasedmlStr
# In the current implementation this will create problems in case of multiple instances of the class.
# Either make this instance variable or make tePhrasedml a singleton class
# see all the access via self. in exportAsCombine


from __future__ import print_function, division

import os.path
import roadrunner
import tellurium as te
import tempfile
import re

try:
    import phrasedml
except ImportError as e:
    phrasedml = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
try:
    import tecombine as combine
except ImportError as e:
    combine = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))


class tePhrasedml(object):
    """ phrasedml helper class. """

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

        tePhrasedml.modelispath = modelispath
        tePhrasedml.antimonyStr = antimonyStr
        tePhrasedml.phrasedmlStr = phrasedmlStr

    def getAntimonyString(self):
        """ Get antimony string.
        :returns: antimony string
        :rtype: string
        """
        return self.antimonyStr

    def getSbmlString(self):
        """ Get SBML string.
        :returns: SBML string
        :rtype: string
        """
        return te.antimonyTosbml(self.antimonyStr)

    def getPhrasedmlString(self):
        """ Get phrasedml string.
        :returns: phrasedml string
        :rtype: string
        """
        return self.phrasedmlStr

    def getSedmlString(self):
        """ Get sedml string.
        :returns: sedml string
        :rtype: string
        """
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        phrasedmllines = self.phrasedmlStr.splitlines()
        for line in phrasedmllines:
            reSearchModel = re.split(reModel, line)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])

        phrasedml.setReferencedSBML(modelsource, te.antimonyTosbml(self.antimonyStr))
        sedmlstr = phrasedml.convertString(self.phrasedmlStr)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())
        phrasedml.clearReferencedSBML()

        return sedmlstr

    def execute(self):
        """ Executes created python code.
        See :func:`createpython`
        """
        execStr = self.createpython()
        try:
            exec execStr
        except Exception as e:
            raise e

    def createpython(self):
        """ Create and return python script given antimony and phrasedml strings.

        :returns: python string to execute
        :rtype: str
        """
        rePath = r"(\w*).load\('(.*)'\)"
        reLoad = r"(\w*) = roadrunner.RoadRunner\(\)"
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        phrasedmllines = tePhrasedml.phrasedmlStr.splitlines()
        for k, line in enumerate(phrasedmllines):
            reSearchModel = re.split(reModel, line)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])
                modelname = os.path.basename(modelsource)
                modelname = str(modelname).replace(".xml", '')

        phrasedml.setReferencedSBML(modelsource, te.antimonyTosbml(tePhrasedml.antimonyStr))
        sedmlstr = phrasedml.convertString(tePhrasedml.phrasedmlStr)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())

        phrasedml.clearReferencedSBML()

        fd1, sedmlfilepath = tempfile.mkstemp()
        os.write(fd1, sedmlstr)

        pysedml = te.SedmlToRr.sedml_to_python(sedmlfilepath)
        if tePhrasedml.modelispath is False:
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

        outputstr = str(modelname) + " = '''" + tePhrasedml.antimonyStr + "'''\n\n" + pysedml

        os.close(fd1)
        os.remove(sedmlfilepath)

        return outputstr

    def printpython(self):
        """ Prints the created python string by :func:`createpython`. """
        execStr = self.createpython()
        print(execStr)

    def exportAsCombine(self, outputpath):
        """ Export as a combine archive.

        :param outputpath: full path of the combine zip file to create
        :type outputpath: str
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
        phrasedml.setReferencedSBML(modelname, te.antimonyTosbml(self.antimonyStr))
        combine.export(outputpath, self.antimonyStr, modelname, revphrasedml)
        phrasedml.clearReferencedSBML()

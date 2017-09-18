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

phrasedml provides a simple description language to create the key SED-ML components
    - models
    - simulations
    - tasks
    - outputs
"""
# TODO: handle multiple phrasedml files with multiple models
# TODO: implement general experiment which works with SEDML files, phrasedml files, SBML, URI, ...

from __future__ import print_function, division
import os.path
import shutil
import tempfile
import re
import warnings
from six import string_types, iteritems

import tellurium as te
import tellurium.tecombine as tecombine
import phrasedml
try:
    import tesedml as libsedml
except ImportError:
    import libsedml

from tellurium.sedml import tesedml


class experiment(object):
    """ Phrasedml experiment.

    Simulation experiments are defined and executed via the experiment class.

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
        # backwards compatibility & simplified syntax
        # for one phrasedml and antimony string
        if isinstance(antimonyList, string_types):
            antimonyList = [antimonyList]
        if isinstance(phrasedmlList, string_types):
            phrasedmlList = [phrasedmlList]

        modelispath = []
        for aStr in antimonyList:
            if not isinstance(aStr, string_types):
                raise IOError("invalid Antimony string/model path")
            if os.path.exists(aStr):
                modelispath.append(True)
            else:
                modelispath.append(False)

        self.modelispath = modelispath
        self.antimonyList = antimonyList
        self.phrasedmlList = phrasedmlList

    def getId(self):
        return self._experimentId()

    def _experimentId(self):
        """ Id is necessary to write the files and folders for the experiment.
        An experiment can contain multiples SBML and SED-ML files, so the model name
        is not sufficient.

        :return: id of the experiment
        :rtype: str
        """
        sources = self._modelsFromPhrasedml(self.phrasedmlList[0])
        names = sorted(sources.keys())
        return "_".join(names)

    def execute(self, selPhrasedml=None, workingDir=None):
        """ Executes the python code created for the given phrasedml string.

        The execution is performed in the workingDir. Combine archive files and
        outputs from the experiment are written in the workingDir.
        If no workingDir is provided a temporary workingDir is used which is
        removed after the experiment.

        :param selPhrasedml: Name of PhraSEDML string defined in the code
        :type selPhrasedml: str
        :param workingDir: working directory for execution
        :type workingDir: str
        """
        # create temporary working directory if no workingDir provided
        isTmpDir = False
        if workingDir is None:
            workingDir = tempfile.mkdtemp(suffix="_sedml")
            isTmpDir = True

        # This calls exec. Nothing bad should ever happen here !
        execStr = self._toPython(selPhrasedml, workingDir=workingDir)
        exec(execStr)

        # remove temporary workingDir
        if isTmpDir:
            shutil.rmtree(workingDir)

    def _toPython(self, phrasedmlStr, workingDir=None):
        """ Create and return python script given phrasedml string.
        
        :param phrasedmlStr: Name of PhraSEDML string defined in the code
        :type phrasedmlStr: str

        :returns: python string to execute
        :rtype: str
        """
        if phrasedmlStr is None:
            phrasedmlStr = self._getDefaultPhrasedml()

        # Models have to be resolved from phrasedml string and set as referenced
        phrasedml.clearReferencedSBML()
        self._setReferencedSBML(phrasedmlStr)

        # check if conversion is possible
        self._phrasedmlToSEDML(phrasedmlStr)

        # create temporary working directory
        import tempfile
        isTmpDir = False
        if workingDir is None:
            workingDir = tempfile.mkdtemp(suffix="_sedml")
            isTmpDir = True

        # Export archive
        expId = self.getId()
        expArchive = os.path.join(workingDir, "{}.omex".format(expId))
        self.exportAsCombine(expArchive)

        # Create python code from archive
        # This is the clean way to generate the code !
        pycode = tesedml.sedmlToPython(expArchive)

        # remove the temporary directory
        if isTmpDir:
            shutil.rmtree(workingDir)

        return pycode

    def printPython(self, phrasedmlStr=None):
        """ Prints the created python string by :func:`createpython`. 
        
        :param phrasedmlStr: Name of PhraSEDML string defined in the code
        :type phrasedmlStr: str
        """
        execStr = self.getPython(phrasedmlStr)
        print(execStr)

    def getPython(self, phrasedmlStr=None):
        """ Gets the created python string. """
        return self._toPython(phrasedmlStr)

    def exportAsCombine(self, outputPath, execute=False):
        """ Creates COMBINE archive for given antimony and phrasedml files.

        If execute=True all phrasedml are executed and the results written

        :param exportPath: full path of the combine zip file to create
        :type exportPath: str
        """

        # Create empty archive
        m = tecombine.CombineArchive()

        # Add antimony models to archive
        for aStr in self.antimonyList:
            r = te.loada(aStr)
            name = r.getModel().getModelName()
            m.addAntimonyStr(aStr, "{}.xml".format(name))

        # Add phrasedml models to archive
        for k, phrasedmlStr in enumerate(self.phrasedmlList):
            phrasedml.clearReferencedSBML()
            self._setReferencedSBML(phrasedmlStr)
            m.addPhraSEDMLStr(phrasedmlStr, self._phrasedmlFileName(k), master=True)
        phrasedml.clearReferencedSBML()

        # Add README.md to archive
        readmeStr = self.createReadmeString(outputPath)
        m.addStr(readmeStr, location='README.md', filetype='md')

        # add output files to archive
        if execute:
            for phrasedmlStr in self.phrasedmlList:
                # execute in temporary directory
                workingDir = tempfile.mkdtemp(suffix="_sedml")
                execStr = self._toPython(phrasedmlStr, workingDir=workingDir)
                exec(execStr)

                # Add output files to archive
                files = [f for f in os.listdir(workingDir)]

                for f in files:
                    filepath = os.path.join(workingDir, f)
                    if f.endswith('.xml'):
                        # SBML or SEDML resulting from antimony/phrasedml (already in archive)
                        pass
                    elif f.endswith('.md'):
                        # README.md (already in archive)
                        pass
                    elif f.endswith('.png'):
                        # outputPlot2D | outputPlot3D
                        m.addFile(filepath, filetype="png")
                    elif f.endswith('.csv'):
                        # outputReport
                        m.addFile(filepath, filetype="csv")
                    else:
                        warnings.warn('Unsupported file type not written in COMBINE archive: {}'.format(filepath))
                # remove temporary workingDir
                shutil.rmtree(workingDir)

        # Write archive
        m.write(outputPath)

    def exportAsCombineWithOutputs(self, outputPath):
        """ Combine archive with SED-ML outputs.

        All phrasedml files are run and the outputs added to the archive.

        :param exportPath: full path of the combine zip file to create
        :type exportPath: str
        """
        self.exportAsCombine(outputPath=outputPath, execute=True)


    def _getDefaultPhrasedml(self):
        """ Handling the case when no phrasedml string is supplied. """
        if len(self.phrasedmlList) > 0:
            selPhrasedml = self.phrasedmlList[0]
            warnings.warn("No phrasedml string selected, defaulting to first phrasedml.")
        else:
            raise IOError('No phrasedmlStr available.')
        return selPhrasedml

    def _phrasedmlToSEDML(self, phrasedmlStr):
        """ Convert phrasedml string to SEDML.

        Necessary to set the reference models via
            phrasedml.setReferencedSBML
        first.

        :param phrasedmlStr:
        :type phrasedmlStr:
        :return:
        :rtype:
        """
        sedmlstr = phrasedml.convertString(phrasedmlStr)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())
        return sedmlstr

    def _setReferencedSBML(self, phrasedmlStr):
        """ Set phrasedml referenced SBML for given phrasedml String. """
        modelNames = []
        for aStr in self.antimonyList:
            r = te.loada(aStr)
            name = r.getModel().getModelName()
            modelNames.append(name)

        sources = self._modelsFromPhrasedml(phrasedmlStr)
        for source, name in iteritems(sources):
            # not a antimony model
            if name not in modelNames:
                continue

            # set as referenced model
            aStr = self.antimonyList[modelNames.index(name)]
            phrasedml.setReferencedSBML(source, te.antimonyToSBML(aStr))

    @staticmethod
    def _modelsFromPhrasedml(phrasedmlStr):
        """ Find model sources and names in phrasedml file. """
        sources = {}

        # find model source, name
        reModel = r"""(\w+)\s*=\s*model\s*('|")(.*)('|")"""
        lines = phrasedmlStr.splitlines()
        for k, line in enumerate(lines):
            reSearchModel = re.split(reModel, line)
            if len(reSearchModel) > 1:
                source = str(reSearchModel[3])
                name = os.path.basename(source)
                name = str(name).replace(".xml", '')
                # add to source dictionary
                sources[source] = name

        return sources

    def _phrasedmlFileName(self, k):
        """ Name of SEDML-File in Combine Archive for k-th phrasedml."""
        return 'experiment{}.xml'.format(k+1)

    def createReadmeString(self, outputPath):
        """ README.md added to the archive.

        :return: readme information
        :rtype: str
        """
        readme = """
        # Tellurium {} experiment
        This COMBINE archive stores an tellurium experiment.
        http://tellurium.analogmachine.org/

        ## Run Experiment
        To reproduce the experiment and to create the figures and data run
        ```
        import tellurium as te
        omexPath = '{}'
        te.executeSEDML(omexPath)
        ```
        in tellurium, with `omexPath` the path to this archive file.
        """.format(te.getTelluriumVersion(),
                   os.path.basename(outputPath))
        return readme

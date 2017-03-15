from __future__ import print_function, division

import tecombine as libcombine
import phrasedml
import antimony
import tempfile
import shutil
import os
import tellurium as te

class inlineOmex:
    @classmethod
    def fromString(cls, omex_str):
        from .extractor import partitionInlineOMEXString
        sb,pml = partitionInlineOMEXString(omex_str)
        pml = '\n'.join(pml)
        return cls({'main.xml':pml},'main.xml',sb)

    def __init__(self, pmdict, master, sblist):
        '''Converts a dictionary of PhraSEDML files and list of Antimony files into sedml/sbml.

        :param pmdict: A dictionary containing the phrasedml keyed by the sedml file name
        :param master: The master sedml file
        :param sblist: A list of strings of Antimony sources'''

        self.master = master

        # Convert antimony to sbml
        self.sbmldict = {}
        for sb in sblist:
            r = antimony.loadAntimonyString(sb)
            if r < 0:
                raise RuntimeError('Failed to load Antimony model: {}'.format(antimony.getLastError()))
            modulename = antimony.getModuleNames()[-1]
            self.sbmldict[modulename] = antimony.getSBMLString(modulename)
            self.sbmldict[modulename]

        # Convert phrasedml to sedml
        self.sedmldict = {}
        for t in pmdict:
            for modulename in self.sbmldict:
                phrasedml.setReferencedSBML(modulename,self.sbmldict[modulename])
            phrasedml.convertString(pmdict[t])
            phrasedml.addDotXMLToModelSources()
            sedml = phrasedml.getLastSEDML()
            if sedml is None:
                raise RuntimeError('Unable to convert PhraSEDML to SED-ML: {}'.format(phrasedml.getLastError()))
            self.sedmldict[t] = sedml

    def writeFiles(self, dir):
        filenames = []
        for t in self.sedmldict:
            fname = os.path.join(dir,t)
            filenames.append(fname)
            with open(fname, 'w') as f:
                f.write(self.sedmldict[t])

        for t in self.sbmldict:
            fname = os.path.join(dir,t)+'.xml'
            filenames.append(fname)
            with open(fname, 'w') as f:
                f.write(self.sbmldict[t])
        return filenames

    def executeOmex(self):
        '''Executes this Omex instance.'''
        workingDir = tempfile.mkdtemp(suffix="_sedml")
        self.writeFiles(workingDir)
        from tellurium import executeSEDML
        executeSEDML(self.sedmldict[self.master], workingDir=workingDir)
        # shutil.rmtree(workingDir)

    def exportToCombine(self, outfile):
        '''Exports this Omex instance to a Combine archive.

        :param outfile: A path to the output file'''
        archive = libcombine.CombineArchive()
        description = libcombine.OmexDescription()
        description.setAbout('.') # about the archive itself
        desc = 'Description.'
        description.setDescription(desc)
        description.setCreated(libcombine.OmexDescription.getCurrentDateAndTime())

        # TODO: pass in creator
        creator = libcombine.VCard()
        creator.setFamilyName('Boi')
        creator.setGivenName('Dat')
        creator.setEmail('oh@sht.whaddup')
        creator.setOrganization('Denk')

        description.addCreator(creator)

        archive.addMetadata('.', description)

        # Write out to temporary files
        workingDir = tempfile.mkdtemp(suffix="_sedml")
        files = [] # Keep a list of files to remove
        for t in self.sedmldict:
            with open(os.path.join(workingDir,t),'w') as f:
                sedfile = f.name
                files.append(sedfile)
                f.write(self.sedmldict[t])
                archive.addFile(sedfile,t,libcombine.KnownFormats.lookupFormat("sedml"),t==self.master)

        for t in self.sbmldict:
            with open(os.path.join(workingDir,t+'.xml'),'w') as f:
                sbmlfile = f.name
                files.append(sbmlfile)
                f.write(self.sbmldict[t])
                archive.addFile(sbmlfile,t+'.xml',libcombine.KnownFormats.lookupFormat("sbml"))

        archive.writeToFile(outfile)

        for f in files:
            os.remove(f)

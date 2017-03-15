from __future__ import print_function, division

import os, re

from tecombine import CombineArchive
from .convert_phrasedml import phrasedmlImporter
from .convert_antimony import antimonyConverter
import shutil
import os

class OmexAsset:
    def getLocation(self):
        return self.location

    def getFileName(self):
        return os.path.split(self.getLocation())[-1]

    def getContent(self):
        return self.content

    def getMaster(self):
        return self.master

class SbmlAsset(OmexAsset):
    def __init__(self, location, content, master=False):
        self.location = location
        self.content = content
        self.master = master

    def getModuleName(self):
        return os.path.splitext(self.getFileName())[0]

class SedmlAsset(OmexAsset):
    def __init__(self, location, content, master=False):
        self.location = location
        self.content = content
        self.master = master

class Omex:
    ''' Wrapper for Combine archives. '''

    def __init__(self,
        about       = 'Format for storing dynamical models and simulations.', # about the archive itself
        description = 'No description.',
        creator     = None):

        self.about        = about
        self.description  = description
        self.creator      = creator

        self.sbml_assets  = []
        self.sedml_assets = []

    def addSbmlAsset(self, asset):
        self.sbml_assets.append(asset)

    def addSedmlAsset(self, asset):
        self.sedml_assets.append(asset)

    def getSbmlAssets(self):
        return self.sbml_assets

    def getSedmlAssets(self):
        return self.sedml_assets

    def writeFiles(self, dir):
        filenames = []
        for t in self.getSedmlAssets():
            fname = os.path.join(dir,t.getLocation())
            filenames.append(fname)
            with open(fname, 'w') as f:
                f.write(t.getContent())

        for t in self.getSbmlAssets():
            fname = os.path.join(dir,t.getLocation())
            filenames.append(fname)
            with open(fname, 'w') as f:
                f.write(t.getContent())
        return filenames

    def executeOmex(self):
        '''Executes this Omex instance.'''
        workingDir = tempfile.mkdtemp(suffix="_sedml")
        self.writeFiles(workingDir)
        from tellurium import executeSEDML
        for sedml_asset in self.getSedmlAssets():
            if sedml_asset.getMaster():
                executeSEDML(os.path.join(workingDir, sedml_asset.getLocation()),
                    workingDir=workingDir)
        # shutil.rmtree(workingDir)

    def exportToCombine(self, outfile):
        '''Exports this Omex instance to a Combine archive.

        :param outfile: A path to the output file'''
        archive = libcombine.CombineArchive()
        description = libcombine.OmexDescription()
        description.setAbout(self.about)
        description.setDescription(self.description)
        description.setCreated(libcombine.OmexDescription.getCurrentDateAndTime())

        # TODO: pass in creator
        if self.creator is not None:
            creator = libcombine.VCard()
            creator.setFamilyName(self.creator['last'])
            creator.setGivenName(self.creator['first'])
            creator.setEmail(self.creator['email'])
            creator.setOrganization(self.creator['organization'])
            description.addCreator(creator)

        archive.addMetadata('.', description)

        # Write out to temporary files
        # TODO: can add content via strings now
        workingDir = tempfile.mkdtemp(suffix="_sedml")
        files = [] # Keep a list of files to remove

        for t in self.getSedmlAssets():
            with open(os.path.join(workingDir,t.getLocation()),'w') as f:
                filepath = f.name
                files.append(filepath)
                f.write(t.getContent())
                archive.addFile(filepath, t.getLocation(), libcombine.KnownFormats.lookupFormat("sedml"), t.getMaster())

        for t in self.getSbmlAssets():
            with open(os.path.join(workingDir,t.getLocation()),'w') as f:
                filepath = f.name
                files.append(filepath)
                f.write(t.getContent())
                archive.addFile(filepath, t.getLocation(), libcombine.KnownFormats.lookupFormat("sbml"), t.getMaster())

        archive.writeToFile(outfile)

        for f in files:
            os.remove(f)

class inlineOmexImporter:
    # Set to false to disable "Converted from ...xml" comments
    __write_block_delimiter_comments = True

    @classmethod
    def fromFile(cls, path):
        """ Initialize from a file location.

        :param path: The path to the omex file
        """
        omex = CombineArchive()
        if not omex.initializeFromArchive(path):
            raise IOError('Could not read COMBINE archive.')
        return inlineOmexImporter(omex)

    def __init__(self, omex):
        """ Initialize from a CombineArchive instance
        (https://sbmlteam.github.io/libCombine/html/class_combine_archive.html).

        :param omex: A CombineArchive instance
        """
        self.omex = omex
        self.write_block_delimiter_comments = inlineOmexImporter.__write_block_delimiter_comments

        self.n_master_sedml = 0
        self.sedml_entries = []
        # match sedml, any level/ver
        self.sedml_fmt_expr = re.compile(r'^http[s]?://identifiers\.org/combine\.specifications/sed-ml.*$')

        self.sbml_entries = []
        # match sbml, any level/ver
        self.sbml_fmt_expr = re.compile(r'^http[s]?://identifiers\.org/combine\.specifications/sbml.*$')

        # Prevents %antimony and %phrasedml headers from
        # being written when all entries are in root of archive
        # and no sedml entries have master=False.
        self.headerless = True
        for entry in self.getEntries():
            # shouldn't happen
            if not entry.isSetLocation():
                raise RuntimeError('Entry has no location')
            if not self.isInRootDir(entry.getLocation()):
                # must write headers to specify entry paths
                self.headerless = False
            # count number of master sedml entries
            if self.sedml_fmt_expr.match(entry.getFormat()) != None:
                if entry.isSetMaster():
                    if entry.getMaster():
                        self.n_master_sedml += 1
                        if self.n_master_sedml > 1:
                            # must write headers to specify non-master sedml
                            self.headerless = False
                        self.sedml_entries.append(entry)
                    else:
                        # must write headers to specify non-master sedml
                        self.headerless = False
            elif self.sbml_fmt_expr.match(entry.getFormat()) != None:
                self.sbml_entries.append(entry)

    def getEntries(self):
        for k in range (self.omex.getNumEntries()):
            yield self.omex.getEntry(k)

    def isInRootDir(self, path):
        """ Returns true if path specififies a root location like ./file.ext."""
        d = os.path.split(path)[0]
        return d == '' or d =='.'

    def makeHeader(self, entry, type):
        """ Makes a header for an entry.

        :param entry: Entry in Combine archive (class CaContent)
        :param type: Can be 'sbml' or 'sedml'
        """
        header_map = {
            'sbml':  '%antimony',
            'sedml': '%phrasedml',
        }
        name_map = {
            'sbml':  'Antimony',
            'sedml': 'PhraSEDML',
        }
        try:
            header_start = header_map[type]
            block_source_name = name_map[type]
        except KeyError:
            raise KeyError('Filetype {} not understood by makeHeader', type)

        header = ''
        if not self.headerless:
            header += '{} {}'.format(header_start, entry.getLocation())
            if entry.isSetMaster() and entry.getMaster():
                header += ' --master=True'
            header += '\n'
        if self.write_block_delimiter_comments:
            header += '// -- Begin {} block converted from {}\n'.format(block_source_name, os.path.basename(entry.getLocation()))
        return header

    def makeFooter(self, entry, type):
        """ Makes a header for an entry.

        :param entry: Entry in Combine archive (class CaContent)
        :param type: Can be 'sbml' or 'sedml'
        """
        name_map = {
            'sbml':  'Antimony',
            'sedml': 'PhraSEDML',
        }
        try:
            block_source_name = name_map[type]
        except KeyError:
            raise KeyError('Filetype {} not understood by makeFooter', type)

        footer = ''
        if self.write_block_delimiter_comments:
            footer += '// -- End {} block\n\n'.format(block_source_name)
        return footer

    def normalizePath(self, path):
        return os.path.normpath(path)

    def formatPhrasedmlResource(self, path):
        """ Normalizes and also strips xml extension."""
        return self.normalizePath(path)
        # return os.path.splitext(self.normalizePath(path))[0]

    def makeSBMLResourceMap(self):
        result = {}
        for entry in self.sbml_entries:
            result[self.formatPhrasedmlResource(entry.getLocation())] = self.omex.extractEntryToString(entry.getLocation())
        return result

    def toInlineOmex(self):
        """ Converts a COMBINE archive into an inline phrasedml / antimony string.

        :returns: A string with the inline phrasedml / antimony source
        """
        output = ''

        # convert sbml entries to antimony
        for entry in self.sbml_entries:
            output += (self.makeHeader(entry, 'sbml') +
                antimonyConverter().sbmlToAntimony(self.omex.extractEntryToString(entry.getLocation()))[1].rstrip() + '\n'
                + self.makeFooter(entry, 'sbml'))
        # convert sedml entries to phrasedml
        for entry in self.sedml_entries:
            try:
                phrasedml_output = phrasedmlImporter.fromContent(
                    self.omex.extractEntryToString(entry.getLocation()).replace('BIOMD0000000012,xml','BIOMD0000000012.xml'),
                    self.makeSBMLResourceMap()
                    ).toPhrasedml().rstrip()
            except:
                raise RuntimeError('Could not read embedded SED-ML file {}.'.format(entry.getLocation()))
            output += (self.makeHeader(entry, 'sedml') +
                phrasedml_output + '\n'
                + self.makeFooter(entry, 'sedml'))

        return output.rstrip()

from __future__ import print_function, division

import os, re

from tecombine import CombineArchive
from .convert_phrasedml import phrasedmlImporter
from .convert_antimony import antimonyConverter

class omexImporter:
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
        return omexImporter(omex)

    def __init__(self, omex):
        """ Initialize from a CombineArchive instance
        (https://sbmlteam.github.io/libCombine/html/class_combine_archive.html).

        :param omex: A CombineArchive instance
        """
        self.omex = omex
        self.write_block_delimiter_comments = omexImporter.__write_block_delimiter_comments

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

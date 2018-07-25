"""
Class for working with omex files.
"""
from __future__ import print_function, division, absolute_import
import os
import re
import shutil
import tempfile
import json
import getpass


import imp  # reloads because numl is overwriting symbols
try:
    import tecombine as libcombine

except ImportError:
    import libcombine




from .convert_phrasedml import phrasedmlImporter
from .convert_antimony import antimonyConverter

class OmexFormatDetector:
    def __init__(self, omex):
        self.omex = omex
        # match sbml, any level/ver
        self.sbml_fmt_expr = re.compile(r'^http[s]?://identifiers\.org/combine\.specifications/sbml.*$')
        # match sedml, any level/ver
        self.sedml_fmt_expr = re.compile(r'^http[s]?://identifiers\.org/combine\.specifications/sed-ml.*$')

    def isSEDMLEntry(self, entry):
        return self.sedml_fmt_expr.match(entry.getFormat()) != None

    def isSBMLEntry(self, entry):
        """ Return true if this entry is SBML. """
        if self.sbml_fmt_expr.match(entry.getFormat()) != None:
            return True
        elif entry.getFormat() == 'application/xml':
            # try to guess if it is SBML
            content = self.omex.extractEntryToString(entry.getLocation())
            if content.startswith('<?xml') and '<sbml xmlns="http://www.sbml.org/sbml' in content:
                return True
            else:
                return False
        else:
            return False

def readCreator(file=None):
    from .. import getAppDir
    if file is None:
        file = os.path.join(getAppDir(), 'telocal', getpass.getuser() + '.vcard')
        if not os.path.exists(file) or not os.path.isfile(file):
            return None
    with open(file, 'rb') as f:
        return json.load(f)


class OmexAsset(object):
    def getLocation(self):
        return self.location

    def getFileName(self):
        return os.path.split(self.getLocation())[-1]

    def getContent(self):
        return self.content

    def getMaster(self):
        master = False
        if self.master is not None:
            master = self.master
        return master


class SbmlAsset(OmexAsset):
    def __init__(self, location, content, master=False):
        self.location = location
        self.content = content
        self.master = master

    def getModuleName(self):
        return os.path.splitext(self.getFileName())[0]

    def __repr__(self):
        return 'SbmlAsset(location={}, master={})'.format(self.getLocation(), self.getMaster())


class SedmlAsset(OmexAsset):
    def __init__(self, location, content, master=False):
        self.location = location
        self.content = content
        self.master = master

    def __repr__(self):
        return 'SedmlAsset(location={}, master={})'.format(self.getLocation(), self.getMaster())


class Omex(object):
    """ Wrapper for Combine archives. """
    def __init__(self,
                 description='',
                 creator=None):

        self.about = '.'
        self.description = description
        self.creator = creator

        self.sbml_assets = []
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
            fname = os.path.join(dir, os.path.normpath(t.getLocation()))
            dname = os.path.dirname(fname)
            if not os.path.exists(dname):
                os.makedirs(dname)
            filenames.append(fname)
            with open(fname, 'w') as f:
                f.write(t.getContent())

        for t in self.getSbmlAssets():
            fname = os.path.join(dir, os.path.normpath(t.getLocation()))
            dname = os.path.dirname(fname)
            if not os.path.exists(dname):
                os.makedirs(dname)
            filenames.append(fname)
            with open(fname, 'w') as f:
                f.write(t.getContent())
        return filenames

    def executeOmex(self):
        """ Executes this Omex instance.

        :return:
        """
        import phrasedml
        phrasedml.clearReferencedSBML()

        workingDir = tempfile.mkdtemp(suffix="_sedml")
        self.writeFiles(workingDir)
        from tellurium import executeSEDML
        for sedml_asset in self.getSedmlAssets():
            if sedml_asset.getMaster():
                sedml_path = os.path.join(workingDir, sedml_asset.getLocation())
                executeSEDML(sedml_path,
                             workingDir=os.path.dirname(sedml_path))
                # shutil.rmtree(workingDir)

    def exportToCombine(self, outfile):
        """ Export Omex instance as combine archive.

        :param outfile: A path to the output file"""
        import phrasedml
        phrasedml.clearReferencedSBML()

        archive = libcombine.CombineArchive()
        description = libcombine.OmexDescription()
        description.setAbout(self.about)
        description.setDescription(self.description)
        time_now = libcombine.OmexDescription.getCurrentDateAndTime()
        description.setCreated(time_now)

        # TODO: pass in creator
        if self.creator is not None:
            creator = libcombine.VCard()
            creator.setFamilyName(self.creator['last_name'])
            creator.setGivenName(self.creator['first_name'])
            creator.setEmail(self.creator['email'])
            creator.setOrganization(self.creator['organization'])
            description.addCreator(creator)

        archive.addMetadata('.', description)

        # Write out to temporary files
        # TODO: can add content via strings now
        workingDir = tempfile.mkdtemp(suffix="_sedml")
        files = []  # Keep a list of files to remove

        def addAssetToArchive(asset, format):
            """ Helper to add asset of given format. """
            fname = os.path.join(workingDir, os.path.normpath(asset.getLocation()))
            dname = os.path.dirname(fname)
            if not os.path.exists(dname):
                os.makedirs(dname)
            with open(fname, 'w') as f:
                files.append(fname)
                f.write(t.getContent())
                archive.addFile(fname,
                                asset.getLocation(),
                                libcombine.KnownFormats.lookupFormat(format),
                                asset.getMaster())

        try:
            for t in self.getSedmlAssets():
                addAssetToArchive(t, 'sedml')

            for t in self.getSbmlAssets():
                addAssetToArchive(t, 'sbml')

            archive.writeToFile(outfile)
        finally:
            # put this in finally to make sure files are removed even under Exception
            for f in files:
                os.remove(f)




class inlineOmexImporter:
    # Set to false to disable "Converted from ...xml" comments
    __write_block_delimiter_comments = True

    @classmethod
    def fromFile(cls, path):
        """ Initialize from a combine archive.

        :param path: The path to the omex file
        """
        if not os.path.isfile(path):
            raise IOError('No such file: {}'.format(path))

        d = None
        if not os.access(os.getcwd(), os.W_OK):
            d = os.getcwd()
            os.chdir(tempfile.gettempdir())

        omex = libcombine.CombineArchive()
        if not omex.initializeFromArchive(path):
            raise IOError('Could not read COMBINE archive.')
        importer = inlineOmexImporter(omex)

        # if d is not None:
            # os.chdir(d)
        return importer

    def __init__(self, omex):
        """ Initialize from a CombineArchive instance
        (https://sbmlteam.github.io/libCombine/html/class_combine_archive.html).

        :param omex: A CombineArchive instance
        """
        self.omex = omex
        self.write_block_delimiter_comments = inlineOmexImporter.__write_block_delimiter_comments

        self.n_master_sedml = 0
        self.sedml_entries = []
        self.sbml_entries = []
        detector = OmexFormatDetector(self.omex)

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
            if detector.isSEDMLEntry(entry):
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
            elif detector.isSBMLEntry(entry):
                self.sbml_entries.append(entry)
                # check whether the model id matches the file name - if it doesn't, we need headers
                module_name = antimonyConverter().sbmlToAntimony(self.omex.extractEntryToString(entry.getLocation()))[0]
                file_name_normalized = os.path.splitext(os.path.split(entry.getLocation())[-1])[0]
                if module_name != file_name_normalized:
                    self.headerless = False

        self.BioModHackRemoveDuplicates()

    def getEntries(self):
        for k in range(self.omex.getNumEntries()):
            yield self.omex.getEntry(k)

    def numEntries(self):
        return self.omex.getNumEntries()

    def numSBMLEntries(self):
        return len(self.sbml_entries)

    def containsSBMLOnly(self):
        """ Return true if this is a SBML-only archive (no SED-ML). """
        if len(self.sbml_entries) > 0 and len(self.sedml_entries) == 0:
            return True
        else:
            return False

    def BioModHackRemoveDuplicates(self):
        """ A hack to remove duplicates (urn/url) in BioModels archives. """
        if len(self.sbml_entries) == 2:
            n_urn = 0
            n_url = 0
            for entry in self.sbml_entries:
                if '_urn.xml' in entry.getLocation():
                    n_urn += 1
                if '_url.xml' in entry.getLocation():
                    n_url += 1
            if n_urn == 1 and n_url == 1:
                del self.sbml_entries[-1]

    def isInRootDir(self, path):
        """ Returns true if path specififies a root location like ./file.ext."""
        d = os.path.split(path)[0]
        return d == '' or d == '.'

    def makeHeader(self, entry, type):
        """ Makes a header for an entry.

        :param entry: Entry in Combine archive (class CaContent)
        :param type: Can be 'sbml' or 'sedml'
        """
        header_map = {
            'sbml': '%model',
            'sedml': '%tasks',
        }
        name_map = {
            'sbml': 'Antimony',
            'sedml': 'PhraSEDML',
        }
        try:
            header_start = header_map[type]
            block_source_name = name_map[type]
        except KeyError:
            raise KeyError('Filetype {} not understood by makeHeader', type)

        header = ''
        if not self.headerless:
            header += '{} {}'.format(header_start, self.fixExt(entry.getLocation()))
            if entry.isSetMaster() and entry.getMaster():
                header += ' --master=True'
            header += '\n'
        if self.write_block_delimiter_comments:
            header += '// -- Begin {} block converted from {}\n'.format(block_source_name,
                                                                        os.path.basename(entry.getLocation()))
        return header

    def makeFooter(self, entry, type):
        """ Makes a header for an entry.

        :param entry: Entry in Combine archive (class CaContent)
        :param type: Can be 'sbml' or 'sedml'
        """
        name_map = {
            'sbml': 'Antimony',
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

    def fixExt(self, path):
        """ Ensures all extensions are .xml."""
        p = os.path.splitext(path)[0]
        return ''.join([p, '.xml'])

    def fixSep(self, path):
        """ Converts Windows-style separators to Unix separators."""
        if os.path.sep == '\\':
            return path.replace(os.path.sep, '/')
        else:
            return path

    def formatPhrasedmlResource(self, path):
        """ Normalizes path, strips xml extension, and normalizes fs separator."""
        return self.fixSep(self.normalizePath(path))
        # return os.path.splitext(self.normalizePath(path))[0]

    def makeSBMLResourceMap(self, relative_to=None):
        result = {}
        for entry in self.sbml_entries:
            if relative_to is None:
                relpath = entry.getLocation()
            else:
                relpath = self.fixSep(os.path.relpath(entry.getLocation(), relative_to))
            result[self.formatPhrasedmlResource(relpath)] = self.omex.extractEntryToString(entry.getLocation())
        return result

    def toInlineOmex(self, detailedErrors=True):
        """ Converts a COMBINE archive into an inline phrasedml / antimony string.

        :returns: A string with the inline phrasedml / antimony source
        """
        output = ''

        # try to read the author information
        desc = self.omex.getMetadataForLocation('.')
        if desc and desc.getNumCreators() > 0:
            # just get first one
            vcard = desc.getCreator(0)
            output += '// Archive author information:\n'
            first_name = vcard.getGivenName()
            last_name = vcard.getFamilyName()
            name = ' '.join([first_name, last_name])
            email = vcard.getEmail()
            org = vcard.getOrganization()

            if name:
                output += '// - Name: {}\n'.format(name.replace('\n', ' ').replace('\r', ''))
            if email:
                output += '// - Email: {}\n'.format(email.replace('\n', ' ').replace('\r', ''))
            if org:
                output += '// - Organization: {}\n'.format(org.replace('\n', ' ').replace('\r', ''))

        # convert sbml entries to antimony
        for entry in self.sbml_entries:
            output += (self.makeHeader(entry, 'sbml') +
                       antimonyConverter().sbmlToAntimony(self.omex.extractEntryToString(entry.getLocation()))[
                           1].rstrip() + '\n'
                       + self.makeFooter(entry, 'sbml'))
        # convert sedml entries to phrasedml
        for entry in self.sedml_entries:
            sedml_str = self.omex.extractEntryToString(entry.getLocation()).replace('BIOMD0000000012,xml',
                                                                                    'BIOMD0000000012.xml')
            try:
                phrasedml_output = phrasedmlImporter.fromContent(
                    sedml_str,
                    self.makeSBMLResourceMap(self.fixSep(os.path.dirname(entry.getLocation())))
                ).toPhrasedml().rstrip().replace('compartment', 'compartment_')
            except Exception as e:
                errmsg = 'Could not read embedded SED-ML file {}.'.format(entry.getLocation())
                try:
                    import tesedml
                    s = tesedml.readSedMLFromString(sedml_str)
                    if s.getNumErrors() > 0:
                        if detailedErrors:
                            for k in range(s.getNumErrors()):
                                errmsg += 'Error {}:\n{}'.format(k + 1, s.getError(k).getMessage())
                        else:
                            errmsg += ' Run te.convertCombineArchive for more info.'
                    else:
                        errmsg += ' Not supported by PhraSEDML.'
                except Exception as e:
                    if detailedErrors:
                        errmsg += ' '+str(e)
                    else:
                        errmsg += ' Invalid SED-ML.'
                raise RuntimeError(errmsg)
            output += (self.makeHeader(entry, 'sedml') +
                       phrasedml_output + '\n'
                       + self.makeFooter(entry, 'sedml'))

        return output.rstrip()

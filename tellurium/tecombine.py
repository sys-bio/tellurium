"""
Utilities for working with combine archives.
"""
from __future__ import print_function, division

import os
from os.path import exists, isfile, basename
import warnings
import zipfile
import phrasedml
import antimony
import re


class CombineTools(object):
    """ Helper functions to work with combine archives."""

    @staticmethod
    def extractArchive(archivePath, directory):
        """ Extracts given archive into the target directory.

        Target directory is created if it does not exist.
        Files are overwritten in the directory !

        :param archivePath: path to combine archive
        :type archivePath: str
        :param directory: path to directory where to extract to
        :type directory:
        :return:
        :rtype:
        """
        zip = zipfile.ZipFile(archivePath, 'r')

        if not os.path.isdir(directory):
            os.makedirs(directory)
        else:
            warnings.warn("Combine archive directory already exists:{}".format(directory))

        for each in zip.namelist():
            # check if the item includes a subdirectory
            # if it does, create the subdirectory in the output folder and write the file
            # otherwise, just write the file to the output folder
            if not each.endswith('/'):
                root, name = os.path.split(each)
                directory = os.path.normpath(os.path.join(directory, root))
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                file(os.path.join(directory, name), 'wb').write(zip.read(each))
        zip.close()

    @staticmethod
    def filePathsFromExtractedArchive(directory, formatType='sed-ml'):
        """ Reads file paths from extracted combine archive.

        Searches the manifest.xml of the archive for files of the
        specified formatType and checks if the files exist in the directory.

        Supported formatTypes are:
            'sed-ml' : SED-ML files
            'sbml' : SBML files

        :param directory: directory of extracted archive
        :return: list of paths
        :rtype: list
        """
        filePaths = []

        manifest = os.path.join(directory, "manifest.xml")
        if os.path.exists(manifest):
            # get the sedml files from the manifest
            import xml.etree.ElementTree as et
            tree = et.parse(manifest)
            root = tree.getroot()
            print(root)
            for child in root:
                format = child.attrib['format']
                if format.endswith(formatType):
                    location = child.attrib['location']

                    # real path
                    fpath = os.path.join(directory, location)
                    if not os.path.exists(fpath):
                        raise IOError('Path specified in manifest.xml does not exist in archive: {}'.format(fpath))
                    filePaths.append(fpath)
        else:
            # no manifest (use all sedml files in folder)
            warnings.warn("No 'manifest.xml' in archive, using all '*.sedml' files.")
            for fname in os.listdir(directory):
                if fname.endswith(".sedml") or fname.endswith(".sedx.xml"):
                    filePaths.append(os.path.join(directory, fname))

        return filePaths


class CombineAsset(object):
    @classmethod
    def getCOMBINEResourceURI(cls, x):
        """ Get URI for uri type."

        :param x: uri type (either 'sbml' or 'sed-ml')
        :type x: str
        :return: uri of the combine specification
        :rtype: str
        """
        types = {
            'sbml': 'http://identifiers.org/combine.specifications/sbml',
            'sed-ml': 'http://identifiers.org/combine.specifications/sed-ml'
        }
        return types[x]

    def isPhraSEDML(self):
        return False

# Raw/file assets:
# File assets specify a file path in the OS filesystem
# Raw assets contain the raw string of the entire asset

class CombineRawAsset(CombineAsset):
    def __init__(self, raw, archname):
        self.raw = raw
        self.archname = archname

    def isFile(self):
        return False

    def getArchName(self):
        return self.archname

    def getRawStr(self):
        return self.raw

    # return a form suitable for exporting to COMBINE (uses dynamic binding)
    def getExportedStr(self):
        return self.getRawStr()


class CombineFileAsset(CombineAsset):
    def __init__(self, filename):
        self.filename = filename

    def isFile(self):
        return True

    def getbasename(self, f):
        return basename(f)

    def getFileName(self):
        return self.filename

    def getArchName(self, f):
        return self.getbasename(f)

    def getRawStr(self):
        with open(self.getFileName()) as f:
            return f.read()

    def getExportedStr(self):
        return self.getRawStr()

# Asset types: SBML, SEDML, etc.

class CombineSBMLAsset(CombineAsset):
    def getResourceURI(self):
        return CombineAsset.getCOMBINEResourceURI('sbml')


class CombineAntimonyAsset(CombineAsset):
    def getSBMLStr(self):
        antimony.clearPreviousLoads()
        antimony.loadString(self.getRawStr())
        return antimony.getSBMLString(antimony.getModuleNames()[-1])

    def getResourceURI(self):
        return CombineAsset.getCOMBINEResourceURI('sbml')


class CombineSEDMLAsset(CombineAsset):
    def getResourceURI(self):
        return CombineAsset.getCOMBINEResourceURI('sed-ml')


class CombinePhraSEDMLAsset(CombineAsset):
    def isPhraSEDML(self):
        return True

    def getSEDMLStr(self):
        sedmlstr = phrasedml.convertString(self.getRawStr())
        if sedmlstr == None:
            raise Exception(phrasedml.getLastError())
        return sedmlstr

    def getResourceURI(self):
        return CombineAsset.getCOMBINEResourceURI('sed-ml')

# SBML:

class CombineSBMLRawAsset(CombineRawAsset, CombineSBMLAsset):
    pass

class CombineSBMLFileAsset(CombineFileAsset, CombineSBMLAsset):
    pass

# Antimony:

class CombineAntimonyRawAsset(CombineRawAsset, CombineAntimonyAsset):
    # return SBML, since COMBINE doesn't support Antimony
    def getExportedStr(self):
        return self.getSBMLStr()

class CombineAntimonyFileAsset(CombineFileAsset, CombineAntimonyAsset):
    # converts a phrasedml extension to a sedml extension
    def replace_ext(self, filename):
        r = re.compile(r'.*\.([^.]*)')
        m = r.match(filename)
        if m is None:
            raise RuntimeError('Unrecognized file name: {}'.format(filename))
        return filename.replace(m.groups()[0], 'xml')

    def getArchName(self, f):
        return self.replace_ext(self.getbasename(f))

    # return SEDML, since COMBINE doesn't support PhraSEDML
    def getExportedStr(self):
        return self.getSBMLStr()

# SEDML:

class CombineSEDMLRawAsset(CombineRawAsset, CombineSEDMLAsset):
    pass

class CombineSEDMLFileAsset(CombineFileAsset, CombineSEDMLAsset):
    pass

# PhraSEDML:


class CombinePhraSEDMLRawAsset(CombineRawAsset,   CombinePhraSEDMLAsset):
    # return SEDML, since COMBINE doesn't support PhraSEDML
    def getExportedStr(self):
        return self.getSEDMLStr()


class CombinePhraSEDMLFileAsset(CombineFileAsset, CombinePhraSEDMLAsset):
    # converts a phrasedml extension to a sedml extension
    def replace_pml_ext(self, filename):
        r = re.compile(r'.*\.([^.]*)')
        m = r.match(filename)
        if m is None:
            raise RuntimeError('Unrecognized file name: {}'.format(filename))
        return filename.replace(m.groups()[0], 'xml')

    def getArchName(self, f):
        return self.replace_pml_ext(self.getbasename(f))

    # return SEDML, since COMBINE doesn't support PhraSEDML
    def getExportedStr(self):
        return self.getSEDMLStr()


class MakeCombine:
    def __init__(self):
        self.assets = []

    def checkfile(self, filename):
        if not exists(filename) or not isfile(filename):
            raise RuntimeError('No such file: {}'.format(filename))

    # Add raw strings:
    def addSBMLStr(self, rawstr, archname):
        self.assets.append(CombineSBMLRawAsset(rawstr, archname))

    def addAntimonyStr(self, rawstr, archname):
        self.assets.append(CombineAntimonyRawAsset(rawstr, archname))

    def addSEDMLStr(self, rawstr, archname):
        self.assets.append(CombineSEDMLRawAsset(rawstr, archname))

    def addPhraSEDMLStr(self, rawstr, archname):
        self.assets.append(CombinePhraSEDMLRawAsset(rawstr, archname))

    # Add files:
    def addSBMLFile(self, filename):
        self.checkfile(filename)
        self.assets.append(CombineSBMLFileAsset(filename))

    def addAntimonyFile(self, filename):
        self.checkfile(filename)
        self.assets.append(CombineAntimonyFileAsset(filename))

    def addSEDMLFile(self, filename):
        self.checkfile(filename)
        self.assets.append(CombineSEDMLFileAsset(filename))

    def addPhraSEDMLFile(self, filename):
        self.checkfile(filename)
        self.assets.append(CombinePhraSEDMLFileAsset(filename))

    def writeAsset(self, zipfile, asset):
        if asset.isFile():
            zipfile.write(asset.getFileName(), asset.getArchName())
        else:
            zipfile.writestr(asset.getArchName(), asset.getExportedStr())

        self.manifest += '    <content location="./{}" master="true" format="{}"/>\n'.format(
            asset.getArchName(),
            asset.getResourceURI()
            )

    def write(self, outfile):
        self.manifest = ''
        with zipfile.ZipFile(outfile, 'w') as z:
            self.manifest += '<?xml version="1.0"  encoding="utf-8"?>\n<omexManifest  xmlns="http://identifiers.org/combine.specifications/omex-manifest">\n'
            self.manifest += '    <content location="./manifest.xml" format="http://identifiers.org/combine.specifications/omex-manifest"/>\n'

            for a in self.assets:
                self.writeAsset(z, a)

            self.manifest += '</omexManifest>\n'

            z.writestr('manifest.xml', self.manifest)


def export(outfile, antimonyStr, SBMLName, *args):
    m = MakeCombine()

    m.addAntimonyStr(antimonyStr, SBMLName)

    # remaining arguments are assumed to be phrasedml
    n = 1
    for phrasedmlStr in args:
        m.addPhraSEDMLStr(phrasedmlStr, 'experiment{}.xml'.format(n))
        n += 1

    m.write(outfile)

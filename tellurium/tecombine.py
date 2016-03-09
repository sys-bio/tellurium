"""
Tellurium utilities for working with COMBINE archives.

Open Modeling EXchange format (OMEX) is the basis of the COMBINE Archive, a single file that supports
the exchange of all the information necessary for a modeling and simulation experiment in biology.
An OMEX file is a ZIP container that includes a manifest file, listing the content of the archive,
an optional metadata file adding information about the archive and its content, and the files describing
the model. The content of a COMBINE Archive consists of files encoded in COMBINE standards whenever
possible, but may include additional files defined by an Internet Media Type.

The COMBINE Archive facilitates the reproduction of modeling and simulation experiments in biology by
embedding all the relevant information in one file. Having all the information stored and exchanged at
once also helps in building activity logs and audit trails.

The COMBINE archive is described in the following publication
BMC Bioinformatics. 2014 Dec 14;15:369. doi: 10.1186/s12859-014-0369-z.
COMBINE archive and OMEX format: one file to share all information to reproduce a modeling project.

The specification is available from
http://co.mbine.org/specifications/omex.version-1

The archive contains
1. a mandatory manifest file, called manifest.xml, always located at the root of the archive, that describes the
location and the type of each data file contained in the archive plus an entry describing the archive itself.
The location of those files is defined by a relative path.

2. metadata files containing clerical information about the various files contained in the archive, and the archive
itself. A best practice is to include only one file for each file format metadata called metadata.* (where *
means the suitable file extension)

3. all remaining files necessary to the model and simulation project
"""
# TODO: MakeCombine should support the storage of data, figures, csv tables, ...
# required for a CombineWithResults


from __future__ import print_function, division

import os
import warnings
from zipfile import ZipFile
import phrasedml
import antimony
import re
import tellurium as te
import roadrunner
from xml.etree import ElementTree as et
import libsedml


def combine(combinePath):
    """ Open a combine archive from local directory.

    :param combinePath: Path to a combine archive
    :type combinePath: str
    :returns: OpenCombine instance
    """
    return OpenCombine(combinePath)


# Assets --------------------------------------------------------
class Asset(object):
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


class RawAsset(Asset):
    """ Raw assets contain the raw string of the entire asset. """
    def __init__(self, raw, archname):
        self.raw = raw
        self.archname = archname

    def isFile(self):
        return False

    def getArchName(self):
        return self.archname

    def getRawStr(self):
        return self.raw

    def getExportedStr(self):
        """ Returns a form suitable for exporting to COMBINE (uses dynamic binding)
        :return:
        :rtype:
        """
        return self.getRawStr()


class FileAsset(Asset):
    """ File assets specify a file path in the file system. """
    def __init__(self, filename):
        self.filename = filename

    def isFile(self):
        return True

    def getFileName(self):
        return self.filename

    def getArchName(self, f):
        return self.getBasename(f)

    def getBasename(self, f):
        return os.path.basename(f)

    def getRawStr(self):
        with open(self.getFileName()) as f:
            return f.read()

    def getExportedStr(self):
        return self.getRawStr()


# SBML --------------------------------------------------------
class SBMLAsset(Asset):
    """ SBML. """
    def getResourceURI(self):
        return Asset.getCOMBINEResourceURI('sbml')

class SBMLRawAsset(RawAsset, SBMLAsset):
    """ SBML raw asset. """
    pass

class SBMLFileAsset(FileAsset, SBMLAsset):
    """ SBML file asset. """
    pass


# SED-ML --------------------------------------------------------
class SEDMLAsset(Asset):
    def getResourceURI(self):
        return Asset.getCOMBINEResourceURI('sed-ml')

class SEDMLRawAsset(RawAsset, SEDMLAsset):
    pass

class SEDMLFileAsset(FileAsset, SEDMLAsset):
    pass


# Antimony --------------------------------------------------------
class AntimonyAsset(Asset):
    """ Antimony. """
    def getSBMLStr(self):
        antimony.clearPreviousLoads()
        antimony.loadString(self.getRawStr())
        return antimony.getSBMLString(antimony.getModuleNames()[-1])

    def getResourceURI(self):
        return Asset.getCOMBINEResourceURI('sbml')

class AntimonyRawAsset(RawAsset, AntimonyAsset):
    """ Antimony Raw. """
    def getExportedStr(self):
        """ return SBML, since COMBINE doesn't support Antimony."""
        return self.getSBMLStr()

class AntimonyFileAsset(FileAsset, AntimonyAsset):

    def getArchName(self, f):
        return self._replace_ext(self.getBasename(f))

    def getExportedStr(self):
        """ Returns SEDML, since COMBINE doesn't support PhraSEDML. """
        return self.getSBMLStr()

    def _replace_ext(self, filename):
        """ Converts a phrasedml extension to a sedml extension.
        :param filename:
        :type filename:
        :return:
        :rtype:
        """
        r = re.compile(r'.*\.([^.]*)')
        m = r.match(filename)
        if m is None:
            raise RuntimeError('Unrecognized file name: {}'.format(filename))
        return filename.replace(m.groups()[0], 'xml')


# PhrasedML --------------------------------------------------------
class PhraSEDMLAsset(Asset):
    def isPhraSEDML(self):
        return True

    def getSEDMLStr(self):
        # FIXME: This will create problems, because the referenced models can change since the Asset was created
        # There should only be SEDML and SBML assets, i.e on creation of PhrasedMlAssets and AntimonyAssets these
        # should be translated.
        sedmlstr = phrasedml.convertString(self.getRawStr())
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())
        return sedmlstr

    def getResourceURI(self):
        return Asset.getCOMBINEResourceURI('sed-ml')


class PhraSEDMLRawAsset(RawAsset, PhraSEDMLAsset):
    def getExportedStr(self):
        """ Returns SEDML, since COMBINE doesn't support PhraSEDML. """
        # FIXME: Necessary to add .xml to models due to https://sourceforge.net/p/phrasedml/tickets/15/
        return self.getSEDMLStr()


class PhraSEDMLFileAsset(FileAsset, PhraSEDMLAsset):
    def getArchName(self, f):
        return self._replace_pml_ext(self.getBasename(f))

    def _replace_pml_ext(self, filename):
        """ Converts a phrasedml extension to a sedml extension. """
        r = re.compile(r'.*\.([^.]*)')
        m = r.match(filename)
        if m is None:
            raise RuntimeError('Unrecognized file name: {}'.format(filename))
        return filename.replace(m.groups()[0], 'xml')

    def getExportedStr(self):
        """ Returns SEDML, since COMBINE doesn't support PhraSEDML."""
        return self.getSEDMLStr()


class MakeCombine:
    """ Class for creating combine archives.

    Raw and file assets are added to the empty COMBINE archive via
    the respective add*Str and add*File methods.
    The archive is written to file via the write function.
    """
    def __init__(self):
        self.assets = []
        self.manifest = ''

    def checkfile(self, filename):
        """ Check that file exists. """
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise RuntimeError('No such file: {}'.format(filename))

    # Add raw strings
    def addSBMLStr(self, rawstr, archname):
        self.assets.append(SBMLRawAsset(rawstr, archname))

    def addAntimonyStr(self, rawstr, archname):
        self.assets.append(AntimonyRawAsset(rawstr, archname))

    def addSEDMLStr(self, rawstr, archname):
        self.assets.append(SEDMLRawAsset(rawstr, archname))

    def addPhraSEDMLStr(self, rawstr, archname):
        self.assets.append(PhraSEDMLRawAsset(rawstr, archname))

    # Add files
    def addSBMLFile(self, filename):
        self.checkfile(filename)
        self.assets.append(SBMLFileAsset(filename))

    def addAntimonyFile(self, filename):
        self.checkfile(filename)
        self.assets.append(AntimonyFileAsset(filename))

    def addSEDMLFile(self, filename):
        self.checkfile(filename)
        self.assets.append(SEDMLFileAsset(filename))

    def addPhraSEDMLFile(self, filename):
        self.checkfile(filename)
        self.assets.append(PhraSEDMLFileAsset(filename))

    def write(self, outfile):
        """ Write the combine archive to the outfile.
        Writes all assets and creates the manifest.xml.
        """
        with ZipFile(outfile, 'w') as zf:
            self.manifest += '<?xml version="1.0"  encoding="utf-8"?>\n<omexManifest  xmlns="http://identifiers.org/combine.specifications/omex-manifest">\n'
            self.manifest += '    <content location="./manifest.xml" format="http://identifiers.org/combine.specifications/omex-manifest"/>\n'
            for a in self.assets:
                self._writeAsset(zf, a)
            self.manifest += '</omexManifest>\n'
            # write manifest
            zf.writestr('manifest.xml', self.manifest)

    def _writeAsset(self, zf, asset):
        """ Writes asset to zip file (archive) and adds the manifest line for the file. """
        if asset.isFile():
            zf.write(asset.getFileName(), asset.getArchName())
        else:
            zf.writestr(asset.getArchName(), asset.getExportedStr())

        self.manifest += '    <content location="./{}" master="true" format="{}"/>\n'.format(
            asset.getArchName(),
            asset.getResourceURI()
        )


class OpenCombine(object):

    def __init__(self, combinePath):
        if os.path.exists(combinePath):
            self.combinePath = combinePath
        else:
            raise Exception("Invalid path for combine archive")
    
    def addSBML(self, sbmlPath):
        modelname = self.getModelName(sbmlPath)
        contents = self.listContents()
        zf = ZipFile(self.combinePath, 'a')
        if os.path.exists(sbmlPath):
            numSame = 0
            while contents.count(modelname + '.xml') == 1:
                modelname = modelname + '_' + str(numSame)
                numSame += 1
            zf.write(sbmlPath, arcname=modelname + '.xml')
        elif sbmlPath.startswith(r'<?xml'):
            numSame = 0
            while contents.count(modelname + '.xml') == 1:
                modelname = modelname + '_' + str(numSame)
                numSame += 1
            zf.writestr(modelname + '.xml', sbmlPath)
        else:
            raise Exception("Invalid string for sbml: Check the path of the file")
        zf.close()
        self.updateManifest(modelname + '.xml', 'sbml')


    def addAntimony(self, antimonyStr):
        """ Add antimony to archive. """
        sbmlStr = te.antimonyToSBML(antimonyStr)
        self.addSBML(sbmlStr)


    def addSEDML(self, sedmlPath, arcname=None):
        contents = self.listContents()
        sedmlBase = os.path.basename(sedmlPath)
        try:
            arcname, arcFormat = os.path.splitext(arcname)
        except AttributeError:
            pass
        zf = ZipFile(self.combinePath, 'a')
        if os.path.exists(sedmlPath):
            if arcname == None:
                sedmlname, sedmlFormat = os.path.splitext(sedmlBase)
                numSame = 0
                while contents.count(sedmlname + '.xml') == 1:
                    sedmlname = sedmlname + '_' + str(numSame)
                    numSame += 1
                zf.write(sedmlPath, arcname=sedmlname + '.xml')
            else:
                if arcname + '.xml' in contents:
                    raise Exception('Combine archive contains a file with the same name. Please try different name.')
                else:
                    zf.write(sedmlPath, arcname=arcname + '.xml')
        elif sedmlPath.startswith(r'<?xml'):
            if arcname == None:
                raise Exception("Name of sedml file not defined.")
            else:
                if arcname + '.xml' in contents:
                    raise Exception('Combine archive contains a file with the same name. Please try different name.')
                else:
                    zf.writestr(arcname + '.xml', sedmlPath)
        else:
            raise Exception("Invalid string for sbml: Check the path of the file")
        zf.close()
        if arcname == None:
            self.updateManifest(sedmlname + '.xml', 'sedml')
        else:
            self.updateManifest(arcname + '.xml', 'sedml')
    
    def addPhrasedml(self, phrasedmlStr, antimonyStr, arcname=None):
        """ Adds phrasedml via conversion to SEDML. """
        # FIXME: This does not work for multiple referenced models !.
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        phrasedmllines = phrasedmlStr.splitlines()
        for k, line in enumerate(phrasedmllines):
            reSearchModel = re.split(reModel, line)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])
                modelname = os.path.basename(modelsource)
                modelname = str(modelname).replace(".xml", '')

        phrasedml.setReferencedSBML(modelsource, te.antimonyToSBML(antimonyStr))
        sedmlstr = phrasedml.convertString(phrasedmlStr)
        if sedmlstr is None:
            raise Exception(phrasedml.getLastError())

        phrasedml.clearReferencedSBML()
        self.addSEDML(sedmlstr, arcname)
        
    def addFile(self, filePath):
        """ Add other file type. """
        acceptedFormats = ('png','jpg','jpeg','pdf','txt','csv','dat')
        contents = self.listContents()
        fileBase = os.path.basename(filePath)
        fileName, fileFormat = os.path.splitext(fileBase)
        zf = ZipFile(self.combinePath, 'a')
        if os.path.exists(filePath):
            if filePath.lower().endswith(acceptedFormats):
                if filePath.lower().endswith(('png', 'jpg', 'jpeg')):
                    numSame = 0
                    while contents.count("fig/" + fileName + fileFormat) == 1:
                        fileName = fileName + '_' + str(numSame)
                        numSame += 1
                    zf.write(filePath, arcname="fig/" + fileName + fileFormat)
                if filePath.lower().endswith(('pdf', 'txt', 'csv', 'dat')):
                    numSame = 0
                    while contents.count("data/" + fileName + fileFormat) == 1:
                        fileName = fileName + '_' + str(numSame)
                        numSame += 1
                    zf.write(filePath, arcname="data/" + fileName + fileFormat)
            else:
                raise Exception("Unsupported file format")
        else:
            raise Exception("Cannot find the file")
        zf.close()
        self.updateManifest(fileName + fileFormat, fileFormat[1:])
    
    def getModelName(self, sbmlfile):
        r = roadrunner.RoadRunner(sbmlfile)
        return r.getModel().getModelName()
        
    def getSBML(self, sbmlfile):
        zf = ZipFile(self.combinePath, 'r')
        sbmlStr = zf.read(sbmlfile)
        zf.close()
        print(sbmlStr)
        return sbmlStr
        
    def getSBMLAsAntimony(self, sbmlfile):
        zf = ZipFile(self.combinePath, 'r')
        sbmlStr = zf.read(sbmlfile)
        zf.close()
        antStr = te.sbmlToAntimony(sbmlStr)
        print(antStr)
        return antStr

    def getSEDML(self, sedmlfile):
        zf = ZipFile(self.combinePath, 'r')
        sedmlStr = zf.read(sedmlfile)
        zf.close()
        print(sedmlStr)
        return sedmlStr
        
    def getSEDMLAsPhrasedml(self, sedmlfile):
        zf = ZipFile(self.combinePath, 'r')
        sedmlStr = zf.read(sedmlfile)
        zf.close()
        phrasedmlStr = phrasedml.convertString(sedmlStr)
        print(phrasedmlStr)
        return phrasedmlStr        
        
    def listContents(self):
        zf = ZipFile(self.combinePath, 'r')
        temp = zf.namelist()
        print(zf.namelist())
        zf.close()
        return temp
        
    def listDetailedContents(self):
        """ List contents of the archive from the manifest.xml

        :return: contentList of dictionaries with keys: filename, type
        :rtype: [{}]
        """
        contents = []
        man = self.readManifest()
        xml = et.ElementTree(et.fromstring(man))
        root = xml.getroot()
        for child in root:
            # get content for xml element
            content = None
            attribute = child.attrib
            formtype = attribute.get('format')
            loc = attribute.get('location')
            # sbml
            if formtype == "http://identifiers.org/combine.specifications/sbml":
                if loc.startswith('http') or loc.startswith('www'):
                    content = {'filename': loc, 'type': 'sbml'}
                else:
                    content = {'filename': os.path.basename(loc), 'type': 'sbml'}
            # sedml
            elif formtype == "http://identifiers.org/combine.specifications/sed-ml":
                zf = ZipFile(self.combinePath, 'r')
                try:
                    sedmlRaw = zf.read(loc)
                except KeyError as e:
                    try:
                        sedmlRaw = zf.read(os.path.basename(loc))
                    except KeyError as e:
                        raise e
                sedmlDoc = libsedml.readSedMLFromString(sedmlRaw)
                tempSedmlSource = []
                for model in sedmlDoc.getListOfModels():
                    if os.path.splitext(os.path.basename(model.getSource()))[1] == '':
                        pass
                    else:
                        tempSedmlSource.append(os.path.basename(model.getSource()))
                content = {'filename': os.path.basename(loc), 
                           'type': 'sedml', 
                           'modelsource': tempSedmlSource}
                zf.close()
            # other formats
            elif formtype == "image/png":
                content = {'filename': os.path.basename(loc), 'type': 'png'}
            elif formtype == "image/jpg" or formtype == "image/jpeg":
                content = {'filename': os.path.basename(loc), 'type': 'jpg'}
            elif formtype == "application/pdf":
                content = {'filename': os.path.basename(loc), 'type': 'pdf'}
            elif formtype == "plain/text":
                content = {'filename': os.path.basename(loc), 'type': 'txt'}
            elif formtype == "plain/csv":
                content = {'filename': os.path.basename(loc), 'type': 'csv'}
            elif formtype == "plain/dat":
                content = {'filename': os.path.basename(loc), 'type': 'dat'}
            contents.append(content)
            
        print(contents)
        return contents
        
    def removeFile(self, fileName):
        baseName, fileFormat = os.path.splitext(fileName)
        tempPath = os.path.join(os.path.dirname(self.combinePath), os.path.splitext(
            os.path.basename(self.combinePath))[0] + '_tempcombine' + os.path.splitext(os.path.basename(self.combinePath))[1])
        zin = ZipFile(self.combinePath, 'r')
        zout = ZipFile(tempPath, 'w')
        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if (item.filename != fileName):
                zout.writestr(item, buffer)
        zout.close()
        zin.close()
        os.remove(self.combinePath)
        os.rename(tempPath, self.combinePath)
        if fileName == 'manifest.xml':
            pass
        else:
            self.updateManifest(baseName + fileFormat, fileFormat[1:], delete=True)
    
    def update(self, currentExp):
        currentExp.updateCombine(self.combinePath)
        
    def readManifest(self):
        zf = ZipFile(self.combinePath, 'r')
        try:
            man = zf.read(r'manifest.xml')
        except KeyError as e:
            raise e
        zf.close()
        return man
            
    def updateManifest(self, fileName, fileType, delete=False):
        man = self.readManifest()
        man = man.splitlines()
        
        if delete == True:
            matching = [s for s in man if fileName in s]
            man.remove(matching[0])
        else:
            if fileType == 'sbml':
                value = r'    <content location="./' + fileName + '" format="http://identifiers.org/combine.specifications/sbml"/>'
            elif fileType == 'sedml':
                value = r'    <content location="./' + fileName + '" master="true" format="http://identifiers.org/combine.specifications/sed-ml"/>'
            elif fileType == 'png':
                value = r'    <content location="./fig/'+ fileName + '" format="image/png"/>'
            elif fileType == 'jpg' or fileType == '.jpeg':
                value = r'    <content location="./fig/'+ fileName + '" format="image/jpg"/>'
            elif fileType == 'pdf':
                value = r'    <content location="./data/'+ fileName + '" format="application/pdf"/>'
            elif fileType == 'txt':
                value = r'    <content location="./data/'+ fileName + '" format="plain/text"/>'
            elif fileType == 'csv':
                value = r'    <content location="./data/'+ fileName + '" format="plain/csv"/>'
            elif fileType == 'dat':
                value = r'    <content location="./data/'+ fileName + '" format="plain/dat"/>'
            else:
                raise Exception("Unsupported file type")            
            man.insert(-1, value)
        man = "\n".join(man)
        self.removeFile(r'manifest.xml')
        
        zf = ZipFile(self.combinePath, 'a')
        zf.writestr(r'manifest.xml', man)
        zf.close()


class CombineTools(object):
    """ Helper functions to work with combine archives."""
    # TODO: integrate with the rest of the combine archive

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
        zip = ZipFile(archivePath, 'r')

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
            tree = et.parse(manifest)
            root = tree.getroot()
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
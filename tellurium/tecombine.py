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


class Asset(object):
    RESOURCE_URI = {
        'sbml': 'http://identifiers.org/combine.specifications/sbml',
        'sed-ml': 'http://identifiers.org/combine.specifications/sed-ml'
    }

    def __init__(self, raw=None, archname=None):
        self.raw = raw
        self.archname = archname
        self.filename = None
        self.uri = None

    @classmethod
    def fromRaw(cls, raw, archname):
        """ Create asset from raw string.

        :param raw: raw string content
        :type raw: str
        :param archname: ??
        :type archname: ??
        :return:
        :rtype:
        """
        asset = cls()
        asset.filename = None
        asset.raw = raw
        asset.archname = archname
        return asset

    @classmethod
    def fromFile(cls, filename):
        """ Create asset from filename.

        :param filename:
        :type filename:
        :return:
        :rtype:
        """
        asset = cls()
        asset.filename = filename
        asset.archname = os.path.basename(filename)
        with open(filename) as f:
            asset.raw = f.read()
        return asset


class SBMLAsset(Asset):
    """ SBML asset. """
    def getResourceURI(self):
        return Asset.RESOURCE_URI['sbml']

    @classmethod
    def fromAntimony(cls, antimonyStr, archname):
        """ Create SBMLAsset from antimonyStr
        :param antimonyStr:
        :type antimonyStr:
        :param archname:
        :type archname:
        :return:
        :rtype:
        """
        r = te.loada(antimonyStr)
        raw = r.getSBML()
        return cls.fromRaw(raw=raw, archname=archname)


class SEDMLAsset(Asset):
    """ SEDML asset. """
    def getResourceURI(self):
        return Asset.RESOURCE_URI['sed-ml']

    @classmethod
    def fromPhrasedML(cls, phrasedmlStr, archname):

        sedmlStr = phrasedml.convertString(phrasedmlStr)
        # necessary to add xml extensions to antimony models
        phrasedml.addDotXMLToModelSources()
        sedmlStr = phrasedml.getLastSEDML()
        if sedmlStr is None:
            raise Exception(phrasedml.getLastError())

        return cls.fromRaw(raw=sedmlStr, archname=archname)


class CombineArchive(object):
    """ Class for creating combine archives.

    Raw and file assets are added to the empty COMBINE archive via
    the respective add*Str and add*File methods.
    The archive is written to file via the write function.
    """
    # TODO: add general file asset

    def __init__(self):
        self.assets = []
        self.manifest = ''

    def checkfile(self, filename):
        """ Check that file exists. """
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise RuntimeError('No such file: {}'.format(filename))

    def addAsset(self, asset):
        self.assets.append(asset)

    def addSBMLStr(self, sbmlStr, archname):
        self.addAsset(SBMLAsset.fromRaw(sbmlStr, archname))

    def addAntimonyStr(self, antimonyStr, archname):
        self.addAsset(SBMLAsset.fromAntimony(antimonyStr, archname))

    def addSEDMLStr(self, sedmlStr, archname):
        self.addAsset(SEDMLAsset.fromRaw(sedmlStr, archname))

    def addPhraSEDMLStr(self, phrasedmlStr, archname):
        self.addAsset(SEDMLAsset.fromPhrasedML(phrasedmlStr, archname))

    def addSBMLFile(self, filename):
        self.checkfile(filename)
        self.addAsset(SBMLAsset.fromFile(filename))

    def addSEDMLFile(self, filename):
        self.checkfile(filename)
        self.addAsset(SEDMLAsset.fromFile(filename))

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
        if asset.filename is not None:
            zf.write(asset.filename, asset.archname)
        else:
            zf.writestr(asset.archname, asset.raw)

        self.manifest += '    <content location="./{}" master="true" format="{}"/>\n'.format(
            asset.archname,
            asset.getResourceURI()
        )


class OpenCombine(object):
    """ Main class for handling COMBINE Archives. """

    def __init__(self, combinePath):
        # open existing
        if os.path.exists(combinePath):
            self.combinePath = combinePath
        # create new archive
        else:

            raise Exception("Invalid path for combine archive")


    # <SBML>
    def addSBML(self, sbmlPath):
        modelname = self.getModelName(sbmlPath)
        contents = self.listContents()
        zf = ZipFile(self.combinePath, 'a')
        if os.path.exists(sbmlPath):
            numSame = 0
            while contents.count(modelname + '.xml') == 1:
                # This should never happen (breaks the SEDML files)
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

    def getModelName(self, sbmlfile):
        r = roadrunner.RoadRunner(sbmlfile)
        return r.getModel().getModelName()


    def addAntimony(self, antimonyStr):
        """ Add antimony to archive. """
        sbmlStr = te.antimonyToSBML(antimonyStr)
        self.addSBML(sbmlStr)

    # <SEDML>

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

    # Other file

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
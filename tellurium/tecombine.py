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


    An entry in the OmexManifest is represented by the Content class. It declares a file in the COMBINE archive. A
    content element possesses two required attributes, location and format, as well as an optional one, master.

    The location attribute of type string is required. It represents the relative location of an entry within the archive.
        The archive is represented by a dot '.'.

        The format attribute of type string is required. It indicates the file type of the Content element. The allowed
        values fall in two categories. Either the format denotes one of the COMBINE standards, in which case the format is
        the corresponding Identifiers.org URI. Or the format represents an InternetMedia type (Freed and Borenstein,
        1996) (previously known as "MIME type"), in which case the format indicates this Media type.

        The master attribute of type boolean optional. When set to "true", it indicates that the file declared by the content
        element should be used first when processing the content of the archive. The file can be for instance the description
        of an upper model in a composed model, itself declaring the various submodels; a simulation description,
        declaring the different model descriptions and data sources used in the experiment. In most cases, one content
        element per archive will have its master attribute set to true.


"""
# TODO: handle real world archives from other tools
# TODO: metaData
# TODO: list of Entries, entry.getFormat(), entry.getLocation()

from __future__ import print_function, division

import os
import shutil
import warnings
from zipfile import ZipFile
import phrasedml
import re

import tellurium as te
import roadrunner
try:
    import tesedml as libsedml
except ImportError:
    import libsedml
from xml.etree import ElementTree as et


def combine(combinePath):
    """ Open a combine archive from local directory.

    :param combinePath: Path to a combine archive
    :type combinePath: str
    :returns: OpenCombine instance
    """
    return OpenCombine(combinePath)


class Asset(object):
    COMBINE_PREFIX = 'http://identifiers.org/combine.specifications/'
    MEDIATYPE_PREFIX = 'http://purl.org/NET/mediatypes/'

    FORMATS = {
        # combine formats
        # http://co.mbine.org/standards/specifications/
        'biopax': COMBINE_PREFIX + 'biopax',                # Biological Pathway Exchange format
        'cellml': COMBINE_PREFIX + 'cellml',                # CellML
        'omex': COMBINE_PREFIX + 'omex',                    # COMBINE archive
        'omex-manifest': COMBINE_PREFIX + 'omex-manifest',  # COMBINE archive manifest
        'omex-metadata': COMBINE_PREFIX + 'omex-metadata',  # COMBINE archive metadata
        'gpml': COMBINE_PREFIX + 'gpml',                    # GenMAPP Pathway Markup Language
        'sbgn': COMBINE_PREFIX + 'sbgn',                    # Systems Biology Graphical Notation
        'sbml': COMBINE_PREFIX + 'sbml',                    # Systems Biology Markup Language
        'sbol': COMBINE_PREFIX + 'sbol',                    # Synthetic Biology Open Language
        'sed-ml': COMBINE_PREFIX + 'sed-ml',                # Simulation Experiment Description Markup Language
        'teddy': COMBINE_PREFIX + 'teddy',                  # TErminology for the Description of DYnamics

        # File assets
        'png': MEDIATYPE_PREFIX + 'image/png',
        'jpg': MEDIATYPE_PREFIX + 'image/jpg',
        'jpeg': MEDIATYPE_PREFIX + 'image/jpg',
        'svg': MEDIATYPE_PREFIX + 'image/svg+xml',

        'pdf': MEDIATYPE_PREFIX + 'application/pdf',

        'txt': MEDIATYPE_PREFIX + 'text/plain',
        'csv': MEDIATYPE_PREFIX + 'text/csv',
        'dat': MEDIATYPE_PREFIX + 'text/dat',
        'md': MEDIATYPE_PREFIX + 'text/x-markdown',
    }

    def __init__(self, raw=None, location=None, filetype=None, master=False):
        self.raw = raw
        self.location = location
        self.master = master
        self.format = Asset.formatFromFiletype(filetype)
        # subfolders for figures and data
        if filetype in ['png', 'jpg', 'jpeg', 'svg']:
            self.location = 'fig/{}'.format(self.location)
        if filetype in ['txt', 'csv', 'dat']:
            self.location = 'data/{}'.format(self.location)


    @classmethod
    def formatFromFiletype(cls, filetype):
        if filetype not in cls.FORMATS:
            raise IOError("Unsupported filetype for CombineArchive. Supported are: {}".format(cls.FORMATS.keys()))
        return cls.FORMATS[filetype]


    @classmethod
    def fromRaw(cls, raw, location, filetype, master=None):
        """ Create asset from raw string.

        :param raw: raw string content
        :type raw: str
        :param location: ??
        :type location: ??
        :return:
        :rtype:
        """
        return cls(raw=raw, location=location, filetype=filetype, master=master)

    @classmethod
    def fromFile(cls, filename, filetype, master=None):
        """ Create asset from filename.

        :param filename:
        :type filename:
        :return:
        :rtype:
        """
        location = os.path.basename(filename)
        with open(filename) as f:
            raw = f.read()
        return cls(raw=raw, location=location, filetype=filetype, master=master)

    @classmethod
    def fromAntimony(cls, antimonyStr, location, master=None):
        """ Create SBMLAsset from antimonyStr
        :param antimonyStr:
        :type antimonyStr:
        :param location:
        :type location:
        :return:
        :rtype:
        """
        r = te.loada(antimonyStr)
        raw = r.getSBML()
        return cls.fromRaw(raw=raw, location=location, filetype='sbml', master=master)

    @classmethod
    def fromPhrasedML(cls, phrasedmlStr, location, master=None):
        sedmlStr = phrasedml.convertString(phrasedmlStr)
        # necessary to add xml extensions to antimony models
        phrasedml.addDotXMLToModelSources()
        sedmlStr = phrasedml.getLastSEDML()
        if sedmlStr is None:
            raise Exception(phrasedml.getLastError())

        return cls.fromRaw(raw=sedmlStr, location=location, filetype='sed-ml', master=master)


class CombineArchive(object):
    """ Class for creating combine archives.

    Raw and file assets are added to the empty COMBINE archive via
    the respective add*Str and add*File methods.
    The archive is written to file via the write function.
    """
    def __init__(self):
        self.assets = []

    def checkfile(self, filename):
        """ Check that file exists. """
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise RuntimeError('No such file: {}'.format(filename))

    def addAsset(self, asset):
        self.assets.append(asset)

    def addSBMLStr(self, sbmlStr, location, master=None):
        self.addAsset(Asset.fromRaw(sbmlStr, location, filetype='sbml', master=master))

    def addAntimonyStr(self, antimonyStr, location, master=None):
        self.addAsset(Asset.fromAntimony(antimonyStr, location, master=master))

    def addSEDMLStr(self, sedmlStr, location, master=None):
        self.addAsset(Asset.fromRaw(sedmlStr, location, filetype='sed-ml', master=master))

    def addPhraSEDMLStr(self, phrasedmlStr, location, master=None):
        self.addAsset(Asset.fromPhrasedML(phrasedmlStr, location, master=master))

    def addSBMLFile(self, filename, master=None):
        self.checkfile(filename)
        self.addAsset(Asset.fromFile(filename, filetype='sbml', master=master))

    def addSEDMLFile(self, filename, master=None):
        self.checkfile(filename)
        self.addAsset(Asset.fromFile(filename, filetype='sed-ml', master=master))

    def addFile(self, filename, filetype, master=None):
        self.addAsset(Asset.fromFile(filename=filename, filetype=filetype, master=master))

    def addStr(self, textStr, location, filetype):
        self.addAsset(Asset.fromRaw(raw=textStr, location=location, filetype=filetype))

    def write(self, outfile):
        """ Write the combine archive to the outfile.
        Writes all assets and creates the manifest.xml.
        """
        manifestStr = self._createManifestString()

        with ZipFile(outfile, 'w') as zf:
            # write assets
            for a in self.assets:
                zf.writestr(a.location, a.raw)
            # write manifest
            zf.writestr('manifest.xml', manifestStr)

    def _createManifestString(self):
        lines = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<omexManifest xmlns="http://identifiers.org/combine.specifications/omex-manifest">',
                 '    <content location="./manifest.xml" format="http://identifiers.org/combine.specifications/omex-manifest"/>']
        for a in self.assets:
            if a.master:
                lines.append('    <content location="./{}" format="{}" master="true"/>'.format(a.location, a.format))
            else:
                lines.append('    <content location="./{}" format="{}"/>'.format(a.location, a.format))
        lines.append('</omexManifest>')
        return "\n".join(lines)


    @staticmethod
    def extractArchive(archivePath, directory):
        """ Extracts given archive into the target directory.

        Target directory is created if it does not exist.
        Files are overwritten in the directory !

        :param archivePath: path to combine archive
        :type archivePath: str
        :param directory: path to directory where to extract to
        :type directory:
        """
        if not os.path.isdir(directory):
            os.makedirs(directory)
        else:
            warnings.warn("Combine archive directory already exists:{}".format(directory))

        fh = open(archivePath, 'rb')
        z = ZipFile(fh)
        for name in z.namelist():
            z.extract(name, directory)
        fh.close()

    @staticmethod
    def readContentsFromManifest(manifestPath):
        """ Reads the manifest information.

        :param manifestPath:
        :type manifestPath:
        :return:
        :rtype:
        """
        from collections import namedtuple
        Content = namedtuple('Content', 'location format master')
        contents = []

        tree = et.parse(manifestPath)
        root = tree.getroot()
        for child in root:
            location = child.attrib['location']
            format = child.attrib['format']
            master = child.attrib.get('master', None)
            contents.append(Content(location, format, master))
        return contents

    @staticmethod
    def filePathsFromExtractedArchive(directory, filetype):
        """ Reads file paths from extracted combine archive.

        Searches the manifest.xml of the archive for files of the
        specified filetype and checks if the files exist in the directory.

        :param directory: directory of extracted archive
        :return: list of paths
        :rtype: list
        """
        paths = []
        manifest = os.path.join(directory, "manifest.xml")
        if os.path.exists(manifest):
            contents = CombineArchive.readContentsFromManifest(manifest)
            for c in contents:
                # matches the filetype
                if filetype in c.format:
                    # real path
                    path = os.path.join(directory, c.location)
                    if not os.path.exists(path):
                        raise IOError('Path specified in manifest.xml does not exist in archive: {}'.format(path))
                    paths.append(path)
        else:
            # no manifest, use all files in folder
            warnings.warn("No 'manifest.xml' in archive, trying to resolve manually")

            # TODO: this must recursively look in folder, not very robust right now
            for fname in os.listdir(directory):
                if filetype == "sed-ml":
                    if fname.endswith(".sedml") or fname.endswith(".sedx.xml"):
                        paths.append(os.path.join(directory, fname))

        paths = [os.path.normpath(p) for p in paths]
        return paths


###########################################################################################
# working with existing combine archives

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
    def addSBML(self, sbmlPath, filename=None):
        """ Adds SBML file into COMBINE archive.
        :param sbmlPath: path to SBML file or full SBML file string
        """
        modelname = self.getModelName(sbmlPath)
        contents = self.listContents()
        zf = ZipFile(self.combinePath, 'a')
        if os.path.exists(sbmlPath):
            numSame = 0
            while contents.count(modelname + '.xml') == 1:
                # This should never happen (breaks the SEDML files)
                modelname = modelname + '_' + str(numSame) + '.xml'
                numSame += 1
            if filename != None:
                if filename[-3:] != ('xml' or 'sbml'):
                    filename = filename + '.xml'
                modelname = filename
            zf.write(sbmlPath, arcname=modelname)
        elif sbmlPath.startswith(r'<?xml'):
            numSame = 0
            while contents.count(modelname + '.xml') == 1:
                modelname = modelname + '_' + str(numSame) + '.xml'
                numSame += 1
            if filename != None:
                if filename[-3:] != ('xml' or 'sbml'):
                    filename = filename + '.xml'
                modelname = filename
            zf.writestr(modelname, sbmlPath)
        else:
            raise Exception("Invalid string for sbml: Check the path of the file")
        zf.close()
        self.updateManifest(modelname, 'sbml')

    def getModelName(self, sbmlfile):
        r = roadrunner.RoadRunner(sbmlfile)
        return r.getModel().getModelName()


    def addAntimony(self, antimonyStr, filename=None):
        """ Adds SBML file as Antimony into COMBINE archive.
        :param antimonyStr: antimony string
        """
        sbmlStr = te.antimonyToSBML(antimonyStr)
        self.addSBML(sbmlStr, filename)

    # <SEDML>

    def addSEDML(self, sedmlPath, arcname=None):
        """ Adds SEDML file into COMBINE archive.
        :param sedmlPath: path to SEDML file
        :param arcname: (optional) desired name of SEDML file
        """
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
        """ Adds SEDML file as phraSEDML string into COMBINE archive.
        :param phrasedmlStr: phraSEDML string
        :param antimonyStr: antimony string to be referenced
        :param arcname: (optional) desired name of SEDML file
        """
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
        """ Adds other file into COMBINE archive.

        Currently, png, jpg, pdf, txt, csv, dat formats are supported.

        :param filePath: path to the file
        """
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
        """ returns SBML

        :param sbmlfile: filename of SBML file in COMBINE archive
        :return: SBML string
        :rtype: str
        """

        zf = ZipFile(self.combinePath, 'r')
        sbmlStr = zf.read(sbmlfile)
        zf.close()

        return sbmlStr

    def getSBMLAsAntimony(self, sbmlfile):
        """ returns SBML as antimony

        :param sbmlfile: filename of SBML file in COMBINE archive
        :return: antimony string
        :rtype: str
        """
        zf = ZipFile(self.combinePath, 'r')
        sbmlStr = zf.read(sbmlfile)
        zf.close()
        antStr = te.sbmlToAntimony(sbmlStr)

        return antStr

    def getSEDML(self, sedmlfile):
        """ returns SEDML

        :param sbmlfile: filename of SEDML file in COMBINE archive
        :return: SEDML string
        :rtype: str
        """
        zf = ZipFile(self.combinePath, 'r')
        sedmlStr = zf.read(sedmlfile)
        zf.close()

        return sedmlStr

    def getSEDMLAsPhrasedml(self, sedmlfile):
        """ returns SEDML as phraSEDML

        :param sbmlfile: filename of SEDML file in COMBINE archive
        :return: phraSEDML string
        :rtype: str
        """
        zf = ZipFile(self.combinePath, 'r')
        sedmlStr = zf.read(sedmlfile)
        zf.close()
        phrasedmlStr = phrasedml.convertString(sedmlStr)

        return phrasedmlStr

    def listContents(self):
        """ returns simplified content list

        """
        zf = ZipFile(self.combinePath, 'r')
        temp = zf.namelist()
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
            # manifest
            elif formtype == "http://identifiers.org/combine.specifications/omex-manifest":
                content = {'filename': os.path.basename(loc), 'type': 'manifest'}
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
            if content != None:
                contents.append(content)

        return contents

    def removeFile(self, fileName):
        """ remove specified file from COMBINE archive

        :param fileName: name of the file to be removed
        """
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
        shutil.move(tempPath, self.combinePath)

        if fileName == 'manifest.xml':
            pass
        else:
            self.updateManifest(baseName + fileFormat, fileFormat[1:], delete=True)

    def update(self, targetFile, change):
        """ update the contents of SBML or SEDML files in COMBINE archive

        Only supports antimony or phrasedml string. For other input types, use removeFile().

        :param targetFile: SBML or SEDML file to be updated
        :param change: antimony or phrasedml string
        """
        contentList = self.listDetailedContents()

        try:
            filetype = (item for item in contentList if item["filename"] == targetFile).next().get('type')
        except TypeError:
            raise Exception('There is no file name called ' + targetFile + 'in COMBINE archive')

        if filetype == 'sbml':
            self.removeFile(targetFile)
            self.addAntimony(change, filename=targetFile)
        elif filetype == 'sedml':
            modelSource = (item for item in contentList if item["filename"] == targetFile).next().get('modelsource')[0]
            refAntStr = self.getSBMLAsAntimony(modelSource)
            self.removeFile(targetFile)
            self.addPhrasedml(change, refAntStr, arcname=targetFile)
        else:
            raise Exception('Unsupported file type')

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
        man = "\n".join([str(item) for item in man])
        self.removeFile(r'manifest.xml')

        zf = ZipFile(self.combinePath, 'a')
        zf.writestr(r'manifest.xml', man)
        zf.close()

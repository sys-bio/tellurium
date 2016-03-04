"""
Utilities for working with combine archives.
"""
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
        return os.path.basename(f)

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
        if not os.path.exists(filename) or not os.path.isfile(filename):
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

    def writeAsset(self, zf, asset):
        if asset.isFile():
            zf.write(asset.getFileName(), asset.getArchName())
        else:
            zf.writestr(asset.getArchName(), asset.getExportedStr())

        self.manifest += '    <content location="./{}" master="true" format="{}"/>\n'.format(
            asset.getArchName(),
            asset.getResourceURI()
            )

    def write(self, outfile):
        self.manifest = ''
        with ZipFile(outfile, 'w') as z:
            self.manifest += '<?xml version="1.0"  encoding="utf-8"?>\n<omexManifest  xmlns="http://identifiers.org/combine.specifications/omex-manifest">\n'
            self.manifest += '    <content location="./manifest.xml" format="http://identifiers.org/combine.specifications/omex-manifest"/>\n'

            for a in self.assets:
                self.writeAsset(z, a)

            self.manifest += '</omexManifest>\n'

            z.writestr('manifest.xml', self.manifest)

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
        contentList = []
        man = self.readManifest()
        xml = et.ElementTree(et.fromstring(man))
        root = xml.getroot()
        for child in root:
            attribute = child.attrib
            formtype = attribute.get('format')
            loc = attribute.get('location')
            if formtype == "http://identifiers.org/combine.specifications/sbml":
                if loc.startswith('http') or loc.startswith('www'):
                    contentList.append({'filename':loc, 'type':'sbml'})                    
                else:
                    contentList.append({'filename':os.path.basename(loc), 'type':'sbml'})
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
                for i in range(0, sedmlDoc.getNumModels()):
                    currentModel = sedmlDoc.getModel(i)
                    if os.path.splitext(os.path.basename(currentModel.getSource()))[1] == '':
                        pass
                    else:
                        tempSedmlSource.append(os.path.basename(currentModel.getSource()))
                contentList.append({'filename':os.path.basename(loc), 'type':'sedml', 'modelsource':tempSedmlSource})
                zf.close()
            elif formtype == "image/png":
                contentList.append({'filename':os.path.basename(loc), 'type':'png'})
            elif formtype == "image/jpg" or formtype == "image/jpeg":
                contentList.append({'filename':os.path.basename(loc), 'type':'jpg'})
            elif formtype == "application/pdf":
                contentList.append({'filename':os.path.basename(loc), 'type':'pdf'})
            elif formtype == "plain/text":
                contentList.append({'filename':os.path.basename(loc), 'type':'txt'})
            elif formtype == "plain/csv":
                contentList.append({'filename':os.path.basename(loc), 'type':'csv'})
            elif formtype == "plain/dat":
                contentList.append({'filename':os.path.basename(loc), 'type':'dat'})
            
        print(contentList)
        
        return(contentList)
        
    def removeFile(self, fileName):
        baseName, fileFormat = os.path.splitext(fileName)
        tempPath = os.path.join(os.path.dirname(self.combinePath), os.path.splitext(
            os.path.basename(self.combinePath))[0] + '_tempcombine' + os.path.splitext(os.path.basename(self.combinePath))[1])
        zin = ZipFile (self.combinePath, 'r')
        zout = ZipFile (tempPath, 'w')
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
        currentExp.update(self.combinePath)
        
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

def export(outfile, antimonyStr, phrasedmlStrs):
    m = MakeCombine()
    modelNames = []
    for i in range(len(antimonyStr)):
        r = te.loada(antimonyStr[i])
        SBMLName = r.getModel().getModelName()
        m.addAntimonyStr(antimonyStr[i], SBMLName + ".xml")
        modelNames.append(SBMLName)

    # remaining arguments are assumed to be phrasedml
    n = 1
    for phrasedmlStr in phrasedmlStrs:
        reModel = r"""(\w*) = model ('|")(.*)('|")"""
        lines = phrasedmlStr.splitlines()
        for i, s in enumerate(lines):
            reSearchModel = re.split(reModel, s)
            if len(reSearchModel) > 1:
                modelsource = str(reSearchModel[3])
                modelname = os.path.basename(modelsource)
        
        if modelname not in modelNames:
            raise Exception("Cannot find the model defined in phrasedml string. Check the model name in antimony")
        phrasedml.setReferencedSBML(modelname, te.antimonyToSBML(antimonyStr[modelNames.index(modelname)]))
        m.addPhraSEDMLStr(phrasedmlStr, 'experiment{}.xml'.format(n))
        n += 1

    m.write(outfile)
    phrasedml.clearReferencedSBML()
    
from __future__ import print_function, division, absolute_import

import os
import re
import phrasedml
try:
    import tesedml as libsedml
except ImportError:
    import libsedml


class phrasedmlImporter(object):

    def __init__(self, sbml_map={}):
        """ Constructor. """
        self.sedml_str = None
        self.sedml_path = None
        self.sbml_map = sbml_map


    @classmethod
    def fromContent(cls, sedml_str, sbml_map={}):

        # FIXME: bad hack for https://github.com/fbergmann/libSEDML/issues/47
        # test for JWS quirks
        if 'xmlns="http://sed-ml.org/sed-ml/level1/version3"' in sedml_str:
            # import xml.etree.ElementTree as ElementTree
            # root = ElementTree.fromstring(sedml_str)
            # for p in root.findall('{http://sed-ml.org/sed-ml/level1/version3}plot2D'):
            #     if not 'logX' in p.attrib or not 'logY' in p.attrib:
            #         logX = False
            #         logY = False
            #         for l in p.findall('{http://sed-ml.org/sed-ml/level1/version3}listOfCurves'):
            #             for c in l.findall('{http://sed-ml.org/sed-ml/level1/version3}curve'):
            #                 if 'logX' in c.attrib and c.attrib['logX'].lower() == 'true':
            #                     logX = True
            #                 if 'logY' in c.attrib and c.attrib['logY'].lower() == 'true':
            #                     logY = True
            #         p.set('logX', logX)
            #         p.set('logY', logY)
            # sedml_str = (ElementTree.tostring(root, encoding='utf8', method='xml')).decode('utf8')
            while True:
                p = sedml_str.find('plot2D')
                if p < 0:
                    break
                b = sedml_str.find('>', p)
                if b < 0:
                    break
                l = sedml_str.find('logX', p)
                if l < 0 or b < l:
                    sedml_str = sedml_str[:p] + 'plot2D logX="false" logY="false" ' + sedml_str[p+len('plot2D'):]
                else:
                    break
            print(sedml_str)


        importer = phrasedmlImporter(sbml_map)
        importer.sedml_str = sedml_str
        # test for errors
        result = importer.toPhrasedml()
        if result is None:
            # get errors from libsedml
            doc = libsedml.SedReader().readSedMLFromString(sedml_str)
            if doc.getNumErrors():
                max_len = 100
                message = doc.getError(doc.getNumErrors()-1).getMessage()
                message = message[:max_len] + '...' if len(message) > max_len else message
                raise RuntimeError('Errors reading SED-ML: {}'.format(message))
            else:
                raise RuntimeError('Unable to read SED-ML.')
        return importer


    def isInRootDir(self, file):
        d = os.path.split(file)[0]
        return d == '' or d == '.'

    def removeFileExt(self, filename):
        return os.path.splitext(filename)[0]

    def formatResource(self, filename):
        """ Normalizes and also strips xml extension."""
        return self.removeFileExt(os.path.normpath(filename))

    def fixModelRefs(self, phrasedml_str):
        ''' Changes all references of type myModel.xml to myModel.'''
        model_ref = re.compile(r'^.*\s*model\s*"([^"]*)"\s*$')
        out_str = ''
        for line in phrasedml_str.splitlines():
            match = model_ref.match(line)
            if match:
                filename = match.group(1)
                if self.isInRootDir(filename):
                    line = line.replace(filename,self.formatResource(filename))
            out_str += line+'\n'
        return out_str

    def toPhrasedml(self):
        # assign sbml resources
        # print('toPhrasedml sbml resources:')
        phrasedml.clearReferencedSBML()
        for sbml_resource in self.sbml_map:
            # print('  {} -> {}'.format(sbml_resource, self.sbml_map[sbml_resource][:30]))
            phrasedml.setReferencedSBML(sbml_resource, self.sbml_map[sbml_resource])
        # convert to phrasedml
        if self.sedml_str:
            result = phrasedml.convertString(self.sedml_str)
            if result is None:
                raise RuntimeError(phrasedml.getLastError())
            return self.fixModelRefs(phrasedml.getLastPhraSEDML())
        elif self.sedml_path:
            result = phrasedml.convertFile(self.sedml_str)
            if result is None:
                raise RuntimeError(phrasedml.getLastError())
            return self.fixModelRefs(phrasedml.getLastPhraSEDML())

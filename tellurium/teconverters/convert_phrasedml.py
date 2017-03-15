from __future__ import print_function, division

import os, re

import phrasedml
from tesedml import SedReader

class phrasedmlImporter:
    @classmethod
    def fromContent(cls, sedml_str, sbml_map={}):
        importer = phrasedmlImporter(sbml_map)
        importer.sedml_str = sedml_str
        # test for errors
        result = importer.toPhrasedml()
        if result is None:
            # get errors from libsedml
            doc = SedReader().readSedMLFromString(sedml_str)
            if doc.getNumErrors():
                max_len = 100
                message = doc.getError(doc.getNumErrors()-1).getMessage()
                message = message[:max_len] + '...' if len(message) > max_len else message
                raise RuntimeError('Errors reading SED-ML: {}'.format(message))
            else:
                raise RuntimeError('Unable to read SED-ML.')
        return importer

    def __init__(self, sbml_map={}):
        self.sedml_str = None
        self.sedml_path = None
        self.sbml_map = sbml_map

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
        print('toPhrasedml sbml resources:')
        phrasedml.clearReferencedSBML()
        for sbml_resource in self.sbml_map:
            print('  {} -> {}'.format(sbml_resource, self.sbml_map[sbml_resource][:30]))
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

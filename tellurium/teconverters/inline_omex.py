from __future__ import print_function, division

import tecombine as libcombine
import phrasedml

class inlineOmex:
    @classmethod
    def fromString(cls, omex_str):
        from .extractor import partitionInlineOMEXString
        sb,pml = partitionInlineOMEXString(omex_str)
        pml = '\n'.join(pml)
        return cls({'main.xml':pml},'main.xml',sb)

    def __init__(self, pmdict, master, sblist):
        '''Converts a dictionary of PhraSEDML files and list of Antimony files into sedml/sbml.

        :param pmdict: A dictionary containing the phrasedml keyed by the sedml file name
        :param master: The master sedml file
        :param sblist: A list of strings of Antimony sources'''

        from .convert_omex import Omex, SbmlAsset, SedmlAsset
        from .convert_antimony import antimonyConverter

        self.omex = Omex()

        self.master = master

        # Convert antimony to sbml
        for sb in sblist:
            modulename, sbmlstr = antimonyConverter().antimonyToSBML(sb)
            self.omex.addSbmlAsset(SbmlAsset(modulename+'.xml', sbmlstr))

        # Convert phrasedml to sedml
        for t in pmdict:
            for sbml_asset in self.omex.getSbmlAssets():
                phrasedml.setReferencedSBML(sbml_asset.getModuleName(), sbml_asset.getContent())
            phrasedml.convertString(pmdict[t])
            phrasedml.addDotXMLToModelSources()
            sedml = phrasedml.getLastSEDML()
            if sedml is None:
                raise RuntimeError('Unable to convert PhraSEDML to SED-ML: {}'.format(phrasedml.getLastError()))
            self.omex.addSedmlAsset(SedmlAsset(t, sedml))

    def executeOmex(self):
        self.omex.executeOmex()

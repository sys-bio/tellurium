"""
Working with inline omex.
This is used in the notebook to provide functionality to the cells.
"""
from __future__ import print_function, division, absolute_import
import re
import os
import argparse

try:
    import tecombine as libcombine
except ImportError:
    import libcombine

import phrasedml
from .antimony_regex import getModelStartRegex, getModelEndRegex


def saveInlineOMEX(omex_str, out_path):
    """Saves an inline omex string to a file.

    :param omex_str: The inline omex string
    :type  omex_str: str
    :param out_path: Path to the output file
    :type  out_path: str
    """
    omex = inlineOmex.fromString(omex_str)
    omex.exportToCombine(out_path)


def parseMagicArgs(line):
    parser = argparse.ArgumentParser()
    parser.add_argument('location')
    parser.add_argument('--master', type=bool)
    return parser.parse_args(line)


class inlineOmex(object):

    def __init__(self, sources):
        """ Converts a dictionary of PhraSEDML files and list of Antimony files into sedml/sbml.

        :param sources: Sources returned from partitionInlineOMEXString
        """
        from .convert_omex import Omex, SbmlAsset, SedmlAsset, readCreator
        from .convert_antimony import antimonyConverter

        phrasedml.clearReferencedSBML()

        from .. import DumpJSONInfo
        self.omex = Omex(
            description=DumpJSONInfo(),
            creator=readCreator()
        )

        # Convert antimony to sbml
        for t, loc, master in (
        (x['source'], x['location'] if 'location' in x else None, x['master'] if 'master' in x else None)
        for x in sources if x['type'] == 'antimony'):
            modulename, sbmlstr = antimonyConverter().antimonyToSBML(t)
            outpath = loc if loc is not None else modulename + '.xml'
            self.omex.addSbmlAsset(SbmlAsset(outpath, sbmlstr, master=master))

        # Convert phrasedml to sedml
        for t, loc, master in (
        (x['source'], x['location'] if 'location' in x else None, x['master'] if 'master' in x else None)
        for x in sources if x['type'] == 'phrasedml'):

            for sbml_asset in self.omex.getSbmlAssets():
                if sbml_asset.location:
                    if loc:
                        path = os.path.relpath(sbml_asset.location, os.path.dirname(loc))
                    else:
                        path = sbml_asset.location
                else:
                    path = sbml_asset.getModuleName()
                # make windows paths like unix paths
                if os.path.sep == '\\':
                    path = path.replace(os.path.sep, '/')
                phrasedml.setReferencedSBML(path, sbml_asset.getContent())
            phrasedml.convertString(t)
            phrasedml.addDotXMLToModelSources(False)
            sedml = phrasedml.getLastSEDML()
            if sedml is None:
                raise RuntimeError('Unable to convert PhraSEDML to SED-ML: {}'.format(phrasedml.getLastError()))
            outpath = loc if loc is not None else 'main.xml'
            self.omex.addSedmlAsset(SedmlAsset(outpath, sedml, master=master))


    @classmethod
    def fromString(cls, omex_str):
        """Given mixed Antimony/PhraSEDML, separates out the constituent parts.
        Assumes that Antimony and PhraSEDML are not mixed on the same line.

        :param instr: The input string containing mixed Antimony/PhraSEDML
        :returns: 2-tuple containing a list of Antimony parts and a list of PhraSEDML parts as strings
        """
        class S_PML:
            # recognizes Antimony start
            sb_start = re.compile(getModelStartRegex())
            force_sb_start = re.compile(r'^\s*(%crn|%sb|%antimony|%model).*$')
            force_pml_start = re.compile(r'^\s*(%tasks|%phrasedml)\s+.*$')

            def __init__(self, force=False, initl_content='', args=None):
                self.pml = initl_content
                self.force = force
                self.args = args

            def __call__(self, line):
                if self.force_sb_start.match(line) != None:
                    args = parseMagicArgs(line.split()[1:])
                    return S_SB(True, args=args), self.pml if self.force else None, None, self.args if self.force else None
                if self.force_pml_start.match(line) != None:
                    args = parseMagicArgs(line.split()[1:])
                    return S_PML(True, args=args), self.pml if self.force else None, None, self.args if self.force else None
                if not self.force and self.sb_start.match(line) != None:
                    return S_SB(self.force, line), self.pml, None, self.args
                else:
                    self.pml += line + '\n'
                    return self, None, None, None

            def dump(self): return self.pml, None, self.args

        class S_SB:
            sb_end = re.compile(getModelEndRegex())
            force_sb_start = re.compile(r'^\s*(%crn|%sb|%antimony|%model).*$')
            force_pml_start = re.compile(r'^\s*(%tasks|%phrasedml)\s+.*$')

            def __init__(self, force=False, initl_content='', args=None):
                self.sb = initl_content
                self.force = force
                self.args = args

            def __call__(self, line):
                if self.force_pml_start.match(line) != None:
                    args = parseMagicArgs(line.split()[1:])
                    return S_PML(True, args=args), None, self.sb if self.force else None, self.args if self.force else None
                if self.force_sb_start.match(line) != None:
                    args = parseMagicArgs(line.split()[1:])
                    return S_SB(True, args=args), None, self.sb if self.force else None, self.args if self.force else None
                if not self.force and self.sb_end.match(line) != None:
                    self.sb += line + '\n'
                    return S_PML(self.force), None, self.sb, self.args
                else:
                    self.sb += line + '\n'
                    return self, None, None, None

            def dump(self): return None, self.sb, self.args

        s = S_PML()

        sources = []
        def add_source(src, type, args):
            if src:
                new_src = {
                    'source': src,
                    'type': type,
                }
                if args is not None:
                    new_src['location'] = args.location
                    if args.master is not None:
                        new_src['master'] = args.master
                    else:
                        new_src['master'] = False
                sources.append(new_src)

        for l in omex_str.splitlines():
            s, pml, sb, args = s(l)
            add_source(pml, 'phrasedml', args)
            add_source(sb,  'antimony',  args)

        pml, sb, args = s.dump()
        add_source(pml, 'phrasedml', args)
        add_source(sb,  'antimony',  args)

        # merge phrasedml when no location specified
        if s.force == False:
            phrasedml_combined = ''
            for src in list(sources):
                if src['type'] == 'phrasedml':
                    phrasedml_combined += src['source']
                    sources.remove(src)
            if phrasedml_combined:
                sources.append({
                    'source': phrasedml_combined,
                    'type': 'phrasedml',
                    'location': 'main.xml',
                    'master': True,
                })

        return inlineOmex(sources)


    def executeOmex(self):
        """ Executes the archive. """
        self.omex.executeOmex()


    def exportToCombine(self, outpath):
        """ Exports the archive to file. """
        self.omex.exportToCombine(outpath)

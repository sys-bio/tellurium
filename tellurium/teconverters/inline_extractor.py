from __future__ import print_function, division
from .inline_omex import inlineOmex
import re

# TODO: move to teomex
def saveInlineOMEX(omex_str, out_path):
    '''Saves an inline omex string to a file. Invokes partitionInlineOMEXString.

    :param omex_str: The inline omex string
    :type  omex_str: str
    :param out_path: Path to the output file
    :type  out_path: str
    '''
    omex = inlineOmex.fromString(omex_str)
    omex.exportToCombine(out_path)

def partitionInlineOMEXString(instr):
    '''Given mixed Antimony/PhraSEDML, separates out the constituent parts.
    Assumes that Antimony and PhraSEDML are not mixed on the same line.

    :param instr: The input string containing mixed Antimony/PhraSEDML
    :returns: 2-tuple containing a list of Antimony parts and a list of PhraSEDML parts as strings
    '''
    class S_PML:
        # recognizes Antimony start
        sb_start = re.compile(r'^\s*\*?\s*model\s*[^()\s]+\s*(\([^)]*\))?\s*$')
        force_sb_start = re.compile(r'^\s(%crn|%sb)\s*$')

        def __init__(self, force=False, initl_content=''):
            self.pml = initl_content
            self.force = force

        def __call__(self, line):
            if self.force_sb_start.match(line) != None:
                return S_SB(True, line), self.pml, None
            if not self.force and self.sb_start.match(line) != None:
                return S_SB(self.force, line), self.pml, None
            else:
                self.pml += line + '\n'
                return self, None, None

        def dump(self): return self.pml, None

    class S_SB:
        sb_end = re.compile(r'^\s*end\s*$')
        force_pml_start = re.compile(r'^\s(%tasks)\s*$')

        def __init__(self, force=False, initl_content=''):
            self.sb = initl_content
            self.force = force

        def __call__(self, line):
            if self.force_pml_start.match(line) != None:
                return S_PML(True), None, self.sb
            if not self.force and self.sb_end.match(line) != None:
                self.sb += line + '\n'
                return S_PML(self.force), None, self.sb
            else:
                self.sb += line + '\n'
                return self, None, None

        def dump(self): return None, self.sb
    s = S_PML()
    sb_src = []
    pml_src = []
    for l in instr.splitlines():
        s, pml, sb = s(l)
        if pml:
            pml_src.append(pml)
        if sb:
            sb_src.append(sb)

    pml, sb = s.dump()
    if pml:
        pml_src.append(pml)
    if sb:
        sb_src.append(sb)

    return (sb_src,pml_src)

"""
Helpers to work with SBO terms in antimony.
"""

from __future__ import print_function, division, absolute_import

import re
try:
    import tesbml as libsbml
except ImportError:
    import libsbml

from .antimony_regex import getModelStartRegex, getModelEndRegex, getFunctionStartRegex, getSBORegex

def filterIfEmpty(l):
    """ If l is one line (comment), filter."""
    if len(l) == 1:
        return []
    else:
        return l

class SBOError(RuntimeError):
    pass

class antimonySBOConverter(object):
    def __init__(self, doc):
        """ Create an SBO converter.

        :param doc: SBMLDocument
        """
        self.doc = doc
        if self.doc.getNumErrors() > 0:
            raise RuntimeError('Errors encountered loading SBML')
        self.model = doc.getModel()
        if self.model is None:
            raise RuntimeError('No SBML model')

    def convert(self, antimony_str):
        """ Add SBO terms to the Antimony string corresponding to this SBML document.

        :param antimony_str: Antimony string. Should represent the same SBML this object was initialized with.
        :return: The Antimony string with the SBO terms added.
        """

        model_start = re.compile(getModelStartRegex())
        n_model_starts = 0

        function_start = re.compile(getFunctionStartRegex())

        model_end = re.compile(getModelEndRegex())
        n_model_ends = 0
        model_end_index = None

        scopes = []

        n_leading_spaces = 0

        lines = antimony_str.splitlines()


        for n,line in enumerate(lines):
            if model_start.match(line) != None:
                n_model_starts += 1
                scopes.append('model')
            if function_start.match(line) != None:
                scopes.append('function')
            elif model_end.match(line) != None:
                if n_model_ends > 0:
                    raise SBOError('Multiple embedded models (e.g. comp) not supported for SBO converter')
                if len(scopes) == 0:
                    raise RuntimeError('Unbalanced begin/end blocks')
                scope = scopes.pop()
                if scope == 'model':
                    n_model_ends += 1
                    model_end_index = n
                elif scope == 'function':
                    pass
                else:
                    raise RuntimeError('Unknown scope')
            else:
                # calculate leading whitespace
                ws = len(line) - len(line.lstrip(' '))
                if ws > n_leading_spaces and n_leading_spaces == 0:
                    n_leading_spaces = ws
        if n_model_starts != n_model_ends:
            raise RuntimeError('Antimony model begin/end blocks unbalanced - missing begin/end marker?')
        if n_model_starts > 1:
            raise SBOError('Multiple embedded models (e.g. comp) not supported for SBO converter')
        if n_model_ends > 1:
            raise SBOError('Multiple embedded models (e.g. comp) not supported for SBO converter')
        # add SBO terms right before the end
        lead_space = ' '*n_leading_spaces
        if model_end_index is not None:
            # get all sbo terms
            sbo_terms = self.getAllSBOTerms()
            if sbo_terms:
                lines[model_end_index:model_end_index] = ['', lead_space + '// SBO terms:'] + \
                    [lead_space + term for term in sbo_terms] + ['']
        return '\n'.join(lines)

    def getAllSBOTerms(self):
        """ Get a list of all SBO terms base on the SBML passed to the constructor. """
        comps = self.getCompartmentSBOTerms()
        species = self.getSpeciesSBOTerms()
        params = self.getParameterSBOTerms()
        rxns = self.getReactionSBOTerms()
        return comps + species + params + rxns

    def getCompartmentSBOTerms(self):
        return filterIfEmpty(['// - Compartment SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getCompartment(k) for k in range(self.model.getNumCompartments())) \
            if self.hasSBOTerm(e)])

    def getSpeciesSBOTerms(self):
        return filterIfEmpty(['// - Species SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getSpecies(k) for k in range(self.model.getNumSpecies())) \
            if self.hasSBOTerm(e)])

    def getParameterSBOTerms(self):
        return filterIfEmpty(['// - Parameter SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getParameter(k) for k in range(self.model.getNumParameters())) \
            if self.hasSBOTerm(e)])

    def getReactionSBOTerms(self):
        return filterIfEmpty(['// - Reaction SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getReaction(k) for k in range(self.model.getNumReactions())) \
            if self.hasSBOTerm(e)])

    def hasSBOTerm(self, elt):
        if elt.isSetSBOTerm():
            return True
        else:
            return False

    def createSBOTermStringForElt(self, elt):
        if elt.isSetSBOTerm():
            return elt.getId() + '.sboTerm = ' + 'SBO:{:07d};'.format(self.getSBOTermForElt(elt))
        else:
            return None

    def getSBOTermForElt(self, elt):
        if elt.isSetSBOTerm():
            return elt.getSBOTerm()
        else:
            raise RuntimeError('No SBO term set.')

    @classmethod
    def fromSBMLFile(cls, sbml_file):
        """ Construct from SBML file. """
        reader = libsbml.SBMLReader()
        doc = reader.readSBMLFromFile(sbml_file)
        return antimonySBOConverter(doc)

    @classmethod
    def fromSBMLString(cls, sbml_str):
        """ Construct from SBML string. """
        reader = libsbml.SBMLReader()
        doc = reader.readSBMLFromString(sbml_str)
        return antimonySBOConverter(doc)


class antimonySBOParser(object):
    def __init__(self, antimony_str):
        """Initialize from an Antimony string."""
        self.antimony_str = antimony_str

    def elideSBOTerms(self):
        """Remove SBO terms from self.antimony_str.

        :return: Antimony string without SBO terms."""

        self.sbo_map = {}

        model_start = re.compile(getModelStartRegex())
        n_model_starts = 0

        model_end = re.compile(getModelEndRegex())
        n_model_ends = 0
        model_end_index = None

        sbo_term = re.compile(getSBORegex())

        n_leading_spaces = 0

        lines = self.antimony_str.splitlines()

        out_lines = []
        for n,line in enumerate(lines):
            sbo_match = sbo_term.match(line)

            if model_start.match(line) != None:
                n_model_starts += 1
                out_lines.append(line)
            elif model_end.match(line) != None:
                if n_model_ends > 0:
                    raise SBOError('Multiple embedded models (e.g. comp) not supported for SBO converter')
                n_model_ends += 1
                model_end_index = n
                out_lines.append(line)
            elif sbo_term.match(line):
                elt_id = sbo_match.group(1)
                sbo = int(sbo_match.group(3))
                self.sbo_map[elt_id] = sbo
                # print('Match SBO term {}->{}'.format(elt_id,sbo))
            else:
                out_lines.append(line)
        if n_model_starts != n_model_ends:
            raise RuntimeError('Antimony model begin/end blocks unbalanced - missing begin/end marker?')
        if n_model_starts > 1:
            raise SBOError('Multiple embedded models (e.g. comp) not supported for SBO converter')
        if n_model_ends > 1:
            raise SBOError('Multiple embedded models (e.g. comp) not supported for SBO converter')

        return '\n'.join(out_lines)

    def addSBOsToSBML(self, sbml_str):
        """Add SBO terms to an SBML string. Must have called
        elideSBOTerms first to populate self.sbo_map."""

        reader = libsbml.SBMLReader()
        doc = reader.readSBMLFromString(sbml_str)
        if doc.getNumErrors() > 0:
            raise RuntimeError('Errors reading SBML')

        for elt_id,sbo in self.sbo_map.items():
            elt = doc.getElementBySId(elt_id)
            if elt is not None:
                # print('set {} -> {}'.format(elt.getId(), sbo))
                elt.setSBOTerm(sbo)

        writer = libsbml.SBMLWriter()
        out_sbml = writer.writeSBMLToString(doc)

        return out_sbml

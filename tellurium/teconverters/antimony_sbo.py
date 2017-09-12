"""
Helpers to work with SBO terms in antimony.
"""

from __future__ import print_function, division, absolute_import

import re
try:
    import tesbml as libsbml
except ImportError:
    import libsbml

from .antimony_regex import getModelStartRegex, getModelEndRegex

class antimonySBOConverter:
    def __init__(self, doc):
        """ Create an SBO converter

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

        model_end = re.compile(getModelEndRegex())
        n_model_ends = 0
        model_end_index = None

        n_leading_spaces = 0

        lines = antimony_str.splitlines()


        for n,line in enumerate(lines):
            if model_start.match(line) != None:
                n_model_starts += 1
            elif model_end.match(line) != None:
                if n_model_ends > 0:
                    raise RuntimeError('Multiple embedded models (e.g. comp) not supported for SBO converter')
                n_model_ends += 1
                model_end_index = n
            else:
                # calculate leading whitespace
                ws = len(line) - len(line.lstrip(' '))
                if ws > n_leading_spaces and n_leading_spaces == 0:
                    n_leading_spaces = ws
        if n_model_starts != n_model_ends:
            raise RuntimeError('Antimony model begin/end blocks unbalanced - missing begin/end marker?')
        if n_model_starts > 1:
            raise RuntimeError('Multiple embedded models (e.g. comp) not supported for SBO converter')
        if n_model_ends > 1:
            raise RuntimeError('Multiple embedded models (e.g. comp) not supported for SBO converter')
        # add SBO terms right before the end
        lead_space = ' '*n_leading_spaces
        if model_end_index is not None:
            # get all sbo terms
            sbo_terms = self.getAllSBOTerms()
            print(sbo_terms)
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
        return ['// - Compartment SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getCompartment(k) for k in range(self.model.getNumCompartments())) \
            if self.hasSBOTerm(e)]

    def getSpeciesSBOTerms(self):
        return ['// - Species SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getSpecies(k) for k in range(self.model.getNumSpecies())) \
            if self.hasSBOTerm(e)]

    def getParameterSBOTerms(self):
        return ['// - Parameter SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getParameter(k) for k in range(self.model.getNumParameters())) \
            if self.hasSBOTerm(e)]

    def getReactionSBOTerms(self):
        return ['// - Reaction SBO Terms:'] + \
            [self.createSBOTermStringForElt(e)
            for e in (self.model.getReaction(k) for k in range(self.model.getNumReactions())) \
            if self.hasSBOTerm(e)]

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

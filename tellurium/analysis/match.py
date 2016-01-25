"""
Utilities for matching species.
"""
from __future__ import print_function, division
import _annotations
import libsbml


def getMatchingSpecies(m1, m2, logging=False):
    """ Returns a list of species with matching annotations URIs for two models

    :param m1: first SBML model
    :type m1: libsbml.Model
    :param m2: second SBML model
    :type m2: libsbml.Model
    :param logging: log info
    :type logging: bool
    :return: returns list of chebi annotation information for matching species
    :rtype: list
    """
    if not isinstance(m1, libsbml.Model) or not isinstance(m2, libsbml.Model):
        raise Exception('Need to call with two libsbml.Model instances')

    matches = []
    for s1 in m1.species:
        for s2 in m2.species:
            match = _annotations.matchSpeciesChebi(s1, s2, logging=logging)
            if match:
                if len(match['exact']) or len(match['children']) or len(match['parents']):
                    matches.append(match)
    return matches


def printMatchingSpecies(matches):
    """ Prints the matches from :func:`getMatchingSpecies`-

    :param matches: matches from getMatchingSpecies
    :type matches: list
    """
    for match in matches:
        if len(match['exact']):
            print('%s exactly matches %s' % (match['exact'][0]['id'], match['id']))
        if len(match['parents']):
            print('%s %s %s' % (match['parents'][0]['id'], match['parents'][0]['data']['type'], match['id']))
        if len(match['children']):
            print('%s %s %s' % (match['children'][0]['id'], match['children'][0]['data']['type'], match['id']))


def getMatchingReactions(modelOrList, idToMatch):
    """ Returns a list of reactions that contains a reactant with the id to match.

    :param modelOrList: SBML Model or list of reactions
    :type modelOrList: libsbml.Model or list[libsbml.Reaction]
    :param idToMatch: reaction id for matching
    :type idToMatch: str
    :return: list of reactions
    :rtype: list
    """
    if isinstance(modelOrList, libsbml.Model):
        reactions = modelOrList.reactions
    else:
        reactions = modelOrList
    matches = []
    for r in reactions:
        for reactant in r.reactants:
            if reactant.getSpecies() == idToMatch:
                matches.append(r)
        for reactant in r.products:
            if reactant.getSpecies() == idToMatch:
                matches.append(r)
        for modifier in r.modifiers:
            if modifier.getSpecies() == idToMatch:
                matches.append(r)
    return matches

"""
Functions handling ontology annotations.
"""
from __future__ import print_function, division
import sys
import re
import bioservices


def getResourceUris(item):
    """ Get list of resource URIs for the given element.
    qualifierType = libsbml.BIOLOGICAL_QUALIFIER,
    biologicalQualifierType = libsbml.BQB_IS):

    :param item: sbml object
    :type item: SBase
    :return: list of resource URIs
    :rtype: list
    """
    uris = []
    for i in range(item.getNumCVTerms()):
        term = item.getCVTerm(i)
        for j in range(term.getNumResources()):
            uris.append(term.getResourceURI(j))
    return uris


def getChebiId(item):
    """ Returns the ChEBI ID from element.

    :param item: sbml object
    :type item: SBase
    :return: first chebi id in rdf annotations, None if no chebi annotation
    :rtype: str
    """
    uris = getResourceUris(item)
    chebiMatches = (re.match('.*(CHEBI:\d+)', uri) for uri in uris)
    chebiIds = [match.group(1) for match in chebiMatches if match]
    if len(chebiIds) > 0:
        return chebiIds[0]
    else:
        return None


def matchSpeciesChebi(s1, s2, logging=False):
    """ Match two Chebi identifiers.
    If matching returns the chebi information of the identifier.

    :param s1: first chebi id
    :type s1: str
    :param s2: second chebi id
    :type s2: str
    :param logging: log messages to console
    :type logging: bool
    :return: dictionary of chebi information, returns None if no match
    :rtype: dict
    """
    ch = bioservices.ChEBI()
    ch1 = getChebiId(s1)
    ch2 = getChebiId(s2)

    if not ch1 or not ch2:
        return None

    if logging:
        print('Comparing %s (%s) with %s (%s)' % (s1.getId(), ch1, s2.getId(), ch2))

    try:
        entry = ch.getCompleteEntity(ch1)

        exact = []
        if ch1 == ch2:
            exact.append({'id': s2.getId()})

        children = []
        if hasattr(entry, 'OntologyChildren'):
            for child in entry.OntologyChildren:
                if child['chebiId'] == ch2:
                    children.append({
                        'id': s2.getId(),
                        'data': child
                        })

        parents = []
        if (hasattr(entry, 'OntologyParents')):
            for parent in entry.OntologyParents:
                if parent['chebiId'] == ch2:
                    parents.append({
                        'id': s2.getId(),
                        'data': parent
                        })

        return {
            'id': s1.getId(),
            'chebi_name': entry.chebiAsciiName,
            'exact': exact,
            'children': children,
            'parents': parents
        }
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return None

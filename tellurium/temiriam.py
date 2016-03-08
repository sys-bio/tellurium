# -*- coding: utf-8 -*-
"""
Helper functions for MIRIAM and identifiers.org.

resolve the locations of:
urn:miriam:biomodels.db:BIOMD0000000003.xml

"""
from __future__ import print_function, division
import bioservices
import re


def getSBMLFromBiomodelsURN(urn):
    """
    Get the SBML from a given BioModels URN.
    Searches for a BioModels identifier in the given urn and retrieves the SBML from biomodels.
    :param urn:
    :type urn:
    :return: SBML string fro given model urn
    :rtype: str
    """
    pattern = "((BIOMD|MODEL)\d{10})|(BMID\d{12})"
    match = re.search(pattern, urn)
    mid = match.group(0)
    biomodels = bioservices.BioModels()
    sbml = biomodels.getModelSBMLById(mid)
    sbml = sbml.encode('utf8')
    return str(sbml)


if __name__ == "__main__":
    print("Get SBML from URN")
    urn = 'urn:miriam:biomodels.db:BIOMD0000000003'
    sbml = getSBMLFromBiomodelsURN(urn)
    print(sbml)

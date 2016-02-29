"""
Helper functions for MIRIAM.

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
    :return:
    :rtype:
    """
    pattern = "((BIOMD|MODEL)\d{10})|(BMID\d{12})"
    match = re.search(pattern, urn)
    mid = match.group(0)
    biomodels = bioservices.BioModels()
    return biomodels.getModelSBMLById(mid)



if __name__ == "__main__":
    urn = 'urn:miriam:biomodels.db:BIOMD0000000003.xml'
    sbml = getSBMLFromBiomodelsURN(urn)
    print(sbml)

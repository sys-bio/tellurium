# -*- coding: utf-8 -*-
"""
Helper functions for MIRIAM and identifiers.org.
"""
from __future__ import absolute_import, print_function
import re


def getSBMLFromBiomodelsURN(urn):
    """ Get SBML string from given BioModels URN.

    Searches for a BioModels identifier in the given urn and retrieves the SBML from biomodels.
    For example:
        urn:miriam:biomodels.db:BIOMD0000000003.xml

    :param urn:
    :return: SBML string for given model urn
    """
    pattern = "((BIOMD|MODEL)\d{10})|(BMID\d{12})"
    match = re.search(pattern, urn)
    mid = match.group(0)

    # py2 / py3
    try:
        import httplib
    except ImportError:
        import http.client as httplib

    conn = httplib.HTTPConnection("www.ebi.ac.uk", timeout=20)
    conn.request("GET", "/biomodels-main/download?mid=" + mid)
    r1 = conn.getresponse()
    # print(r1.status, r1.reason)
    sbml = r1.read()
    conn.close()

    # bytes array in py3
    try:
        sbml_str = sbml.decode("utf-8")
    except:
        sbml_str = str(sbml)
    return sbml_str


if __name__ == "__main__":
    print("Get SBML from URN")
    # urn = 'urn:miriam:biomodels.db:BIOMD0000000003'
    urn = 'urn:miriam:biomodels.db:BIOMD0000000139'
    sbml = getSBMLFromBiomodelsURN(urn)
    print(sbml)

    import roadrunner
    r = roadrunner.RoadRunner(sbml)
    print(r)

# -*- coding: utf-8 -*-
"""
Helper functions for MIRIAM and identifiers.org.
"""
from __future__ import absolute_import, print_function, unicode_literals
import re
import requests


def getSBMLFromBiomodelsURN(urn):
    """ Get SBML string from given BioModels URN.

    Searches for a BioModels identifier in the given urn and retrieves the SBML from biomodels.
    For example:
        urn:miriam:biomodels.db:BIOMD0000000003.xml

    Handles redirects of the download page.

    :param urn:
    :return: SBML string for given model urn
    """
    if ":" not in urn:
        raise ValueError("The URN", urn, "is not in the correct format: it must be divided by colons in a format such as 'urn:miriam:biomodels.db:BIOMD0000000003.xml'.")
    core = urn.split(":")[-1].split(".")[0]

    url = "https://www.ebi.ac.uk/biomodels/model/download/" + core + "?filename="+ core + "_url.xml"
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    sbml = response.content

    # bytes array in py3
    try:
        sbml_str = str(sbml.decode("utf-8"))
    except:
        sbml_str = str(sbml)

    return sbml_str

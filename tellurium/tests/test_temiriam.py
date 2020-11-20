"""
Testing temiriam module
"""
from __future__ import absolute_import, print_function
from six import string_types
import roadrunner
from tellurium import temiriam


def test_getSBMLFromBiomodelsURN1():
    """ Check that string is returned.

    :return:
    """
    urn = 'urn:miriam:biomodels.db:BIOMD0000000139'
    sbml = temiriam.getSBMLFromBiomodelsURN(urn)
    assert sbml is not None
    # check that string
    assert isinstance(sbml, string_types)


def test_getSBMLFromBiomodelsURN2():
    """ Check that model can be loaded in roadrunner.

    :return:
    """
    urn = 'urn:miriam:biomodels.db:BIOMD0000000139'
    sbml = temiriam.getSBMLFromBiomodelsURN(urn)

    print("*" * 80)
    print(type(sbml))
    print("*" * 80)
    print(sbml)
    print("*" * 80)

    r = roadrunner.RoadRunner(sbml)
    assert r is not None

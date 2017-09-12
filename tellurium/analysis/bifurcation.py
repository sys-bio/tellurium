"""
Utility classes for computing bifurcations.
"""
from __future__ import print_function, division, absolute_import

import os.path
from rrplugins import Plugin
from roadrunner import RoadRunner


def bifurcation(model, parameter, lowerBound, upperBound, maxPoints=5000, scanPositive=True):
    """Plot a bifurcation diagram.

    :param model:        A path to an SBML or Antimony file, or raw SBML or Antimony string.
    :param parameter:    The principal continuation parameter.
    :param lowerBound:   The lower bound of the continuation.
    :param upperBound:   The upper bound of the continuation.
    :param maxPoints:    The maximum number of points.
    :param scanPositive: Scan from lower to upper bound (direction is reversed if false).
    """

    if isinstance(model, RoadRunner):
        sbml = model.getSBML()
    elif os.path.exists(model) and os.path.isfile(model):
        # it's a file path
        if os.path.splitext(model)[1] == '.sb':
            # it's an Antimony file
            with open(model) as f:
                sbml = antimonyConverter.antimonyToSBML(f.read())
        elif os.path.splitext(model)[1] == '.txt':
            raise RuntimeError('File ending in ".txt" is ambiguous - pass an SBML file (.xml) or an Antimony file (.sb).')
        else:
            with open(model) as f:
                sbml = f.read()
    else:
        # check if it's Antimony source
        try:
            sbml = antimonyConverter.antimonyToSBML(model)
        except:
            # it better be SBML
            import tesbml as libsbml
            # this will throw if it's not SBML
            libsbml.readSBML(model)

    auto = Plugin('tel_auto2000')

    # Set SBML source
    auto.setProperty('SBML', sbml)

    # Set parameters
    auto.setProperty('ScanDirection', 'Positive' if scanPositive else 'Negative')
    auto.setProperty('PrincipalContinuationParameter', parameter)
    auto.setProperty('PCPLowerBound', lowerBound)
    auto.setProperty('PCPUpperBound', upperBound)

    # Set maximum numberof points
    auto.setProperty('NMX', maxPoints)

    # execute the plugin
    auto.execute()

    # plot Bifurcation diagram
    pts = auto.BifurcationPoints
    lbls = auto.BifurcationLabels
    biData = auto.BifurcationData
    return pts, lbls, biData


def plotBifurcation(model, parameter, lowerBound, upperBound, maxPoints=5000, scanPositive=True):
    """Plot a bifurcation diagram.

    :param model:        A path to an SBML or Antimony file, or raw SBML or Antimony string.
    :param parameter:    The principal continuation parameter.
    :param lowerBound:   The lower bound of the continuation.
    :param upperBound:   The upper bound of the continuation.
    :param maxPoints:    The maximum number of points.
    :param scanPositive: Scan from lower to upper bound (direction is reversed if false).
    """

    pts, lbls, biData = bifurcation(model, parameter, lowerBound, upperBound, maxPoints, scanPositive)
    biData.plotBifurcationDiagram(pts, lbls)

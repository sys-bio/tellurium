from __future__ import print_function, division, absolute_import

def getModelStartRegex():
    """ Return the regex string for Antimony model start. Matches whole line. """
    return r'^\s*\*?\s*model\s*[^()\s]+\s*(\([^)]*\))?\s*(//.*)?$'

def getFunctionStartRegex():
    """ Return the regex string for Antimony model start. Matches whole line. """
    return r'^\s*function\s*[^()\s]*\s*(\([^)]*\))?\s*$'

def getModelEndRegex():
    """ Return the regex string for Antimony model end. Matches whole line. """
    return r'^\s*end\s*$'

def getSBORegex():
    """ Return the regex string for Antimony model end. Matches whole line. """
    return r'^\s*([^.]+)\.sboTerm\s*=\s*(SBO:)?([0-9]+)\s*(;)?\s*$'

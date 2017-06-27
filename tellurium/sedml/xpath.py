"""
Some example code to work with xpath expressions.
"""

from __future__ import absolute_import, print_function
import sympy
import libsedml
import libsbml
import os
from tellurium.sedml.tesedml import SEDMLCodeFactory

fpath = os.path.join('_te_testcase_03', 'testcase_03.xml')
xpath = "/sbml:sbml/sbml:model/descendant::*[@id='S2']"
from lxml import etree
tree = etree.parse(fpath)

# If your XPath expression uses namespace prefixes, you must define them in a prefix mapping.
# To this end, pass a dictionary to the namespaces keyword argument that maps the namespace
# prefixes used in the XPath expression to namespace URIs:

# xpath
res = tree.xpath(xpath,
    namespaces={'sbml': "http://www.sbml.org/sbml/level3/version1/core"})
for r in res:
    print(r)
    print(r.tag)

"""
The return value types of XPath evaluations vary, depending on the XPath expression used:

    True or False, when the XPath expression has a boolean result
    a float, when the XPath expression has a numeric result (integer or float)
    a 'smart' string (as described below), when the XPath expression has a string result.
    a list of items, when the XPath expression has a list as result. The items may include Elements (also comments and processing instructions), strings and tuples. Text nodes and attributes in the result are returned as 'smart' string values. Namespace declarations are returned as tuples of strings: (prefix, URI).
"""




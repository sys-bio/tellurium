"""
Helper functions for evaluation of mathml expressions.
In this namespace all the possible names occuring in formula strings have to be defined.

In build in python are
    *, /, +, -
    and, or, not

"""
from __future__ import absolute_import, print_function, division

try:
    from builtins import range
except ImportError:
    pass  # not available in py2.7

from math import *
try:
    import tesbml as libsbml
except:
    import libsbml
import operator

def product(*args):
    return reduce(operator.mul, args, 1)

def sqr(x):
    return x*x

def root(a, b):
    return a**(1/b)

def xor(*args):
    foundZero = 0
    foundOne = 0
    for a in args:
        if not a:
           foundZero = 1
        else:
           foundOne = 1
    if foundZero and foundOne:
        return 1
    else:
        return 0

def piecewise(*args):
    Nargs = len(args)
    for k in range(0, Nargs-1, 2):
        if args[k+1]:
            return args[k]
    else:
        return args[Nargs-1]

"""
def pow(x, y):
    return x**y

def gt(a, b):
   if a > b:
   	  return 1
   else:
      return 0

def lt(a, b):
   if a < b:
   	  return 1
   else:
      return 0

def geq(a, b):
   if a >= b:
   	  return 1
   else:
      return 0

def leq(a, b):
   if a <= b:
   	  return 1
   else:
      return 0

def neq(a, b):
   if a != b:
   	  return 1
   else:
      return 0

def f_not(a):
   if a == 1:
   	  return 0
   else:
      return 1

def f_and(*args):
    for a in args:
       if a != 1:
          return 0
    return 1

def f_or(*args):
    for a in args:
       if a != 0:
          return  1
    return 0
"""

def evaluableMathML(astnode, variables={}, array=False):
    """ Create evaluable python string.

    """
    # replace variables with provided values
    for key, value in variables.items():
        astnode.replaceArgument(key, libsbml.parseFormula(str(value)))

    # get formula
    formula = libsbml.formulaToL3String(astnode)

    # <replacements>
    # FIXME: these are not exhaustive, but are improved with examples
    if array is False:
        # scalar
        formula = formula.replace("&&", 'and')
        formula = formula.replace("||", 'or')
    else:
        # np.array
        formula = formula.replace("max", 'np.nanmax')
        formula = formula.replace("min", 'np.nanmin')
        formula = formula.replace("sum", 'np.nansum')
        formula = formula.replace("product", 'np.prod')

    return formula


def evaluateMathML(astnode, variables={}, array=False):
    """ Evaluate MathML string with given set of variable and parameter values.

    :param astnode: astnode of MathML string
    :type astnode: libsbml.ASTNode
    :param variables: dictionary of var : value
    :type variables: dict
    :param parameters: dictionary of par : value
    :type parameters: dict
    :return: value of evaluated MathML
    :rtype: float
    """
    formula = evaluableMathML(astnode, variables=variables, array=array)
    print(formula)
    # return the evaluated formula
    return eval(formula)


if __name__ == "__main__":

    mathmlStr = """
           <math xmlns="http://www.w3.org/1998/Math/MathML">
                <piecewise>
                  <piece>
                    <cn type="integer"> 8 </cn>
                    <apply>
                      <lt/>
                      <ci> x </ci>
                      <cn type="integer"> 4 </cn>
                    </apply>
                  </piece>
                  <piece>
                    <cn> 0.1 </cn>
                    <apply>
                      <and/>
                      <apply>
                        <leq/>
                        <cn type="integer"> 4 </cn>
                        <ci> x </ci>
                      </apply>
                      <apply>
                        <lt/>
                        <ci> x </ci>
                        <cn type="integer"> 6 </cn>
                      </apply>
                    </apply>
                  </piece>
                  <otherwise>
                    <cn type="integer"> 8 </cn>
                  </otherwise>
                </piecewise>
              </math>
    """

    # evaluate the function with the values
    astnode = libsbml.readMathMLFromString(mathmlStr)

    y = 5
    res = evaluateMathML(astnode,
                         variables={'x': "y"})
    print('Result:', res)

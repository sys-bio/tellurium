"""
Helper functions for evaluation of mathml expressions.
"""
import libsbml

def pow(x, y):
    return x**y

def sqr(x):
    return x*x

def root(a, b):
    return a^(1/b)

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
    for k in xrange(0, Nargs-1, 2):
        if args[k+1]:
            return args[k]
    else:
        return args[Nargs-1]

"""
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

def evaluateMathML(mathml, variables={}, parameters={}):
    """ Evaluate MathML string with given set of variable and parameter values.

    :param mathml: MathML string
    :type mathml: str
    :param variables: dictionary of var : value
    :type variables: dict
    :param parameters: dictionary of par : value
    :type parameters: dict
    :return: value of evaluated MathML
    :rtype: float
    """

    ast = libsbml.readMathMLFromString(mathml)

    # replace variables with provided values
    for key, value in variables.iteritems():
        ast.replaceArgument(key, libsbml.parseFormula(str(value)))

    # replace parameters with provided values
    for key, value in parameters.iteritems():
        ast.replaceArgument(key, libsbml.parseFormula(str(value)))

    # get formula
    formula = libsbml.formulaToL3String(ast)

    # make replacements in formula
    formula = formula.replace("&&", 'and')
    formula = formula.replace("||", 'or')

    # return the evaluated formula
    return eval(formula)


if __name__ == "__main__":

    mathml = """
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
    res = evaluateMathML(mathml,
                         parameters={'x': 10.0})
    print('Result:', res)
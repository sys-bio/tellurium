"""
Helper functions for evaluation of mathml expressions
"""


astnode = libsbml.readMathMLFromString(mathml)
print(astnode)
# replace arguments
formula = libsbml.formulaToL3String(astnode)
print(formula)



if __name__ == "__main__":
    
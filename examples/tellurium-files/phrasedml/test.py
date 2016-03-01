from __future__ import print_function
import sympy
import libsedml
import libsbml
import os
from tellurium.sedml.tesedml import SEDMLCodeFactory

sbml_doc = libsbml.readSBMLFromFile(os.path.join('_te_testcase_03', 'testcase_03.xml'))
sedml_doc = libsedml.readSedMLFromFile(os.path.join('_te_testcase_03', 'experiment1.xml'))
print(sbml_doc)
print(sedml_doc)

sedml_model = sedml_doc.getModel("mod2")
print(sedml_model)

def applyComputeChange(sbml_doc, change):
    print('* Resolve target *')
    # TODO: resolve the xpath


    xpath =

    target = SEDMLCodeFactory.resolveTargetFromXPath()

    print('* Resolve variables *')
    for var in change.getListOfVariables():
        selection = SEDMLCodeFactory.resolveSelectionFromVariable(var)
        print(selection)
        # check if in SBML
        sbml_model = sbml_doc.getModel()
        sbase = sbml_model.getElementBySId(selection.id)
        print(sbase)




    print('* Set parameters in math *')
    astnode = change.getMath()
    print(astnode)

    for par in change.getListOfParameters():
        print(par.getId(), par.getName(), par.getValue())

    print('* Create initial assignment *')
    a = sbml_model.createInitialAssignment()
    a.setSymbol(sid)
    a.setMath(astnode)


for change in sedml_model.getListOfChanges():
    print(change)
    applyComputeChange(sbml_doc, change)


def _create_parameter(model, sid, unit, name, value, constant):
    p = model.createParameter()
    p.setId(sid)
    if name is not None:
        p.setName(name)
    if value is not None:
        p.setValue(value)
    p.setConstant(constant)
    return p

def ast_node_from_formula(model, formula):
    ast_node = libsbml.parseL3FormulaWithModel(formula, model)
    if not ast_node:
        warnings.warn('Formula could not be parsed:', formula)
        warnings.warn(libsbml.getLastParseL3Error())
    return ast_node
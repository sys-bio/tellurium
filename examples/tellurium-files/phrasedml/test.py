from __future__ import print_function
import sympy
import libsedml
import libsbml
import os
import tellurium.sedml.tesedml as tesedml

sbml_doc = libsbml.readSBMLFromFile(os.path.join('_te_testcase_03', 'testcase_03.xml'))
sedml_doc = libsedml.readSedMLFromFile(os.path.join('_te_testcase_03', 'experiment1.xml'))
print(sbml_doc)
print(sedml_doc)

sedml_model = sedml_doc.getModel("mod2")
print(sedml_model)

def applyComputeChange(sbml_doc, change):
    print('* Resolve variables *')
    for var in change.getListOfVariables():
        selection = tesedml.SEDMLCodeFactory.resolveSelectionFromVariable(var)
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
    


for change in sedml_model.getListOfChanges():
    print(change)
    applyComputeChange(sbml_doc, change)



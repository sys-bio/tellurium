"""
Template filters for rendering SEDML

Additional functionality for templates like displaying the annotations and proper rendering
of units.
"""

import libsedml

filters = [
    'SEDML_isSBMLModel',
    'SEDML_isCellMLModel',
]


def loadSEDMLModel(model, workingDir):
    """ Function for loading the sedml models.
    Loads the model and applies the changes.
    """
    pass
    """
    for i in range(0, currentModel.getNumChanges()):
        aChange = currentModel.getChange(i)
        if aChange.getElementName() == "changeAttribute":
            newValue = aChange.getNewValue()
            variableName = aChange.getTarget()
            if (("model" in variableName) and ("parameter" in variableName)):
                variableName = variableName.rsplit("id=\'",1)[1]
                variableName = variableName.rsplit("\'",1)[0]
                aStr = rrName + ".model[\"" + variableName + "\"] = " + newValue    # set amount
                listOfChanges.append(aStr)
                print(aStr)
            elif (("model" in variableName) and ("species" in variableName)):
                variableName = variableName.rsplit("id=\'",1)[1]
                variableName = variableName.rsplit("\'",1)[0]
                aStr = rrName + ".model[\"init([" + variableName + "])\"] = " + newValue    # set amount
                #aStr = rrName + ".model[\"[" + variableName + "]\"] = " + newValue    # set amount
                listOfChanges.append(aStr)
                print(aStr)
            else:
                print("# Unsupported changeAttribute target " + variableName)
                return          # nothing to do repeatedly since our change is bad
        else:
            aStr = "# Unsupported change " + aChange.getElementName() + " for model " + currentModel.getId()
            print(aStr)
            return
    """


# <CHANGE>
# SEDML_CHANGE_ATTRIBUTE = _libsedml.SEDML_CHANGE_ATTRIBUTE
# SEDML_CHANGE_REMOVEXML = _libsedml.SEDML_CHANGE_REMOVEXML
# SEDML_CHANGE_COMPUTECHANGE = _libsedml.SEDML_CHANGE_COMPUTECHANGE
# SEDML_CHANGE_ADDXML = _libsedml.SEDML_CHANGE_ADDXML
# SEDML_CHANGE_CHANGEXML = _libsedml.SEDML_CHANGE_CHANGEXML

def SEDML_isSBMLModel(model):
    return model.getLanguage().endswith('sbml')

def SEDML_isCellMLModel(model):
    return model.getLanguage().endswith('cellml')


# <SIMULATION>
# SEDML_SIMULATION = _libsedml.SEDML_SIMULATION
# SEDML_SIMULATION_ALGORITHM = _libsedml.SEDML_SIMULATION_ALGORITHM
# SEDML_SIMULATION_UNIFORMTIMECOURSE = _libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE
# SEDML_SIMULATION_ALGORITHM_PARAMETER = _libsedml.SEDML_SIMULATION_ALGORITHM_PARAMETER
# SEDML_SIMULATION_ONESTEP = _libsedml.SEDML_SIMULATION_ONESTEP
# SEDML_SIMULATION_STEADYSTATE = _libsedml.SEDML_SIMULATION_STEADYSTATE

def SEDML_isOneStepSimulation(simulation):
    return simulation.getTypeCode() == libsedml.SEDML_SIMULATION_ONESTEP


def SEDML_isCellMLModel(model):
    return model.getLanguage().endswith('cellml')


# <DATAGENERATOR>
# SEDML_DATAGENERATOR = _libsedml.SEDML_DATAGENERATOR

# <TASK>
# SEDML_TASK = _libsedml.SEDML_TASK
# SEDML_TASK_SUBTASK = _libsedml.SEDML_TASK_SUBTASK
# SEDML_TASK_SETVALUE = _libsedml.SEDML_TASK_SETVALUE
# SEDML_TASK_REPEATEDTASK = _libsedml.SEDML_TASK_REPEATEDTASK

# <OUTPUT>
# SEDML_OUTPUT_DATASET = _libsedml.SEDML_OUTPUT_DATASET
# SEDML_OUTPUT_CURVE = _libsedml.SEDML_OUTPUT_CURVE
# SEDML_OUTPUT_SURFACE = _libsedml.SEDML_OUTPUT_SURFACE
# SEDML_OUTPUT_REPORT = _libsedml.SEDML_OUTPUT_REPORT
# SEDML_OUTPUT_PLOT2D = _libsedml.SEDML_OUTPUT_PLOT2D
# SEDML_OUTPUT_PLOT3D = _libsedml.SEDML_OUTPUT_PLOT3D

# <RANGE>
# SEDML_RANGE = _libsedml.SEDML_RANGE
# SEDML_RANGE_UNIFORMRANGE = _libsedml.SEDML_RANGE_UNIFORMRANGE
# SEDML_RANGE_VECTORRANGE = _libsedml.SEDML_RANGE_VECTORRANGE
# SEDML_RANGE_FUNCTIONALRANGE = _libsedml.SEDML_RANGE_FUNCTIONALRANGE



doc = libsedml.SedDocument()
doc.
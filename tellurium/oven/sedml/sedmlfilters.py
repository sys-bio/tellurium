"""
Template filters for rendering SEDML

Additional functionality for templates like displaying the annotations and proper rendering
of units.
"""

import libsedml

filters = [
    'SEDML_isSBMLModel',
    'SEDML_isCellMLModel',
    'SEDML_isOneStepSimulation',
    'SEDML_isSteadyStateSimulation',
    'SEDML_isUniformTimecourseSimulation',
]


def SEDML_isSBMLModel(model):
    return model.getLanguage().endswith('sbml')

def SEDML_isCellMLModel(model):
    return model.getLanguage().endswith('cellml')

def SEDML_isOneStepSimulation(simulation):
    return simulation.getTypeCode() == libsedml.SEDML_SIMULATION_ONESTEP

def SEDML_isUniformTimecourseSimulation(simulation):
    return simulation.getTypeCode() == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE

def SEDML_isSteadyStateSimulation(simulation):
    return simulation.getTypeCode() == libsedml.SEDML_SIMULATION_STEADYSTATE



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

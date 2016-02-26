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

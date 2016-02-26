"""
    tellurium 1.3.1

    auto-generated code (2016-02-26T11:10:53)
        sedmlDoc: L1V1          workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml
        inputType: SEDML_FILE

"""
from __future__ import print_function, division
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import libsedml
import os.path

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - Application0 (Application0)
#  - Application0_0 (Application0 modified)

# Model <Application0>
Application0 = te.loadSBMLModel(os.path.join(workingDir, '../models/app2sim.xml'))

# Model <Application0_0>
#   Change: <libsedml.SedChangeAttribute; proxy of <Swig Object of type 'SedChangeAttribute_t *' at 0x7f3f4a1f8750> >
Application0_0 = te.loadSBMLModel(os.path.join(workingDir, '../models/app2sim.xml'))
# /sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='s1'] 10.0
Application0_0['init([s1])'] = 10.0

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task_0_0 (task_0_0)
#  - task_0_1 (task_0_1)

# Task <task_0_0>
task_0_0 = [None]
Application0.setIntegrator('cvode')
Application0.timeCourseSelections = ['[s0]', '[s1]', 'time']
task_0_0[0] = Application0.simulate(start=0.0, end=20.0, steps=1000)

# Task <task_0_1>
task_0_1 = [None]
Application0_0.setIntegrator('cvode')
Application0_0.timeCourseSelections = ['[s0]', '[s1]', 'time']
task_0_1[0] = Application0_0.simulate(start=0.0, end=30.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time_task_0_0 (time_task_0_0)
#  - dataGen_task_0_0_s0 (dataGen_task_0_0_s0)
#  - dataGen_task_0_0_s1 (dataGen_task_0_0_s1)
#  - time_task_0_1 (time_task_0_1)
#  - dataGen_task_0_1_s0 (dataGen_task_0_1_s0)
#  - dataGen_task_0_1_s1 (dataGen_task_0_1_s1)

# DataGenerator <time_task_0_0>
time_task_0_0 = [sim['time'] for sim in task_0_0]

# DataGenerator <dataGen_task_0_0_s0>
dataGen_task_0_0_s0 = [sim['[s0]'] for sim in task_0_0]

# DataGenerator <dataGen_task_0_0_s1>
dataGen_task_0_0_s1 = [sim['[s1]'] for sim in task_0_0]

# DataGenerator <time_task_0_1>
time_task_0_1 = [sim['time'] for sim in task_0_1]

# DataGenerator <dataGen_task_0_1_s0>
dataGen_task_0_1_s0 = [sim['[s0]'] for sim in task_0_1]

# DataGenerator <dataGen_task_0_1_s1>
dataGen_task_0_1_s1 = [sim['[s1]'] for sim in task_0_1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot2d_Simulation0 (Application0plots)
#  - plot2d_Simulation1 (Application0plots)

# Output <plot2d_Simulation0>

# Output <plot2d_Simulation1>


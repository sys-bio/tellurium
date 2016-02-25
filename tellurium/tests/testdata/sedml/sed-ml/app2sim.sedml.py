"""
    tellurium 1.3.1

    auto-generated code (2016-02-25T13:51:35)
        sedmlDoc: L1V1          workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml
        inputType: SEDML_FILE

    TODO: add code for extracting sedx archive in working directory

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
#   Change: <libsedml.SedChangeAttribute; proxy of <Swig Object of type 'SedChangeAttribute_t *' at 0x7f4f3dd61150> >
Application0_0 = te.loadSBMLModel(os.path.join(workingDir, '../models/app2sim.xml'))
# /sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='s1'] 10.0
Application0_0['init([s1])'] = 10.0

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task_0_0 (task_0_0)
#  - task_0_1 (task_0_1)

# Task <task_0_0>
# Task <task_0_1>

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
# DataGenerator <dataGen_task_0_0_s0>
# DataGenerator <dataGen_task_0_0_s1>
# DataGenerator <time_task_0_1>
# DataGenerator <dataGen_task_0_1_s0>
# DataGenerator <dataGen_task_0_1_s1>

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot2d_Simulation0 (Application0plots)
#  - plot2d_Simulation1 (Application0plots)

# Output <plot2d_Simulation0>
# Output <plot2d_Simulation1>

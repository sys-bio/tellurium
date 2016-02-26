"""
    tellurium 1.3.1

    auto-generated code (2016-02-26T09:10:18)
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
#  - repressor_activator_oscillations (repressor_activator_oscillations)

# Model <repressor_activator_oscillations>
repressor_activator_oscillations = te.loadSBMLModel(os.path.join(workingDir, '../models/BioModel1_repressor_activator_oscillations.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task_0_0 (task_0_0)
#  - repeatedTask_0_0 (repeatedTask_0_0)

# Task <task_0_0>
repressor_activator_oscillations.setIntegrator('cvode')
repressor_activator_oscillations.timeCourseSelections = []
task_0_0 = repressor_activator_oscillations.simulate(start=0.0, end=200.0, steps=400)

# Task <repeatedTask_0_0>
__range = [0.20000000000000001, 0.60000000000000009, 1.0]
repeatedTask_0_0 = [None] * len(__range)
for k, value in enumerate(__range):
    repressor_activator_oscillations.reset()
    repressor_activator_oscillations['common_delta_A'] = value
    repressor_activator_oscillations.setIntegrator('cvode')
    repressor_activator_oscillations.timeCourseSelections = []
    repeatedTask_0_0[k] = repressor_activator_oscillations.simulate(start=0.0, end=200.0, steps=400)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time_repeatedTask_0_0 (time_repeatedTask_0_0)
#  - dataGen_repeatedTask_0_0_mRNA_R (dataGen_repeatedTask_0_0_mRNA_R)
#  - dataGen_repeatedTask_0_0_A (dataGen_repeatedTask_0_0_A)
#  - dataGen_repeatedTask_0_0_R (dataGen_repeatedTask_0_0_R)
#  - dataGen_repeatedTask_0_0_PrmA (dataGen_repeatedTask_0_0_PrmA)
#  - dataGen_repeatedTask_0_0_PrmR (dataGen_repeatedTask_0_0_PrmR)
#  - dataGen_repeatedTask_0_0_C (dataGen_repeatedTask_0_0_C)
#  - dataGen_repeatedTask_0_0_PrmA_bound (dataGen_repeatedTask_0_0_PrmA_bound)
#  - dataGen_repeatedTask_0_0_PrmR_bound (dataGen_repeatedTask_0_0_PrmR_bound)
#  - dataGen_repeatedTask_0_0_mRNA_A_ (dataGen_repeatedTask_0_0_mRNA_A_)

# DataGenerator <time_repeatedTask_0_0>

# DataGenerator <dataGen_repeatedTask_0_0_mRNA_R>

# DataGenerator <dataGen_repeatedTask_0_0_A>

# DataGenerator <dataGen_repeatedTask_0_0_R>

# DataGenerator <dataGen_repeatedTask_0_0_PrmA>

# DataGenerator <dataGen_repeatedTask_0_0_PrmR>

# DataGenerator <dataGen_repeatedTask_0_0_C>

# DataGenerator <dataGen_repeatedTask_0_0_PrmA_bound>

# DataGenerator <dataGen_repeatedTask_0_0_PrmR_bound>

# DataGenerator <dataGen_repeatedTask_0_0_mRNA_A_>

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot2d_scan_for_delta_A (repressor_activator_oscillationsplots)

# Output <plot2d_scan_for_delta_A>


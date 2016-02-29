"""
    tellurium 1.3.1

<<<<<<< HEAD
    auto-generated code (2016-02-29T08:07:17)
=======
    auto-generated code (2016-02-26T23:20:06)
>>>>>>> e3b2b99f654b459c1a71719ab70ab85555d780ce
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml
    inputType: SEDML_FILE
"""
from __future__ import print_function, division
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import pandas
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
task_0_0 = [None]
repressor_activator_oscillations.setIntegrator('cvode')
repressor_activator_oscillations.timeCourseSelections = []
task_0_0[0] = repressor_activator_oscillations.simulate(start=0.0, end=200.0, steps=400)

# Task <repeatedTask_0_0>
__range_repeatedTask_0_0 = [0.20000000000000001, 0.60000000000000009, 1.0]
repeatedTask_0_0 = [None] * len(__range_repeatedTask_0_0)
for k, value in enumerate(__range_repeatedTask_0_0):
    repressor_activator_oscillations.reset()
    repressor_activator_oscillations['common_delta_A'] = value
    repressor_activator_oscillations.setIntegrator('cvode')
    repressor_activator_oscillations.timeCourseSelections = ['[mRNA_A_]', '[PrmR]', '[PrmA_bound]', '[C]', '[PrmA]', 'time', '[A]', '[mRNA_R]', '[R]', '[PrmR_bound]']
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
time_repeatedTask_0_0 = [sim['time'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_mRNA_R>
dataGen_repeatedTask_0_0_mRNA_R = [sim['[mRNA_R]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_A>
dataGen_repeatedTask_0_0_A = [sim['[A]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_R>
dataGen_repeatedTask_0_0_R = [sim['[R]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_PrmA>
dataGen_repeatedTask_0_0_PrmA = [sim['[PrmA]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_PrmR>
dataGen_repeatedTask_0_0_PrmR = [sim['[PrmR]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_C>
dataGen_repeatedTask_0_0_C = [sim['[C]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_PrmA_bound>
dataGen_repeatedTask_0_0_PrmA_bound = [sim['[PrmA_bound]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_PrmR_bound>
dataGen_repeatedTask_0_0_PrmR_bound = [sim['[PrmR_bound]'] for sim in repeatedTask_0_0]

# DataGenerator <dataGen_repeatedTask_0_0_mRNA_A_>
dataGen_repeatedTask_0_0_mRNA_A_ = [sim['[mRNA_A_]'] for sim in repeatedTask_0_0]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot2d_scan_for_delta_A (repressor_activator_oscillationsplots)

# Output <plot2d_scan_for_delta_A>
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_mRNA_R[k], color='b', linewidth=1.5, label='[mRNA_R]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_mRNA_R[k], color='b', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_A[k], color='g', linewidth=1.5, label='[A]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_A[k], color='g', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_R[k], color='r', linewidth=1.5, label='[R]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_R[k], color='r', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmA[k], color='c', linewidth=1.5, label='[PrmA]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmA[k], color='c', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmR[k], color='m', linewidth=1.5, label='[PrmR]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmR[k], color='m', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_C[k], color='y', linewidth=1.5, label='[C]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_C[k], color='y', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmA_bound[k], color='k', linewidth=1.5, label='[PrmA_bound]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmA_bound[k], color='k', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmR_bound[k], color='b', linewidth=1.5, label='[PrmR_bound]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_PrmR_bound[k], color='b', linewidth=1.5)
for k in range(len(time_repeatedTask_0_0)):
    if k==0:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_mRNA_A_[k], color='g', linewidth=1.5, label='[mRNA_A_]')
    else:
        plt.plot(time_repeatedTask_0_0[k], dataGen_repeatedTask_0_0_mRNA_A_[k], color='g', linewidth=1.5)
plt.title('plot2d_scan_for_delta_A')
plt.legend()
plt.show()

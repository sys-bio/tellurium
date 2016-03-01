"""
    tellurium 1.3.1

    auto-generated code (2016-03-01T18:29:41)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmp6r1_7A_sedml/_te_parameterScan1D
    inputType: COMBINE_FILE
"""
from __future__ import print_function, division
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import pandas
import os.path

workingDir = '/tmp/tmp6r1_7A_sedml/_te_parameterScan1D'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'parameterScan1D.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
task0 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = []
task0[0] = model1.simulate(start=0.0, end=20.0, steps=1000)

# Task <task1>
__range__vector_for_J0_v0 = [8.0, 4.0, 0.40000000000000002]
task1 = [None]*len(__range__vector_for_J0_v0)
for k in range(len(__range__vector_for_J0_v0)):
    model1.reset()
    __value__vector_for_J0_v0 = __range__vector_for_J0_v0[k]
    model1['J0_v0'] = __value__vector_for_J0_v0
    model1.setIntegrator('cvode')
    model1.timeCourseSelections = ['S2', 'S1', 'time']
    task1[k] = model1.simulate(start=0.0, end=20.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
plot_0_0_0 = [sim['time'] for sim in task1]

# DataGenerator <plot_0_0_1>
plot_0_0_1 = [sim['S1'] for sim in task1]

# DataGenerator <plot_0_1_1>
plot_0_1_1 = [sim['S2'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot_0>
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5, label='S1-plot_0_0_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5, label='S2-plot_0_1_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5)
plt.title('plot_0')
plt.legend()
plt.show()


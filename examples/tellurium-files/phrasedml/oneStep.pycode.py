"""
    tellurium 1.3.1

    auto-generated code (2016-03-01T18:59:02)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpZoDFzl_sedml/_te_oneStep
    inputType: COMBINE_FILE
"""
from __future__ import print_function, division
import tellurium as te
from tellurium.sedml.mathml import *
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import pandas
import os.path

workingDir = '/tmp/tmpZoDFzl_sedml/_te_oneStep'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'oneStep.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
task0 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = []
task0[0] = model1.simulate(start=0.0, end=0.1, points=2)

# Task <task1>
__range__x = list(np.linspace(start=0.0, stop=10.0, num=101))
task1 = [None]*len(__range__x)
for k in range(len(__range__x)):
    __value__x = __range__x[k]
    model1['J0_v0'] = piecewise(8, __value__x < 4, 0.1, (4 <= __value__x) and (__value__x < 6), 8)
    model1.setIntegrator('cvode')
    model1.timeCourseSelections = ['S2', 'S1', 'J0_v0', 'time']
    task1[k] = model1.simulate(start=0.0, end=0.1, points=2)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
plot_0_0_0 = [sim['time'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_0_0 = [np.cumsum(plot_0_0_0)]

# DataGenerator <plot_0_0_1>
plot_0_0_1 = [sim['S1'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_0_1 = [np.concatenate(plot_0_0_1)]

# DataGenerator <plot_0_1_1>
plot_0_1_1 = [sim['S2'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_1_1 = [np.concatenate(plot_0_1_1)]

# DataGenerator <plot_0_2_1>
plot_0_2_1 = [sim['J0_v0'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_2_1 = [np.concatenate(plot_0_2_1)]

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
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5, label='J0_v0-plot_0_2_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5)
plt.title('plot_0')
plt.legend()
plt.show()


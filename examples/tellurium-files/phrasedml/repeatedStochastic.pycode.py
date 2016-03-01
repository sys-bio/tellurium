"""
    tellurium 1.3.1

    auto-generated code (2016-03-01T18:41:45)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpyasJBt_sedml/_te_repeatedStochastic
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

workingDir = '/tmp/tmpyasJBt_sedml/_te_repeatedStochastic'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'repeatedStochastic.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
task0 = [None]
model1.setIntegrator('gillespie')
model1.timeCourseSelections = []
task0[0] = model1.simulate(start=0.0, end=4000.0, steps=1000)

# Task <task1>
__range__x = list(np.linspace(start=0.0, stop=10.0, num=11))
task1 = [None]*len(__range__x)
for k in range(len(__range__x)):
    model1.reset()
    __value__x = __range__x[k]
    model1.setIntegrator('gillespie')
    model1.timeCourseSelections = ['MKKK', 'MKK_P', 'MAPK', 'MKK', 'MKKK_P', 'time', 'MAPK_P', 'MAPK_PP']
    task1[k] = model1.simulate(start=0.0, end=4000.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
plot_0_0_0 = [sim['time'] for sim in task1]

# DataGenerator <plot_0_0_1>
plot_0_0_1 = [sim['MAPK'] for sim in task1]

# DataGenerator <plot_0_1_1>
plot_0_1_1 = [sim['MAPK_P'] for sim in task1]

# DataGenerator <plot_0_2_1>
plot_0_2_1 = [sim['MAPK_PP'] for sim in task1]

# DataGenerator <plot_0_3_1>
plot_0_3_1 = [sim['MKK'] for sim in task1]

# DataGenerator <plot_0_4_1>
plot_0_4_1 = [sim['MKK_P'] for sim in task1]

# DataGenerator <plot_0_5_1>
plot_0_5_1 = [sim['MKKK'] for sim in task1]

# DataGenerator <plot_0_6_1>
plot_0_6_1 = [sim['MKKK_P'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot_0>
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5, label='MAPK-plot_0_0_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5, label='MAPK_P-plot_0_1_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5, label='MAPK_PP-plot_0_2_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_3_1[k], '-o', color='c', linewidth=1.5, label='MKK-plot_0_3_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_3_1[k], '-o', color='c', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_4_1[k], '-o', color='m', linewidth=1.5, label='MKK_P-plot_0_4_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_4_1[k], '-o', color='m', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_5_1[k], '-o', color='y', linewidth=1.5, label='MKKK-plot_0_5_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_5_1[k], '-o', color='y', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_6_1[k], '-o', color='k', linewidth=1.5, label='MKKK_P-plot_0_6_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_6_1[k], '-o', color='k', linewidth=1.5)
plt.title('plot_0')
plt.legend()
plt.show()


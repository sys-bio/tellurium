"""
    tellurium 1.3.1

    auto-generated code (2016-03-02T09:25:39)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpHFaF4X_sedml/_te_testcase_04
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

workingDir = '/tmp/tmpHFaF4X_sedml/_te_testcase_04'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_04.xml'))
# Model <mod2>
mod2 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_04.xml'))
__var__S1 = mod2['S1']
mod2['S2'] = __var__S1 + 4
# Model <mod3>
mod3 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_04.xml'))
__var__S1 = mod3['S1']
mod3['S2'] = __var__S1 + 4
# /sbml:sbml/sbml:model/listOfSpecies/species[@id='S1']/@initialConcentration 10
mod3['init([S1])'] = 10

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
task1 = [None]
mod1.setIntegrator('cvode')
mod1.timeCourseSelections = ['S2', 'S1', 'time']
task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

# Task <task2>
task2 = [None]
mod2.setIntegrator('cvode')
mod2.timeCourseSelections = ['S2', 'S1']
task2[0] = mod2.simulate(start=0.0, end=10.0, steps=100)

# Task <task3>
task3 = [None]
mod2.setIntegrator('cvode')
mod2.timeCourseSelections = ['S2', 'S1']
task3[0] = mod2.simulate(start=0.0, end=10.0, steps=100)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task1_____time = [sim['time'] for sim in task1]
plot_0_0_0 = __var__task1_____time

# DataGenerator <plot_0_0_1>
__var__task1_____S1 = [sim['S1'] for sim in task1]
plot_0_0_1 = __var__task1_____S1

# DataGenerator <plot_0_1_1>
__var__task1_____S2 = [sim['S2'] for sim in task1]
plot_0_1_1 = __var__task1_____S2

# DataGenerator <plot_0_2_1>
__var__task2_____S1 = [sim['S1'] for sim in task2]
plot_0_2_1 = __var__task2_____S1

# DataGenerator <plot_0_3_1>
__var__task2_____S2 = [sim['S2'] for sim in task2]
plot_0_3_1 = __var__task2_____S2

# DataGenerator <plot_0_4_1>
__var__task3_____S1 = [sim['S1'] for sim in task3]
plot_0_4_1 = __var__task3_____S1

# DataGenerator <plot_0_5_1>
__var__task3_____S2 = [sim['S2'] for sim in task3]
plot_0_5_1 = __var__task3_____S2

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
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5, label='S1-plot_0_2_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_3_1[k], '-o', color='c', linewidth=1.5, label='S2-plot_0_3_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_3_1[k], '-o', color='c', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_4_1[k], '-o', color='m', linewidth=1.5, label='S1-plot_0_4_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_4_1[k], '-o', color='m', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_5_1[k], '-o', color='y', linewidth=1.5, label='S2-plot_0_5_1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_5_1[k], '-o', color='y', linewidth=1.5)
plt.title('plot_0')
plt.legend()
plt.show()


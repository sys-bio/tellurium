"""
    tellurium 1.3.1

    auto-generated code (2016-03-01T17:47:01)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpIvAza2_sedml/_te_testcase_03
    inputType: COMBINE_FILE
"""
from __future__ import print_function, division
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import libsbml
import pandas
import os.path

workingDir = '/tmp/tmpIvAza2_sedml/_te_testcase_03'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - mod1 
#  - mod2 

# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_03.xml'))
# Model <mod2>
mod2 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_03.xml'))
__var__S1 = 5
mod2['S2'] = __var__S1 + 4

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 
#  - task2 

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

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - plot_0_0_0 (task1.time)
#  - plot_0_0_1 (task1.S1)
#  - plot_0_1_1 (task1.S2)
#  - plot_0_2_1 (task2.S1)
#  - plot_0_3_1 (task2.S2)

# DataGenerator <plot_0_0_0>
plot_0_0_0 = [sim['time'] for sim in task1]

# DataGenerator <plot_0_0_1>
plot_0_0_1 = [sim['S1'] for sim in task1]

# DataGenerator <plot_0_1_1>
plot_0_1_1 = [sim['S2'] for sim in task1]

# DataGenerator <plot_0_2_1>
plot_0_2_1 = [sim['S1'] for sim in task2]

# DataGenerator <plot_0_3_1>
plot_0_3_1 = [sim['S2'] for sim in task2]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot_0 (Example plot)

# Output <plot_0>
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5, label='S1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5, label='S2')
    else:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5, label='S1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_3_1[k], '-o', color='c', linewidth=1.5, label='S2')
    else:
        plt.plot(plot_0_0_0[k], plot_0_3_1[k], '-o', color='c', linewidth=1.5)
plt.title('plot_0')
plt.legend()
plt.show()


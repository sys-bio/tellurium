"""
    tellurium 1.3.1

    auto-generated code (2016-03-01T17:15:32)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpfcRzEC_sedml/_te_testcase_02
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

workingDir = '/tmp/tmpfcRzEC_sedml/_te_testcase_02'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - model0 
#  - model1 

# Model <model0>
model0 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_02.xml'))
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_02.xml'))
# /sbml:sbml/sbml:model/listOfSpecies/species[@id='S1']/@initialConcentration 5
model1['init([S1])'] = 5

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task0 
#  - task1 

# Task <task0>
task0 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = []
task0[0] = model1.simulate(start=0.0, end=10.0, steps=100)

# Task <task1>
__range__uniform_linear_for_k1 = list(np.linspace(start=0.0, stop=5.0, num=6))
task1 = [None]*len(__range__uniform_linear_for_k1)
for k in range(len(__range__uniform_linear_for_k1)):
    model1.reset()
    __value__uniform_linear_for_k1 = __range__uniform_linear_for_k1[k]
    model1['k1'] = __value__uniform_linear_for_k1
    model1.setIntegrator('cvode')
    model1.timeCourseSelections = ['S2', 'S1', 'time']
    task1[k] = model1.simulate(start=0.0, end=10.0, steps=100)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - plot_0_0_0 (task1.time)
#  - plot_0_0_1 (task1.S1)
#  - plot_0_1_1 (task1.S2)

# DataGenerator <plot_0_0_0>
plot_0_0_0 = [sim['time'] for sim in task1]

# DataGenerator <plot_0_0_1>
plot_0_0_1 = [sim['S1'] for sim in task1]

# DataGenerator <plot_0_1_1>
plot_0_1_1 = [sim['S2'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot_0 

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
plt.title('plot_0')
plt.legend()
plt.show()


"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T16:36:05)
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
#  - model1 
#  - model2 

# Model <model1>
import tellurium.temiriam as temiriam
__model1_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000012')
model1 = te.loadSBMLModel(__model1_sbml)
# Model <model2>
import tellurium.temiriam as temiriam
__model2_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000012')
model2 = te.loadSBMLModel(__model2_sbml)
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id="ps_a"]/@value 0.013
model2['ps_a'] = 0.013
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id="ps_0"]/@value 1.3e-5
model2['ps_0'] = 1.3e-5

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 
#  - task2 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[Z]', '[X]', '[Y]', 'time']
task1[0] = model1.simulate(start=0.0, end=500.0, steps=1000)

# Task <task2>
task2 = [None]
model2.setIntegrator('cvode')
model2.timeCourseSelections = ['[X]', '[Y]', '[Z]']
task2[0] = model2.simulate(start=0.0, end=500.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (time)
#  - X (X)
#  - Y (Y)
#  - Z (Z)
#  - X1 (X1)
#  - Y1 (Y1)
#  - Z1 (Z1)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <X>
X = [sim['[X]'] for sim in task1]

# DataGenerator <Y>
Y = [sim['[Y]'] for sim in task1]

# DataGenerator <Z>
Z = [sim['[Z]'] for sim in task1]

# DataGenerator <X1>
X1 = [sim['[X]'] for sim in task2]

# DataGenerator <Y1>
Y1 = [sim['[Y]'] for sim in task2]

# DataGenerator <Z1>
Z1 = [sim['[Z]'] for sim in task2]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (BM 12)
#  - plot2 (BM 12 (Changed))

# Output <plot1>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], X[k], color='b', linewidth=1.5, label='[X]')
    else:
        plt.plot(time[k], X[k], color='b', linewidth=1.5)
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Y[k], color='g', linewidth=1.5, label='[Y]')
    else:
        plt.plot(time[k], Y[k], color='g', linewidth=1.5)
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Z[k], color='r', linewidth=1.5, label='[Z]')
    else:
        plt.plot(time[k], Z[k], color='r', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()

# Output <plot2>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], X1[k], color='b', linewidth=1.5, label='[X]')
    else:
        plt.plot(time[k], X1[k], color='b', linewidth=1.5)
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Y1[k], color='g', linewidth=1.5, label='[Y]')
    else:
        plt.plot(time[k], Y1[k], color='g', linewidth=1.5)
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Z1[k], color='r', linewidth=1.5, label='[Z]')
    else:
        plt.plot(time[k], Z1[k], color='r', linewidth=1.5)
plt.title('plot2')
plt.legend()
plt.show()


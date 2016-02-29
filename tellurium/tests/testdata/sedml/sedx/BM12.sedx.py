"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:15)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_BM12
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_BM12'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - model1 

# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'model1.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[Z]', '[X]', '[Y]', 'time']
task1[0] = model1.simulate(start=0.0, end=100.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (time)
#  - X (X)
#  - Y (Y)
#  - Z (Z)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <X>
X = [sim['[X]'] for sim in task1]

# DataGenerator <Y>
Y = [sim['[Y]'] for sim in task1]

# DataGenerator <Z>
Z = [sim['[Z]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (BM 12)

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


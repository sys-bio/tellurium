"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:19)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_lorenz
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_lorenz'

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
model1.simulate(start=0.0, end=100.0, points=2)
task1[0] = model1.simulate(start=100.0, end=200.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time1 (time)
#  - X1 (X)
#  - Y1 (Y)
#  - Z1 (Z)

# DataGenerator <time1>
time1 = [sim['time'] for sim in task1]

# DataGenerator <X1>
X1 = [sim['[X]'] for sim in task1]

# DataGenerator <Y1>
Y1 = [sim['[Y]'] for sim in task1]

# DataGenerator <Z1>
Z1 = [sim['[Z]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (The Lorenz Attractor (time series))
#  - plot2 (The Lorenz Attractor (phase plot x vs y))
#  - plot3 (The Lorenz Attractor (phase plot x vs z))
#  - plot4 (The Lorenz Attractor (phase plot y vs z))

# Output <plot1>
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], X1[k], color='b', linewidth=1.5, label='[X]')
    else:
        plt.plot(time1[k], X1[k], color='b', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], Y1[k], color='g', linewidth=1.5, label='[Y]')
    else:
        plt.plot(time1[k], Y1[k], color='g', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], Z1[k], color='r', linewidth=1.5, label='[Z]')
    else:
        plt.plot(time1[k], Z1[k], color='r', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()

# Output <plot2>
for k in range(len(X1)):
    if k == 0:
        plt.plot(X1[k], Y1[k], color='b', linewidth=1.5, label='[Y]')
    else:
        plt.plot(X1[k], Y1[k], color='b', linewidth=1.5)
plt.title('plot2')
plt.legend()
plt.show()

# Output <plot3>
for k in range(len(X1)):
    if k == 0:
        plt.plot(X1[k], Z1[k], color='b', linewidth=1.5, label='[Z]')
    else:
        plt.plot(X1[k], Z1[k], color='b', linewidth=1.5)
plt.title('plot3')
plt.legend()
plt.show()

# Output <plot4>
for k in range(len(Y1)):
    if k == 0:
        plt.plot(Y1[k], Z1[k], color='b', linewidth=1.5, label='[Z]')
    else:
        plt.plot(Y1[k], Z1[k], color='b', linewidth=1.5)
plt.title('plot4')
plt.legend()
plt.show()


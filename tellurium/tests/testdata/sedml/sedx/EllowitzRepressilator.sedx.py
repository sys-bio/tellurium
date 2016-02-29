"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:17)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_EllowitzRepressilator
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_EllowitzRepressilator'

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
model1.timeCourseSelections = ['[X]', '[Y]', '[PX]', 'time', '[PZ]', '[PY]', '[Z]']
task1[0] = model1.simulate(start=0.0, end=10.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time1 (time)
#  - PX1 (Lactose operon repressor)
#  - PY1 (Tetracycline repressor)
#  - PZ1 (Repressor protein CI)
#  - X1 (transcript LacI)
#  - Y1 (transcript TetR)
#  - Z1 (transcript CI)

# DataGenerator <time1>
time1 = [sim['time'] for sim in task1]

# DataGenerator <PX1>
PX1 = [sim['[PX]'] for sim in task1]

# DataGenerator <PY1>
PY1 = [sim['[PY]'] for sim in task1]

# DataGenerator <PZ1>
PZ1 = [sim['[PZ]'] for sim in task1]

# DataGenerator <X1>
X1 = [sim['[X]'] for sim in task1]

# DataGenerator <Y1>
Y1 = [sim['[Y]'] for sim in task1]

# DataGenerator <Z1>
Z1 = [sim['[Z]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (Elowitz2000_Repressilator)

# Output <plot1>
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], PX1[k], color='b', linewidth=1.5, label='[PX]')
    else:
        plt.plot(time1[k], PX1[k], color='b', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], PY1[k], color='g', linewidth=1.5, label='[PY]')
    else:
        plt.plot(time1[k], PY1[k], color='g', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], PZ1[k], color='r', linewidth=1.5, label='[PZ]')
    else:
        plt.plot(time1[k], PZ1[k], color='r', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], X1[k], color='c', linewidth=1.5, label='[X]')
    else:
        plt.plot(time1[k], X1[k], color='c', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], Y1[k], color='m', linewidth=1.5, label='[Y]')
    else:
        plt.plot(time1[k], Y1[k], color='m', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], Z1[k], color='y', linewidth=1.5, label='[Z]')
    else:
        plt.plot(time1[k], Z1[k], color='y', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


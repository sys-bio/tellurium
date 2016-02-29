"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T16:36:17)
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

# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, '../models/BorisEJB.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[MKKK]', '[MKKK_P]', '[MAPK]', '[MAPK_PP]', '[MKK_P]', '[MAPK_P]', 'time', '[MKK]']
task1[0] = model1.simulate(start=0.0, end=4000.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time1 (time)
#  - MAPK1 (MAPK)
#  - MAPK_P1 (MAPK_P)
#  - MAPK_PP1 (MAPK_PP)
#  - MKK1 (MKK)
#  - MKK_P1 (MKK_P)
#  - MKKK1 (MKKK)
#  - MKKK_P1 (MKKK_P)

# DataGenerator <time1>
time1 = [sim['time'] for sim in task1]

# DataGenerator <MAPK1>
MAPK1 = [sim['[MAPK]'] for sim in task1]

# DataGenerator <MAPK_P1>
MAPK_P1 = [sim['[MAPK_P]'] for sim in task1]

# DataGenerator <MAPK_PP1>
MAPK_PP1 = [sim['[MAPK_PP]'] for sim in task1]

# DataGenerator <MKK1>
MKK1 = [sim['[MKK]'] for sim in task1]

# DataGenerator <MKK_P1>
MKK_P1 = [sim['[MKK_P]'] for sim in task1]

# DataGenerator <MKKK1>
MKKK1 = [sim['[MKKK]'] for sim in task1]

# DataGenerator <MKKK_P1>
MKKK_P1 = [sim['[MKKK_P]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (MAPK feedback (Kholodenko, 2000))

# Output <plot1>
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], MAPK1[k], color='b', linewidth=1.5, label='[MAPK]')
    else:
        plt.plot(time1[k], MAPK1[k], color='b', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], MAPK_P1[k], color='g', linewidth=1.5, label='[MAPK_P]')
    else:
        plt.plot(time1[k], MAPK_P1[k], color='g', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], MAPK_PP1[k], color='r', linewidth=1.5, label='[MAPK_PP]')
    else:
        plt.plot(time1[k], MAPK_PP1[k], color='r', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], MKK1[k], color='c', linewidth=1.5, label='[MKK]')
    else:
        plt.plot(time1[k], MKK1[k], color='c', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], MKKK1[k], color='m', linewidth=1.5, label='[MKKK]')
    else:
        plt.plot(time1[k], MKKK1[k], color='m', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], MKK_P1[k], color='y', linewidth=1.5, label='[MKK_P]')
    else:
        plt.plot(time1[k], MKK_P1[k], color='y', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], MKKK_P1[k], color='k', linewidth=1.5, label='[MKKK_P]')
    else:
        plt.plot(time1[k], MKKK_P1[k], color='k', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


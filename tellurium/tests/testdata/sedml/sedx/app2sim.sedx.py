"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T13:09:58)
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
model1 = te.loadSBMLModel(os.path.join(workingDir, 'urn:miriam:biomodels.db:BIOMD0000000003.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[C]', '[M]', '[X]', 'time']
task1[0] = model1.simulate(start=0.0, end=200.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (time)
#  - C1 (C1)
#  - M1 (M1)
#  - X1 (X1)
#  - Total (Total)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <C1>
C1 = [sim['[C]'] for sim in task1]

# DataGenerator <M1>
M1 = [sim['[M]'] for sim in task1]

# DataGenerator <X1>
X1 = [sim['[X]'] for sim in task1]

# DataGenerator <Total>
Total = [sim['[X]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (BioModel 3)

# Output <plot1>
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], C1[k], color='b', linewidth=1.5, label='[C]')
    else:
        plt.plot(time[k], C1[k], color='b', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], M1[k], color='g', linewidth=1.5, label='[M]')
    else:
        plt.plot(time[k], M1[k], color='g', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], X1[k], color='r', linewidth=1.5, label='[X]')
    else:
        plt.plot(time[k], X1[k], color='r', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], Total[k], color='c', linewidth=1.5, label='[X]')
    else:
        plt.plot(time[k], Total[k], color='c', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()

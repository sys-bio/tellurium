"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T15:26:14)
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
import tellurium.temiriam as temiriam
__model1_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000021')
model1 = te.loadSBMLModel(__model1_sbml)

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[P0]', '[T1]', '[T0]', '[CC]', '[P2]', '[T2]', '[P1]', '[Cn]', '[Mp]', 'time', '[Mt]']
task1[0] = model1.simulate(start=0.0, end=100.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (time)
#  - P0_1 (P0_1)
#  - T0_1 (T0_1)
#  - P1_1 (P1_1)
#  - T1_1 (T1_1)
#  - P2_1 (P2_1)
#  - T2_1 (T2_1)
#  - CC_1 (CC_1)
#  - Cn_1 (Cn_1)
#  - Mp_1 (Mp_1)
#  - Mt_1 (Mt_1)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <P0_1>
P0_1 = [sim['[P0]'] for sim in task1]

# DataGenerator <T0_1>
T0_1 = [sim['[T0]'] for sim in task1]

# DataGenerator <P1_1>
P1_1 = [sim['[P1]'] for sim in task1]

# DataGenerator <T1_1>
T1_1 = [sim['[T1]'] for sim in task1]

# DataGenerator <P2_1>
P2_1 = [sim['[P2]'] for sim in task1]

# DataGenerator <T2_1>
T2_1 = [sim['[T2]'] for sim in task1]

# DataGenerator <CC_1>
CC_1 = [sim['[CC]'] for sim in task1]

# DataGenerator <Cn_1>
Cn_1 = [sim['[Cn]'] for sim in task1]

# DataGenerator <Mp_1>
Mp_1 = [sim['[Mp]'] for sim in task1]

# DataGenerator <Mt_1>
Mt_1 = [sim['[Mt]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 

# Output <plot1>
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], P0_1[k], color='b', linewidth=1.5, label='[P0]')
    else:
        plt.plot(time[k], P0_1[k], color='b', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], T0_1[k], color='g', linewidth=1.5, label='[T0]')
    else:
        plt.plot(time[k], T0_1[k], color='g', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], P1_1[k], color='r', linewidth=1.5, label='[P1]')
    else:
        plt.plot(time[k], P1_1[k], color='r', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], T1_1[k], color='c', linewidth=1.5, label='[T1]')
    else:
        plt.plot(time[k], T1_1[k], color='c', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], P2_1[k], color='m', linewidth=1.5, label='[P2]')
    else:
        plt.plot(time[k], P2_1[k], color='m', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], T2_1[k], color='y', linewidth=1.5, label='[T2]')
    else:
        plt.plot(time[k], T2_1[k], color='y', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], CC_1[k], color='k', linewidth=1.5, label='[CC]')
    else:
        plt.plot(time[k], CC_1[k], color='k', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], Cn_1[k], color='b', linewidth=1.5, label='[Cn]')
    else:
        plt.plot(time[k], Cn_1[k], color='b', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], Mp_1[k], color='g', linewidth=1.5, label='[Mp]')
    else:
        plt.plot(time[k], Mp_1[k], color='g', linewidth=1.5)
for k in range(len(time)):
    if k==0:
        plt.plot(time[k], Mt_1[k], color='r', linewidth=1.5, label='[Mt]')
    else:
        plt.plot(time[k], Mt_1[k], color='r', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()

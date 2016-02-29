"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:18)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_JanaWolf
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_JanaWolf'

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
model1.timeCourseSelections = ['[fructose_1_6_bisphosphate]', '[NAD]', '[glycerate_3_phosphate]', 'time', '[ATP]', '[NADH]', '[Acetyladehyde]', '[Glucose]', '[pyruvate]', '[ADP]', '[glyceraldehyde_3_phosphate]', '[External_acetaldehyde]']
task1[0] = model1.simulate(start=0.0, end=10.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time1 (time)
#  - Glucose1 (Glucose)
#  - fructose_1_6_bisphosphate1 (fructose_1_6_bisphosphate)
#  - glyceraldehyde_3_phosphate1 (glyceraldehyde_3_phosphate)
#  - glycerate_3_phosphate1 (glycerate_3_phosphate)
#  - pyruvate1 (pyruvate)
#  - Acetyladehyde1 (Acetyladehyde)
#  - External_acetaldehyde1 (External_acetaldehyde)
#  - ATP1 (ATP)
#  - ADP1 (ADP)
#  - NAD1 (NAD)
#  - NADH1 (NADH)

# DataGenerator <time1>
time1 = [sim['time'] for sim in task1]

# DataGenerator <Glucose1>
Glucose1 = [sim['[Glucose]'] for sim in task1]

# DataGenerator <fructose_1_6_bisphosphate1>
fructose_1_6_bisphosphate1 = [sim['[fructose_1_6_bisphosphate]'] for sim in task1]

# DataGenerator <glyceraldehyde_3_phosphate1>
glyceraldehyde_3_phosphate1 = [sim['[glyceraldehyde_3_phosphate]'] for sim in task1]

# DataGenerator <glycerate_3_phosphate1>
glycerate_3_phosphate1 = [sim['[glycerate_3_phosphate]'] for sim in task1]

# DataGenerator <pyruvate1>
pyruvate1 = [sim['[pyruvate]'] for sim in task1]

# DataGenerator <Acetyladehyde1>
Acetyladehyde1 = [sim['[Acetyladehyde]'] for sim in task1]

# DataGenerator <External_acetaldehyde1>
External_acetaldehyde1 = [sim['[External_acetaldehyde]'] for sim in task1]

# DataGenerator <ATP1>
ATP1 = [sim['[ATP]'] for sim in task1]

# DataGenerator <ADP1>
ADP1 = [sim['[ADP]'] for sim in task1]

# DataGenerator <NAD1>
NAD1 = [sim['[NAD]'] for sim in task1]

# DataGenerator <NADH1>
NADH1 = [sim['[NADH]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (JanaWolf Glycolysis)

# Output <plot1>
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], Glucose1[k], color='b', linewidth=1.5, label='[Glucose]')
    else:
        plt.plot(time1[k], Glucose1[k], color='b', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], fructose_1_6_bisphosphate1[k], color='g', linewidth=1.5, label='[fructose_1_6_bisphosphate]')
    else:
        plt.plot(time1[k], fructose_1_6_bisphosphate1[k], color='g', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], glyceraldehyde_3_phosphate1[k], color='r', linewidth=1.5, label='[glyceraldehyde_3_phosphate]')
    else:
        plt.plot(time1[k], glyceraldehyde_3_phosphate1[k], color='r', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], glycerate_3_phosphate1[k], color='c', linewidth=1.5, label='[glycerate_3_phosphate]')
    else:
        plt.plot(time1[k], glycerate_3_phosphate1[k], color='c', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], pyruvate1[k], color='m', linewidth=1.5, label='[pyruvate]')
    else:
        plt.plot(time1[k], pyruvate1[k], color='m', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], Acetyladehyde1[k], color='y', linewidth=1.5, label='[Acetyladehyde]')
    else:
        plt.plot(time1[k], Acetyladehyde1[k], color='y', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], External_acetaldehyde1[k], color='k', linewidth=1.5, label='[External_acetaldehyde]')
    else:
        plt.plot(time1[k], External_acetaldehyde1[k], color='k', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], ATP1[k], color='b', linewidth=1.5, label='[ATP]')
    else:
        plt.plot(time1[k], ATP1[k], color='b', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], ADP1[k], color='g', linewidth=1.5, label='[ADP]')
    else:
        plt.plot(time1[k], ADP1[k], color='g', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], NAD1[k], color='r', linewidth=1.5, label='[NAD]')
    else:
        plt.plot(time1[k], NAD1[k], color='r', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], NADH1[k], color='c', linewidth=1.5, label='[NADH]')
    else:
        plt.plot(time1[k], NADH1[k], color='c', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


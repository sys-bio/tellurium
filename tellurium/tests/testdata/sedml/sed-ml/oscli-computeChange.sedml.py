"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:07)
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
model1 = te.loadSBMLModel(os.path.join(workingDir, '../models/oscli.xml'))
# Model <model2>
model2 = te.loadSBMLModel(os.path.join(workingDir, '../models/oscli.xml'))
# Unsupported change: computeChange
# Unsupported change: computeChange
# Unsupported change: computeChange

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 
#  - task2 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[S1]', '[S2]', 'time']
task1[0] = model1.simulate(start=0.0, end=100.0, steps=1000)

# Task <task2>
task2 = [None]
model2.setIntegrator('cvode')
model2.timeCourseSelections = ['[S1]', '[S2]']
task2[0] = model2.simulate(start=0.0, end=100.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time1 (time1)
#  - S1_1 (S1_1)
#  - S2_1 (S2_1)
#  - S1_2 (S1_2)
#  - S2_2 (S2_2)

# DataGenerator <time1>
time1 = [sim['time'] for sim in task1]

# DataGenerator <S1_1>
S1_1 = [sim['[S1]'] for sim in task1]

# DataGenerator <S2_1>
S2_1 = [sim['[S2]'] for sim in task1]

# DataGenerator <S1_2>
S1_2 = [sim['[S1]'] for sim in task2]

# DataGenerator <S2_2>
S2_2 = [sim['[S2]'] for sim in task2]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - report1 (Time Course (changed + unchanged))
#  - plot1 (oscli  (unchanged))
#  - plot2 (oscli  (initial concentrations halved))

# Output <report1>
df = pandas.DataFrame(np.column_stack([time1[0], S1_1[0], S1_2[0], S2_1[0], S2_2[0]]), 
    columns=['time1', 'S1_1', 'S1_2', 'S2_1', 'S2_2'])
print(df.head(10))

# Output <plot1>
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], S1_1[k], color='b', linewidth=1.5, label='[S1]')
    else:
        plt.plot(time1[k], S1_1[k], color='b', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], S2_1[k], color='g', linewidth=1.5, label='[S2]')
    else:
        plt.plot(time1[k], S2_1[k], color='g', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()

# Output <plot2>
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], S1_2[k], color='b', linewidth=1.5, label='[S1]')
    else:
        plt.plot(time1[k], S1_2[k], color='b', linewidth=1.5)
for k in range(len(time1)):
    if k == 0:
        plt.plot(time1[k], S2_2[k], color='g', linewidth=1.5, label='[S2]')
    else:
        plt.plot(time1[k], S2_2[k], color='g', linewidth=1.5)
plt.title('plot2')
plt.legend()
plt.show()


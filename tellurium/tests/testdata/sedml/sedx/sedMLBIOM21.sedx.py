"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:22)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_sedMLBIOM21
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_sedMLBIOM21'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - model1 (Circadian Oscillations)
#  - model2 (Circadian Chaos)

# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'model1.xml'))
# Model <model2>
model2 = te.loadSBMLModel(os.path.join(workingDir, 'model1.xml'))
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='V_dT']/@value 4.8
model2['V_dT'] = 4.8
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='V_mT']/@value 0.28
model2['V_mT'] = 0.28

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 (Baseline)
#  - task2 (Modified parameters)

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[Mt]', 'time']
model1.simulate(start=0.0, end=50.0, points=2)
task1[0] = model1.simulate(start=50.0, end=1000.0, steps=1000)

# Task <task2>
task2 = [None]
model2.setIntegrator('cvode')
model2.timeCourseSelections = ['[Mt]']
model2.simulate(start=0.0, end=50.0, points=2)
task2[0] = model2.simulate(start=50.0, end=1000.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (Time)
#  - tim1 (tim mRNA (total))
#  - tim2 (tim mRNA (changed parameters))
#  - tim3 (tim mRNA (difference v1-v2+20))

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <tim1>
tim1 = [sim['[Mt]'] for sim in task1]

# DataGenerator <tim2>
tim2 = [sim['[Mt]'] for sim in task2]

# DataGenerator <tim3>
tim3 = [sim['[Mt]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (tim mRNA with Oscillation and Chaos)

# Output <plot1>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], tim1[k], color='b', linewidth=1.5, label='[Mt]')
    else:
        plt.plot(time[k], tim1[k], color='b', linewidth=1.5)
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], tim2[k], color='g', linewidth=1.5, label='[Mt]')
    else:
        plt.plot(time[k], tim2[k], color='g', linewidth=1.5)
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], tim3[k], color='r', linewidth=1.5, label='[Mt]')
    else:
        plt.plot(time[k], tim3[k], color='r', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


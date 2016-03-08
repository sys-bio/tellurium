"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_ClockSedML
    inputType: COMBINE_FILE
"""
from __future__ import print_function, division
import tellurium as te
from tellurium.sedml.mathml import *
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import pandas
import os.path

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_ClockSedML'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'Clock_BIOMD21.xml'))
# Model <model2>
model2 = te.loadSBMLModel(os.path.join(workingDir, 'Clock_BIOMD21.xml'))
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='V_dT']/@value 4.8
model2['V_dT'] = 4.8
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='V_mT']/@value 0.28
model2['V_mT'] = 0.28

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# Task: <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[Mt]', 'time']
model1.simulate(start=0.0, end=50.0, points=2)
task1[0] = model1.simulate(start=50.0, end=1000.0, steps=1000)

# Task <task2>
# Task: <task2>
task2 = [None]
model2.setIntegrator('cvode')
model2.timeCourseSelections = ['[Mt]']
model2.simulate(start=0.0, end=50.0, points=2)
task2[0] = model2.simulate(start=50.0, end=1000.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <timeDG>
__var__time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__time.shape) == 1:
     __var__time.shape += (1,)
timeDG = __var__time

# DataGenerator <tim1>
__var__v1 = np.transpose(np.array([sim['[Mt]'] for sim in task1]))
if len(__var__v1.shape) == 1:
     __var__v1.shape += (1,)
tim1 = __var__v1

# DataGenerator <tim2>
__var__v2 = np.transpose(np.array([sim['[Mt]'] for sim in task2]))
if len(__var__v2.shape) == 1:
     __var__v2.shape += (1,)
tim2 = __var__v2

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot1>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(timeDG.shape[1]):
    if k == 0:
        plt.plot(timeDG[:,k], tim1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='tim mRNA (total)')
    else:
        plt.plot(timeDG[:,k], tim1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(timeDG.shape[1]):
    if k == 0:
        plt.plot(timeDG[:,k], tim2[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='tim mRNA (changed parameters)')
    else:
        plt.plot(timeDG[:,k], tim2[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('tim mRNA with Oscillation and Chaos', fontweight='bold')
plt.xlabel('Time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot1.png'), dpi=100)
plt.show()


"""
    tellurium 1.3.5

    auto-generated code
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml
    inputType: SEDML_FILE
"""
from __future__ import print_function, division
import tellurium as te
from roadrunner import Config
from tellurium.sedml.mathml import *
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import pandas
import os.path
Config.LOADSBMLOPTIONS_RECOMPILE = True

workingDir = r'/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
import tellurium.temiriam as temiriam
__model1_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000021')
model1 = te.loadSBMLModel(__model1_sbml)
# Model <model2>
import tellurium.temiriam as temiriam
__model2_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000021')
model2 = te.loadSBMLModel(__model2_sbml)
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id="V_dT"]/@value 4.8
model2['V_dT'] = 4.8
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id="V_mT"]/@value 0.28
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
# DataGenerator <time>
__var__var_time_0 = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__var_time_0.shape) == 1:
     __var__var_time_0.shape += (1,)
time = __var__var_time_0

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
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], tim1[:,k], marker = '.', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='tim1')
    else:
        plt.plot(time[:,k], tim1[:,k], marker = '.', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], tim2[:,k], marker = '.', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='tim2')
    else:
        plt.plot(time[:,k], tim2[:,k], marker = '.', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('tim mRNA with Oscillation and Chaos', fontweight='bold')
plt.xlabel('time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot1.png'), dpi=100)
plt.show()


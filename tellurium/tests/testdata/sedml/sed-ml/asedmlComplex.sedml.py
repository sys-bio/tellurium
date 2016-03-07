"""
    tellurium 1.3.1

    auto-generated code (2016-03-07T10:12:42)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml
    inputType: SEDML_FILE
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <Application0>
Application0 = te.loadSBMLModel(os.path.join(workingDir, '../models/asedmlComplex.xml'))
# Model <Application0_0>
Application0_0 = te.loadSBMLModel(os.path.join(workingDir, '../models/asedmlComplex.xml'))
# /sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='s0'] 25.0
Application0_0['init([s0])'] = 25.0

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task_0_0>
# not part of any DataGenerator: task_0_0

# Task <repeatedTask_0_0>

repeatedTask_0_0 = []
__range__range_0_0_s1_init_uM = np.linspace(start=5.0, stop=15.0, num=4)
for __k__range_0_0_s1_init_uM, __value__range_0_0_s1_init_uM in enumerate(__range__range_0_0_s1_init_uM):
    Application0_0.reset()
    # Task: <task_0_0>
    task_0_0 = [None]
    Application0_0.setIntegrator('cvode')
    Application0_0['init([s1])'] = __value__range_0_0_s1_init_uM
    Application0_0.timeCourseSelections = ['[s0]', '[s1]', 'time']
    task_0_0[0] = Application0_0.simulate(start=0.0, end=30.0, steps=1000)

    repeatedTask_0_0.extend(task_0_0)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time_repeatedTask_0_0>
__var__t = np.transpose(np.array([sim['time'] for sim in repeatedTask_0_0]))
if len(__var__t.shape) == 1:
     __var__t.shape += (1,)
time_repeatedTask_0_0 = __var__t

# DataGenerator <dataGen_repeatedTask_0_0_s0>
__var__s0 = np.transpose(np.array([sim['[s0]'] for sim in repeatedTask_0_0]))
if len(__var__s0.shape) == 1:
     __var__s0.shape += (1,)
dataGen_repeatedTask_0_0_s0 = __var__s0

# DataGenerator <dataGen_repeatedTask_0_0_s1>
__var__s1 = np.transpose(np.array([sim['[s1]'] for sim in repeatedTask_0_0]))
if len(__var__s1.shape) == 1:
     __var__s1.shape += (1,)
dataGen_repeatedTask_0_0_s1 = __var__s1

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot2d_Simulation1>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_s0[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_0')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_s0[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_s1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_1')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_s1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Application0plots', fontweight='bold')
plt.xlabel('time_repeatedTask_0_0', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot2d_Simulation1.png'), dpi=100)
plt.show()


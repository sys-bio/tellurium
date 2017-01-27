"""
    tellurium 1.3.5

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/results/_te_parameterScan1D
    inputType: COMBINE_FILE
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

workingDir = r'/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/results/_te_parameterScan1D'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'parameterScan1D.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
# not part of any DataGenerator: task0

# Task <task1>

task1 = []
__range__vector_for_J0_v0 = [8.0, 4.0, 0.40000000000000002]
for __k__vector_for_J0_v0, __value__vector_for_J0_v0 in enumerate(__range__vector_for_J0_v0):
    model1.reset()
    # Task: <task0>
    task0 = [None]
    model1.setIntegrator('cvode')
    model1['J0_v0'] = __value__vector_for_J0_v0
    model1.timeCourseSelections = ['[S1]', '[S2]', 'time']
    task0[0] = model1.simulate(start=0.0, end=20.0, steps=1000)

    task1.extend(task0)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task1_____time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__task1_____time.shape) == 1:
     __var__task1_____time.shape += (1,)
plot_0_0_0 = __var__task1_____time

# DataGenerator <plot_0_0_1>
__var__task1_____S1 = np.transpose(np.array([sim['[S1]'] for sim in task1]))
if len(__var__task1_____S1.shape) == 1:
     __var__task1_____S1.shape += (1,)
plot_0_0_1 = __var__task1_____S1

# DataGenerator <plot_0_1_1>
__var__task1_____S2 = np.transpose(np.array([sim['[S2]'] for sim in task1]))
if len(__var__task1_____S2.shape) == 1:
     __var__task1_____S2.shape += (1,)
plot_0_1_1 = __var__task1_____S2

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot_0>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], marker = '.', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='task1.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], marker = '.', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], marker = '.', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='task1.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], marker = '.', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('plot_0', fontweight='bold')
plt.xlabel('task1.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()


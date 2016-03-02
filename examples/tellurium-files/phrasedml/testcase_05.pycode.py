"""
    tellurium 1.3.1

    auto-generated code (2016-03-02T10:41:09)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmp1QG4dj_sedml/_te_testcase_05
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

workingDir = '/tmp/tmp1QG4dj_sedml/_te_testcase_05'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_05.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
task1 = [None]
mod1.setIntegrator('cvode')
mod1.timeCourseSelections = ['S2', 'S1', 'time']
task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task1_____time = np.array([sim['time'] for sim in task1])
plot_0_0_0 = __var__task1_____time

# DataGenerator <plot_0_0_1>
__var__task1_____S1 = np.array([sim['S1'] for sim in task1])
plot_0_0_1 = __var__task1_____S1

# DataGenerator <plot_0_1_1>
__var__task1_____S2 = np.array([sim['S2'] for sim in task1])
plot_0_1_1 = __var__task1_____S2

# DataGenerator <plot_0_2_1>
__var__task1_____S2 = np.array([sim['S1'] for sim in task1])
__var__task1_____S2 = np.array([sim['S2'] for sim in task1])
plot_0_2_1 = __var__task1_____S1 / __var__task1_____S2

# DataGenerator <plot_1_0_0>
__var__task1_____S1 = np.array([sim['S1'] for sim in task1])
plot_1_0_0 = __var__task1_____S1 / np.max(__var__task1_____S1)

# DataGenerator <plot_1_0_1>
__var__task1_____S2 = np.array([sim['S2'] for sim in task1])
plot_1_0_1 = __var__task1_____S2 / np.max(__var__task1_____S2)

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot_0>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.S1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.S2')
    else:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.S1/task1.S2')
    else:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
plt.title('Example plot', fontweight='bold')
plt.xlabel('task1.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()

# Output <plot_1>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(len(plot_1_0_0)):
    if k == 0:
        plt.plot(plot_1_0_0[k], plot_1_0_1[k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.S2/max(task1.S2)')
    else:
        plt.plot(plot_1_0_0[k], plot_1_0_1[k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
plt.title('Normalized plot', fontweight='bold')
plt.xlabel('task1.S1/max(task1.S1)', fontweight='bold')
plt.ylabel('task1.S2/max(task1.S2)', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()


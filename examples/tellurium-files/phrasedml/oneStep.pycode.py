"""
    tellurium 1.3.1

    auto-generated code (2016-03-03T20:23:44)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmp63FENj_sedml/_te_oneStep
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

workingDir = '/tmp/tmp63FENj_sedml/_te_oneStep'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'oneStep.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
task0 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = []
task0[0] = model1.simulate(start=0.0, end=0.1, points=2)

# Task <task1>
__range__x = list(np.linspace(start=0.0, stop=10.0, num=101))
task1 = []
for k in range(len(__range__x)):
    __value__x = __range__x[k]
    if k == 0:
        model1.reset()
    model1['J0_v0'] = piecewise(8, __value__x < 4, 0.1, (4 <= __value__x) and (__value__x < 6), 8)
    model1.setIntegrator('cvode')
    model1.timeCourseSelections = ['S2', 'S1', 'J0_v0', 'time']
    __subtask__ = model1.simulate(start=0.0, end=0.1, points=2)
    task1.extend([__subtask__])

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__offsets__task1 = np.cumsum(np.array([sim['time'][-1] for sim in task1]))
__offsets__task1 = np.insert(__offsets__task1, 0, 0)
__var__task1_____time = np.transpose(np.array([sim['time']+__offsets__task1[k] for k, sim in enumerate(task1)]))
__var__task1_____time = np.concatenate(np.transpose(__var__task1_____time))
if len(__var__task1_____time.shape) == 1:
     __var__task1_____time.shape += (1,)
plot_0_0_0 = __var__task1_____time

# DataGenerator <plot_0_0_1>
__var__task1_____S1 = np.transpose(np.array([sim['S1'] for sim in task1]))
__var__task1_____S1 = np.concatenate(np.transpose(__var__task1_____S1))
if len(__var__task1_____S1.shape) == 1:
     __var__task1_____S1.shape += (1,)
plot_0_0_1 = __var__task1_____S1

# DataGenerator <plot_0_1_1>
__var__task1_____S2 = np.transpose(np.array([sim['S2'] for sim in task1]))
__var__task1_____S2 = np.concatenate(np.transpose(__var__task1_____S2))
if len(__var__task1_____S2.shape) == 1:
     __var__task1_____S2.shape += (1,)
plot_0_1_1 = __var__task1_____S2

# DataGenerator <plot_0_2_1>
__var__task1_____J0_v0 = np.transpose(np.array([sim['J0_v0'] for sim in task1]))
__var__task1_____J0_v0 = np.concatenate(np.transpose(__var__task1_____J0_v0))
if len(__var__task1_____J0_v0.shape) == 1:
     __var__task1_____J0_v0.shape += (1,)
plot_0_2_1 = __var__task1_____J0_v0

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.J0_v0')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8)
plt.title('plot_0', fontweight='bold')
plt.xlabel('task1.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()


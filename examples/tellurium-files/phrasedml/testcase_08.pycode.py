"""
    tellurium 1.3.1

    auto-generated code (2016-03-03T11:41:02)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmp8rKHRy_sedml/_te_testcase_08
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

workingDir = '/tmp/tmp8rKHRy_sedml/_te_testcase_08'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_08.xml'))
# Model <mod2>
mod2 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_08.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
task1 = [None]
mod1.setIntegrator('cvode')
mod1.timeCourseSelections = []
task1[0] = mod1.simulate(start=0.0, end=10.0, steps=20)

# Task <task2>
task2 = [None]
mod2.setIntegrator('cvode')
mod2.timeCourseSelections = []
task2[0] = mod2.simulate(start=0.0, end=3.0, steps=10)

# Task <repeat1>
__range__uniform_linear_for_S1 = list(np.linspace(start=0.0, stop=10.0, num=10))
repeat1 = [None]*len(__range__uniform_linear_for_S1)
for k in range(len(__range__uniform_linear_for_S1)):
    if k == 0:
        mod1.reset()
    __value__uniform_linear_for_S1 = __range__uniform_linear_for_S1[k]
    mod1['S1'] = __value__uniform_linear_for_S1
    __var__S2 = mod1['S2']
    mod1['S1'] = __var__S2 + 3
    mod1.setIntegrator('cvode')
    mod1.timeCourseSelections = ['S2', 'S1', 'time']
    repeat1[k] = mod1.simulate(start=0.0, end=10.0, steps=20)
repeat1 = [None]*len(__range__uniform_linear_for_S1)
for k in range(len(__range__uniform_linear_for_S1)):
    if k == 0:
        mod2.reset()
    __value__uniform_linear_for_S1 = __range__uniform_linear_for_S1[k]
    mod2['S1'] = __value__uniform_linear_for_S1
    __var__S2 = mod2['S2']
    mod2['S1'] = __var__S2 + 3
    mod2.setIntegrator('cvode')
    mod2.timeCourseSelections = ['S2', 'S1', 'time']
    repeat1[k] = mod2.simulate(start=0.0, end=3.0, steps=10)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__repeat1_____mod1_____time = np.transpose(np.array([sim['time']+(k*sim['time'][-1]) for k,sim in enumerate(repeat1)]))
__var__repeat1_____mod1_____time = np.concatenate(np.transpose(__var__repeat1_____mod1_____time))
if len(__var__repeat1_____mod1_____time.shape) == 1:
     __var__repeat1_____mod1_____time.shape += (1,)
plot_0_0_0 = __var__repeat1_____mod1_____time

# DataGenerator <plot_0_0_1>
__var__repeat1_____mod1_____S1 = np.transpose(np.array([sim['S1'] for sim in repeat1]))
__var__repeat1_____mod1_____S1 = np.concatenate(np.transpose(__var__repeat1_____mod1_____S1))
if len(__var__repeat1_____mod1_____S1.shape) == 1:
     __var__repeat1_____mod1_____S1.shape += (1,)
plot_0_0_1 = __var__repeat1_____mod1_____S1

# DataGenerator <plot_0_1_1>
__var__repeat1_____mod1_____S2 = np.transpose(np.array([sim['S2'] for sim in repeat1]))
__var__repeat1_____mod1_____S2 = np.concatenate(np.transpose(__var__repeat1_____mod1_____S2))
if len(__var__repeat1_____mod1_____S2.shape) == 1:
     __var__repeat1_____mod1_____S2.shape += (1,)
plot_0_1_1 = __var__repeat1_____mod1_____S2

# DataGenerator <plot_0_2_0>
__var__repeat1_____mod2_____time = np.transpose(np.array([sim['time']+(k*sim['time'][-1]) for k,sim in enumerate(repeat1)]))
__var__repeat1_____mod2_____time = np.concatenate(np.transpose(__var__repeat1_____mod2_____time))
if len(__var__repeat1_____mod2_____time.shape) == 1:
     __var__repeat1_____mod2_____time.shape += (1,)
plot_0_2_0 = __var__repeat1_____mod2_____time

# DataGenerator <plot_0_2_1>
__var__repeat1_____mod2_____S1 = np.transpose(np.array([sim['S1'] for sim in repeat1]))
__var__repeat1_____mod2_____S1 = np.concatenate(np.transpose(__var__repeat1_____mod2_____S1))
if len(__var__repeat1_____mod2_____S1.shape) == 1:
     __var__repeat1_____mod2_____S1.shape += (1,)
plot_0_2_1 = __var__repeat1_____mod2_____S1

# DataGenerator <plot_0_3_1>
__var__repeat1_____mod2_____S2 = np.transpose(np.array([sim['S2'] for sim in repeat1]))
__var__repeat1_____mod2_____S2 = np.concatenate(np.transpose(__var__repeat1_____mod2_____S2))
if len(__var__repeat1_____mod2_____S2.shape) == 1:
     __var__repeat1_____mod2_____S2.shape += (1,)
plot_0_3_1 = __var__repeat1_____mod2_____S2

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.mod1.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.mod1.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_2_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_2_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.mod2.S1')
    else:
        plt.plot(plot_0_2_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_2_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_2_0[:,k], plot_0_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.mod2.S2')
    else:
        plt.plot(plot_0_2_0[:,k], plot_0_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=4.0, alpha=0.8)
plt.title('Repeated subtasks', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()


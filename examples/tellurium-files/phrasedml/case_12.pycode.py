"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_12
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

workingDir = r'/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_12'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'case_12.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# not part of any DataGenerator: task1

# Task <task2>
# not part of any DataGenerator: task2

# Task <repeat1>

repeat1 = []
__range__uniform_linear_for_S1 = np.linspace(start=0.0, stop=10.0, num=5)
for __k__uniform_linear_for_S1, __value__uniform_linear_for_S1 in enumerate(__range__uniform_linear_for_S1):
    mod1.reset()
    # Task: <task1>
    task1 = [None]
    mod1.setIntegrator('cvode')
    mod1['init([S1])'] = __value__uniform_linear_for_S1
    __value__S1 = mod1['init([S1])']
    mod1['init([S2])'] = __value__S1 + 20
    mod1.timeCourseSelections = ['[S1]', '[S2]', 'time']
    mod1.simulate(start=0.0, end=2.0, points=2)
    task1[0] = mod1.simulate(start=2.0, end=10.0, steps=49)

    repeat1.extend(task1)

# Task <repeat2>

repeat2 = []
__range__uniform_linear_for_S1 = np.linspace(start=0.0, stop=10.0, num=5)
for __k__uniform_linear_for_S1, __value__uniform_linear_for_S1 in enumerate(__range__uniform_linear_for_S1):
    mod1.reset()
    # Task: <task2>
    task2 = [None]
    mod1.setIntegrator('cvode')
    mod1['init([S1])'] = __value__uniform_linear_for_S1
    __value__S1 = mod1['init([S1])']
    mod1['init([S2])'] = __value__S1 + 20
    mod1.timeCourseSelections = ['[S1]', '[S2]', 'time']
    task2[0] = mod1.simulate(start=0.0, end=15.0, steps=49)

    repeat2.extend(task2)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__repeat2_____time = np.transpose(np.array([sim['time'] for sim in repeat2]))
if len(__var__repeat2_____time.shape) == 1:
     __var__repeat2_____time.shape += (1,)
plot_0_0_0 = __var__repeat2_____time

# DataGenerator <plot_0_0_1>
__var__repeat2_____S1 = np.transpose(np.array([sim['[S1]'] for sim in repeat2]))
if len(__var__repeat2_____S1.shape) == 1:
     __var__repeat2_____S1.shape += (1,)
plot_0_0_1 = __var__repeat2_____S1

# DataGenerator <plot_0_1_1>
__var__repeat2_____S2 = np.transpose(np.array([sim['[S2]'] for sim in repeat2]))
if len(__var__repeat2_____S2.shape) == 1:
     __var__repeat2_____S2.shape += (1,)
plot_0_1_1 = __var__repeat2_____S2

# DataGenerator <plot_0_2_0>
__var__repeat1_____time = np.transpose(np.array([sim['time'] for sim in repeat1]))
if len(__var__repeat1_____time.shape) == 1:
     __var__repeat1_____time.shape += (1,)
plot_0_2_0 = __var__repeat1_____time

# DataGenerator <plot_0_2_1>
__var__repeat1_____S1 = np.transpose(np.array([sim['[S1]'] for sim in repeat1]))
if len(__var__repeat1_____S1.shape) == 1:
     __var__repeat1_____S1.shape += (1,)
plot_0_2_1 = __var__repeat1_____S1

# DataGenerator <plot_0_3_1>
__var__repeat1_____S2 = np.transpose(np.array([sim['[S2]'] for sim in repeat1]))
if len(__var__repeat1_____S2.shape) == 1:
     __var__repeat1_____S2.shape += (1,)
plot_0_3_1 = __var__repeat1_____S2

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_2_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_2_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.S1')
    else:
        plt.plot(plot_0_2_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_2_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_2_0[:,k], plot_0_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.S2')
    else:
        plt.plot(plot_0_2_0[:,k], plot_0_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Offset simulation', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()

# Output <report_1>
__dfs__report_1 = []
for k in range(plot_0_0_0.shape[1]):
    print('-'*80)
    print('report_1, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_1_1[:,k], plot_0_2_0[:,k], plot_0_2_1[:,k], plot_0_3_1[:,k]]), 
    columns=['repeat2.time', 'repeat2.S1', 'repeat2.S2', 'repeat1.time', 'repeat1.S1', 'repeat1.S2'])
    print(__df__k.head(5))
    __dfs__report_1.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_1_{}.csv'.format(k)), sep='	', index=False)


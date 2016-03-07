"""
    tellurium 1.3.1

    auto-generated code (2016-03-07T13:03:01)
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_06
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

workingDir = '/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_06'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'case_06.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# not part of any DataGenerator: task1

# Task <repeat1>

repeat1 = []
__range__uniform_linear_for_S2 = np.linspace(start=0.0, stop=10.0, num=3)
__range__vector_for_S1 = [1.0, 3.0, 5.0]
for __k__uniform_linear_for_S2, __value__uniform_linear_for_S2 in enumerate(__range__uniform_linear_for_S2):
    __value__vector_for_S1 = __range__vector_for_S1[__k__uniform_linear_for_S2]
    mod1.reset()
    # Task: <task1>
    task1 = [None]
    mod1.setIntegrator('cvode')
    mod1['S1'] = __value__vector_for_S1
    mod1['S2'] = __value__uniform_linear_for_S2
    mod1.timeCourseSelections = ['S2', 'S1', 'time']
    task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

    repeat1.extend(task1)

# Task <repeat2>

repeat2 = []
__range__uniform_linear_for_S2 = np.linspace(start=0.0, stop=10.0, num=3)
__range__vector_for_S1 = [1.0, 3.0, 5.0]
for __k__uniform_linear_for_S2, __value__uniform_linear_for_S2 in enumerate(__range__uniform_linear_for_S2):
    __value__vector_for_S1 = __range__vector_for_S1[__k__uniform_linear_for_S2]
    if __k__uniform_linear_for_S2 == 0:
        mod1.reset()
    # Task: <task1>
    task1 = [None]
    mod1.setIntegrator('cvode')
    mod1['S1'] = __value__vector_for_S1
    mod1['S2'] = __value__uniform_linear_for_S2
    mod1.timeCourseSelections = ['S2', 'S1', 'time']
    task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

    repeat2.extend(task1)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__repeat1_____time = np.transpose(np.array([sim['time'] for sim in repeat1]))
if len(__var__repeat1_____time.shape) == 1:
     __var__repeat1_____time.shape += (1,)
plot_0_0_0 = __var__repeat1_____time

# DataGenerator <plot_0_0_1>
__var__repeat1_____S1 = np.transpose(np.array([sim['S1'] for sim in repeat1]))
if len(__var__repeat1_____S1.shape) == 1:
     __var__repeat1_____S1.shape += (1,)
plot_0_0_1 = __var__repeat1_____S1

# DataGenerator <plot_0_1_1>
__var__repeat1_____S2 = np.transpose(np.array([sim['S2'] for sim in repeat1]))
if len(__var__repeat1_____S2.shape) == 1:
     __var__repeat1_____S2.shape += (1,)
plot_0_1_1 = __var__repeat1_____S2

# DataGenerator <plot_2_0_0>
__offsets__repeat2 = np.cumsum(np.array([sim['time'][-1] for sim in repeat2]))
__offsets__repeat2 = np.insert(__offsets__repeat2, 0, 0)
__var__repeat2_____time = np.transpose(np.array([sim['time']+__offsets__repeat2[k] for k, sim in enumerate(repeat2)]))
__var__repeat2_____time = np.concatenate(np.transpose(__var__repeat2_____time))
if len(__var__repeat2_____time.shape) == 1:
     __var__repeat2_____time.shape += (1,)
plot_2_0_0 = __var__repeat2_____time

# DataGenerator <plot_2_0_1>
__var__repeat2_____S1 = np.transpose(np.array([sim['S1'] for sim in repeat2]))
__var__repeat2_____S1 = np.concatenate(np.transpose(__var__repeat2_____S1))
if len(__var__repeat2_____S1.shape) == 1:
     __var__repeat2_____S1.shape += (1,)
plot_2_0_1 = __var__repeat2_____S1

# DataGenerator <plot_2_1_1>
__var__repeat2_____S2 = np.transpose(np.array([sim['S2'] for sim in repeat2]))
__var__repeat2_____S2 = np.concatenate(np.transpose(__var__repeat2_____S2))
if len(__var__repeat2_____S2.shape) == 1:
     __var__repeat2_____S2.shape += (1,)
plot_2_1_1 = __var__repeat2_____S2

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Example plot', fontweight='bold')
plt.xlabel('repeat1.time', fontweight='bold')
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
    __df__k = pandas.DataFrame(np.column_stack([plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_1_1[:,k]]), 
    columns=['repeat1.time', 'repeat1.S1', 'repeat1.S2'])
    print(__df__k.head(10))
    __dfs__report_1.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_1_{}.csv'.format(k)), sep='	', index=False)

# Output <plot_2>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(plot_2_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_2_0_0[:,k], plot_2_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.S1')
    else:
        plt.plot(plot_2_0_0[:,k], plot_2_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_2_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_2_0_0[:,k], plot_2_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.S2')
    else:
        plt.plot(plot_2_0_0[:,k], plot_2_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Example plot', fontweight='bold')
plt.xlabel('repeat2.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_2.png'), dpi=100)
plt.show()

# Output <report_3>
__dfs__report_3 = []
for k in range(plot_2_0_0.shape[1]):
    print('-'*80)
    print('report_3, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([plot_2_0_0[:,k], plot_2_0_1[:,k], plot_2_1_1[:,k]]), 
    columns=['repeat2.time', 'repeat2.S1', 'repeat2.S2'])
    print(__df__k.head(10))
    __dfs__report_3.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_3_{}.csv'.format(k)), sep='	', index=False)


"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_02
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

workingDir = '/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_02'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model0>
model0 = te.loadSBMLModel(os.path.join(workingDir, 'case_02.xml'))
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'case_02.xml'))
# /sbml:sbml/sbml:model/listOfSpecies/species[@id='S1']/@initialConcentration 5
model1['init([S1])'] = 5

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
# not part of any DataGenerator: task0

# Task <task1>

task1 = []
__range__uniform_linear_for_k1 = np.linspace(start=0.0, stop=5.0, num=6)
for __k__uniform_linear_for_k1, __value__uniform_linear_for_k1 in enumerate(__range__uniform_linear_for_k1):
    model1.reset()
    # Task: <task0>
    task0 = [None]
    model1.setIntegrator('cvode')
    model1['k1'] = __value__uniform_linear_for_k1
    model1.timeCourseSelections = ['S2', 'S1', 'k1', 'time']
    task0[0] = model1.simulate(start=0.0, end=6.0, steps=100)

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
__var__task1_____S1 = np.transpose(np.array([sim['S1'] for sim in task1]))
if len(__var__task1_____S1.shape) == 1:
     __var__task1_____S1.shape += (1,)
plot_0_0_1 = __var__task1_____S1

# DataGenerator <plot_0_1_1>
__var__task1_____S2 = np.transpose(np.array([sim['S2'] for sim in task1]))
if len(__var__task1_____S2.shape) == 1:
     __var__task1_____S2.shape += (1,)
plot_0_1_1 = __var__task1_____S2

# DataGenerator <plot_2_0_0>
__var__task1_____k1 = np.transpose(np.array([sim['k1'] for sim in task1]))
if len(__var__task1_____k1.shape) == 1:
     __var__task1_____k1.shape += (1,)
plot_2_0_0 = __var__task1_____k1

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='task1.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='task1.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Repeated task with reset', fontweight='bold')
plt.xlabel('task1.time', fontweight='bold')
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
    columns=['task1.time', 'task1.S1', 'task1.S2'])
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
        plt.plot(plot_2_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='task1.S1')
    else:
        plt.plot(plot_2_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Repeated task varying k1', fontweight='bold')
plt.xlabel('task1.k1', fontweight='bold')
plt.ylabel('task1.S1', fontweight='bold')
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
    __df__k = pandas.DataFrame(np.column_stack([plot_2_0_0[:,k], plot_0_0_1[:,k]]), 
    columns=['task1.k1', 'task1.S1'])
    print(__df__k.head(10))
    __dfs__report_3.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_3_{}.csv'.format(k)), sep='	', index=False)


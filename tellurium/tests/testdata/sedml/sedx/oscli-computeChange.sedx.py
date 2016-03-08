"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_oscli-computeChange
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_oscli-computeChange'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'model1.xml'))
# Model <model2>
model2 = te.loadSBMLModel(os.path.join(workingDir, 'model1.xml'))
__var__J3_k2 = model2['J3_k2']
model2['J3_k2'] = __var__J3_k2 / 2
__var__S2 = model2['[S2]']
model2['init([S2])'] = __var__S2 / 2
__var__S1 = model2['[S1]']
model2['init([S1])'] = __var__S1 / 2

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# Task: <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[S1]', '[S2]', 'time']
task1[0] = model1.simulate(start=0.0, end=100.0, steps=1000)

# Task <task2>
# Task: <task2>
task2 = [None]
model2.setIntegrator('cvode')
model2.timeCourseSelections = ['[S1]', '[S2]']
task2[0] = model2.simulate(start=0.0, end=100.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time1>
__var__time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__time.shape) == 1:
     __var__time.shape += (1,)
time1 = __var__time

# DataGenerator <S1_1>
__var__d1_S1 = np.transpose(np.array([sim['[S1]'] for sim in task1]))
if len(__var__d1_S1.shape) == 1:
     __var__d1_S1.shape += (1,)
S1_1 = __var__d1_S1

# DataGenerator <S2_1>
__var__d1_S2 = np.transpose(np.array([sim['[S2]'] for sim in task1]))
if len(__var__d1_S2.shape) == 1:
     __var__d1_S2.shape += (1,)
S2_1 = __var__d1_S2

# DataGenerator <S1_2>
__var__d2_S1 = np.transpose(np.array([sim['[S1]'] for sim in task2]))
if len(__var__d2_S1.shape) == 1:
     __var__d2_S1.shape += (1,)
S1_2 = __var__d2_S1

# DataGenerator <S2_2>
__var__d2_S2 = np.transpose(np.array([sim['[S2]'] for sim in task2]))
if len(__var__d2_S2.shape) == 1:
     __var__d2_S2.shape += (1,)
S2_2 = __var__d2_S2

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <report1>
__dfs__report1 = []
for k in range(time1.shape[1]):
    print('-'*80)
    print('report1, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([time1[:,k], S1_1[:,k], S1_2[:,k], S2_1[:,k], S2_2[:,k]]), 
    columns=['time1', 'S1_1', 'S1_2', 'S2_1', 'S2_2'])
    print(__df__k.head(10))
    __dfs__report1.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report1_{}.csv'.format(k)), sep='	', index=False)

# Output <plot1>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], S1_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='S1_1')
    else:
        plt.plot(time1[:,k], S1_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], S2_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='S2_1')
    else:
        plt.plot(time1[:,k], S2_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('oscli  (unchanged)', fontweight='bold')
plt.xlabel('time1', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot1.png'), dpi=100)
plt.show()

# Output <plot2>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], S1_2[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='S1_2')
    else:
        plt.plot(time1[:,k], S1_2[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], S2_2[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='S2_2')
    else:
        plt.plot(time1[:,k], S2_2[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('oscli  (initial concentrations halved)', fontweight='bold')
plt.xlabel('time1', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot2.png'), dpi=100)
plt.show()


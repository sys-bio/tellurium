"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_BorisEJBsteady
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_BorisEJBsteady'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'model1.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# Task: <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.conservedMoietyAnalysis = True
model1.steadyStateSelections = ['[MKKK]', '[MKKK_P]', '[MAPK]', '[MAPK_PP]', '[MKK_P]', '[MAPK_P]', 'time', '[MKK]']
model1.simulate()
task1[0] = model1.steadyState()
model1.conservedMoietyAnalysis = False

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time1>
__var__time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__time.shape) == 1:
     __var__time.shape += (1,)
time1 = __var__time

# DataGenerator <MAPK1>
__var__MAPK = np.transpose(np.array([sim['[MAPK]'] for sim in task1]))
if len(__var__MAPK.shape) == 1:
     __var__MAPK.shape += (1,)
MAPK1 = __var__MAPK

# DataGenerator <MAPK_P1>
__var__MAPK_P = np.transpose(np.array([sim['[MAPK_P]'] for sim in task1]))
if len(__var__MAPK_P.shape) == 1:
     __var__MAPK_P.shape += (1,)
MAPK_P1 = __var__MAPK_P

# DataGenerator <MAPK_PP1>
__var__MAPK_PP = np.transpose(np.array([sim['[MAPK_PP]'] for sim in task1]))
if len(__var__MAPK_PP.shape) == 1:
     __var__MAPK_PP.shape += (1,)
MAPK_PP1 = __var__MAPK_PP

# DataGenerator <MKK1>
__var__MKK = np.transpose(np.array([sim['[MKK]'] for sim in task1]))
if len(__var__MKK.shape) == 1:
     __var__MKK.shape += (1,)
MKK1 = __var__MKK

# DataGenerator <MKK_P1>
__var__MKK_P = np.transpose(np.array([sim['[MKK_P]'] for sim in task1]))
if len(__var__MKK_P.shape) == 1:
     __var__MKK_P.shape += (1,)
MKK_P1 = __var__MKK_P

# DataGenerator <MKKK1>
__var__MKKK = np.transpose(np.array([sim['[MKKK]'] for sim in task1]))
if len(__var__MKKK.shape) == 1:
     __var__MKKK.shape += (1,)
MKKK1 = __var__MKKK

# DataGenerator <MKKK_P1>
__var__MKKK_P = np.transpose(np.array([sim['[MKKK_P]'] for sim in task1]))
if len(__var__MKKK_P.shape) == 1:
     __var__MKKK_P.shape += (1,)
MKKK_P1 = __var__MKKK_P

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <report1>
__dfs__report1 = []
for k in range(MAPK1.shape[1]):
    print('-'*80)
    print('report1, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([MAPK1[:,k], MAPK_P1[:,k], MAPK_PP1[:,k], MKK1[:,k], MKKK1[:,k], MKK_P1[:,k], MKKK_P1[:,k]]), 
    columns=['MAPK1', 'MAPK_P1', 'MAPK_PP1', 'MKK1', 'MKKK1', 'MKK_P1', 'MKKK_P1'])
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
        plt.plot(time1[:,k], MAPK1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='MAPK')
    else:
        plt.plot(time1[:,k], MAPK1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], MAPK_P1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='MAPK_P')
    else:
        plt.plot(time1[:,k], MAPK_P1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], MAPK_PP1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='MAPK_PP')
    else:
        plt.plot(time1[:,k], MAPK_PP1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], MKK1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='MKK')
    else:
        plt.plot(time1[:,k], MKK1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], MKKK1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8, label='MKKK')
    else:
        plt.plot(time1[:,k], MKKK1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], MKK_P1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8, label='MKK_P')
    else:
        plt.plot(time1[:,k], MKK_P1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], MKKK_P1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8, label='MKKK_P')
    else:
        plt.plot(time1[:,k], MKKK_P1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('MAPK feedback (Kholodenko, 2000)', fontweight='bold')
plt.xlabel('time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot1.png'), dpi=100)
plt.show()


"""
    tellurium 1.3.5

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/results/_te_case_09
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

workingDir = r'/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/results/_te_case_09'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'case_09.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# not part of any DataGenerator: task1

# Task <repeat1>

repeat1 = []
__range__x = np.linspace(start=0.0, stop=10.0, num=11)
for __k__x, __value__x in enumerate(__range__x):
    mod1.reset()
    # Task: <task1>
    task1 = [None]
    mod1.setIntegrator('cvode')
    mod1.timeCourseSelections = ['[MAPK_P]', '[MAPK]', '[MKK]', '[MAPK_PP]', 'time']
    task1[0] = mod1.simulate(start=0.0, end=4000.0, steps=1000)

    repeat1.extend(task1)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__repeat1_____MAPK = np.transpose(np.array([sim['[MAPK]'] for sim in repeat1]))
if len(__var__repeat1_____MAPK.shape) == 1:
     __var__repeat1_____MAPK.shape += (1,)
plot_0_0_0 = __var__repeat1_____MAPK

# DataGenerator <plot_0_0_1>
__var__repeat1_____time = np.transpose(np.array([sim['time'] for sim in repeat1]))
if len(__var__repeat1_____time.shape) == 1:
     __var__repeat1_____time.shape += (1,)
plot_0_0_1 = __var__repeat1_____time

# DataGenerator <plot_0_0_2>
__var__repeat1_____MAPK_P = np.transpose(np.array([sim['[MAPK_P]'] for sim in repeat1]))
if len(__var__repeat1_____MAPK_P.shape) == 1:
     __var__repeat1_____MAPK_P.shape += (1,)
plot_0_0_2 = __var__repeat1_____MAPK_P

# DataGenerator <plot_0_1_2>
__var__repeat1_____MAPK_PP = np.transpose(np.array([sim['[MAPK_PP]'] for sim in repeat1]))
if len(__var__repeat1_____MAPK_PP.shape) == 1:
     __var__repeat1_____MAPK_PP.shape += (1,)
plot_0_1_2 = __var__repeat1_____MAPK_PP

# DataGenerator <plot_0_2_2>
__var__repeat1_____MKK = np.transpose(np.array([sim['[MKK]'] for sim in repeat1]))
if len(__var__repeat1_____MKK.shape) == 1:
     __var__repeat1_____MKK.shape += (1,)
plot_0_2_2 = __var__repeat1_____MKK

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot_0>
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
ax = plt.subplot(__gs[0], projection='3d')
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_0_2[:,k], marker = '.', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.MAPK_P')
    else:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_0_2[:,k], marker = '.', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_1_2[:,k], marker = '.', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.MAPK_PP')
    else:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_1_2[:,k], marker = '.', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_2_2[:,k], marker = '.', color='g', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.MKK')
    else:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_2_2[:,k], marker = '.', color='g', linewidth=1.5, markersize=4.0, alpha=0.8)
ax.set_title('MAPK oscillations', fontweight='bold')
ax.set_xlabel('repeat1.MAPK', fontweight='bold')
ax.set_ylabel('repeat1.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=10)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()

# Output <report_1>
__dfs__report_1 = []
for k in range(plot_0_0_0.shape[1]):
    print('-'*80)
    print('report_1, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_0_2[:,k], plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_1_2[:,k], plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_2_2[:,k]]), 
    columns=['repeat1.MAPK', 'repeat1.time', 'repeat1.MAPK_P', 'repeat1.MAPK', 'repeat1.time', 'repeat1.MAPK_PP', 'repeat1.MAPK', 'repeat1.time', 'repeat1.MKK'])
    print(__df__k.head(5))
    __dfs__report_1.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_1_{}.csv'.format(k)), sep='	', index=False)


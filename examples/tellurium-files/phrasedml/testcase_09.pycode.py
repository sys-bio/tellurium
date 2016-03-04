"""
    tellurium 1.3.1

    auto-generated code (2016-03-04T16:27:21)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmp7GRRr9_sedml/_te_testcase_09
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

workingDir = '/tmp/tmp7GRRr9_sedml/_te_testcase_09'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_09.xml'))

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
    # execute simpleTask: <task1>
    task1 = [None]
    mod1.setIntegrator('cvode')
    mod1.timeCourseSelections = ['MAPK', 'time', 'MKK', 'MAPK_P', 'MAPK_PP']
    task1[0] = mod1.simulate(start=0.0, end=4000.0, steps=1000)

    repeat1.extend(task1)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__repeat1_____MAPK = np.transpose(np.array([sim['MAPK'] for sim in repeat1]))
if len(__var__repeat1_____MAPK.shape) == 1:
     __var__repeat1_____MAPK.shape += (1,)
plot_0_0_0 = __var__repeat1_____MAPK

# DataGenerator <plot_0_0_1>
__var__repeat1_____time = np.transpose(np.array([sim['time'] for sim in repeat1]))
if len(__var__repeat1_____time.shape) == 1:
     __var__repeat1_____time.shape += (1,)
plot_0_0_1 = __var__repeat1_____time

# DataGenerator <plot_0_0_2>
__var__repeat1_____MAPK_P = np.transpose(np.array([sim['MAPK_P'] for sim in repeat1]))
if len(__var__repeat1_____MAPK_P.shape) == 1:
     __var__repeat1_____MAPK_P.shape += (1,)
plot_0_0_2 = __var__repeat1_____MAPK_P

# DataGenerator <plot_0_1_2>
__var__repeat1_____MAPK_PP = np.transpose(np.array([sim['MAPK_PP'] for sim in repeat1]))
if len(__var__repeat1_____MAPK_PP.shape) == 1:
     __var__repeat1_____MAPK_PP.shape += (1,)
plot_0_1_2 = __var__repeat1_____MAPK_PP

# DataGenerator <plot_0_2_2>
__var__repeat1_____MKK = np.transpose(np.array([sim['MKK'] for sim in repeat1]))
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
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_0_2[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.MAPK_P')
    else:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_0_2[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_1_2[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.MAPK_PP')
    else:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_1_2[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_2_2[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeat1.MKK')
    else:
        ax.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], plot_0_2_2[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8)
ax.set_title('MAPK oscillations', fontweight='bold')
ax.set_xlabel('repeat1.MAPK', fontweight='bold')
ax.set_ylabel('repeat1.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=10)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.show()


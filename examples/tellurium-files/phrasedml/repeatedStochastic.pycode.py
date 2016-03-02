"""
    tellurium 1.3.1

    auto-generated code (2016-03-02T11:35:55)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpmmqY8K_sedml/_te_repeatedStochastic
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

workingDir = '/tmp/tmpmmqY8K_sedml/_te_repeatedStochastic'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'repeatedStochastic.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
task0 = [None]
model1.setIntegrator('gillespie')
model1.timeCourseSelections = []
task0[0] = model1.simulate(start=0.0, end=4000.0, steps=1000)

# Task <task1>
__range__x = list(np.linspace(start=0.0, stop=10.0, num=11))
task1 = [None]*len(__range__x)
for k in range(len(__range__x)):
    model1.reset()
    __value__x = __range__x[k]
    model1.setIntegrator('gillespie')
    model1.timeCourseSelections = ['MKKK', 'MKK_P', 'MAPK', 'MKK', 'MKKK_P', 'time', 'MAPK_P', 'MAPK_PP']
    task1[k] = model1.simulate(start=0.0, end=4000.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task1_____time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__task1_____time.shape) == 1:
     __var__task1_____time.shape += (1,)
plot_0_0_0 = __var__task1_____time

# DataGenerator <plot_0_0_1>
__var__task1_____MAPK = np.transpose(np.array([sim['MAPK'] for sim in task1]))
if len(__var__task1_____MAPK.shape) == 1:
     __var__task1_____MAPK.shape += (1,)
plot_0_0_1 = __var__task1_____MAPK

# DataGenerator <plot_0_1_1>
__var__task1_____MAPK_P = np.transpose(np.array([sim['MAPK_P'] for sim in task1]))
if len(__var__task1_____MAPK_P.shape) == 1:
     __var__task1_____MAPK_P.shape += (1,)
plot_0_1_1 = __var__task1_____MAPK_P

# DataGenerator <plot_0_2_1>
__var__task1_____MAPK_PP = np.transpose(np.array([sim['MAPK_PP'] for sim in task1]))
if len(__var__task1_____MAPK_PP.shape) == 1:
     __var__task1_____MAPK_PP.shape += (1,)
plot_0_2_1 = __var__task1_____MAPK_PP

# DataGenerator <plot_0_3_1>
__var__task1_____MKK = np.transpose(np.array([sim['MKK'] for sim in task1]))
if len(__var__task1_____MKK.shape) == 1:
     __var__task1_____MKK.shape += (1,)
plot_0_3_1 = __var__task1_____MKK

# DataGenerator <plot_0_4_1>
__var__task1_____MKK_P = np.transpose(np.array([sim['MKK_P'] for sim in task1]))
if len(__var__task1_____MKK_P.shape) == 1:
     __var__task1_____MKK_P.shape += (1,)
plot_0_4_1 = __var__task1_____MKK_P

# DataGenerator <plot_0_5_1>
__var__task1_____MKKK = np.transpose(np.array([sim['MKKK'] for sim in task1]))
if len(__var__task1_____MKKK.shape) == 1:
     __var__task1_____MKKK.shape += (1,)
plot_0_5_1 = __var__task1_____MKKK

# DataGenerator <plot_0_6_1>
__var__task1_____MKKK_P = np.transpose(np.array([sim['MKKK_P'] for sim in task1]))
if len(__var__task1_____MKKK_P.shape) == 1:
     __var__task1_____MKKK_P.shape += (1,)
plot_0_6_1 = __var__task1_____MKKK_P

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.MAPK')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.MAPK_P')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.MAPK_PP')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_3_1[:,k], '-o', color='c', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.MKK')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_3_1[:,k], '-o', color='c', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_4_1[:,k], '-o', color='m', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.MKK_P')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_4_1[:,k], '-o', color='m', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_5_1[:,k], '-o', color='y', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.MKKK')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_5_1[:,k], '-o', color='y', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_6_1[:,k], '-o', color='k', linewidth=1.5, markersize=4.0, alpha=0.8, label='task1.MKKK_P')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_6_1[:,k], '-o', color='k', linewidth=1.5, markersize=4.0, alpha=0.8)
plt.title('plot_0', fontweight='bold')
plt.xlabel('task1.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()


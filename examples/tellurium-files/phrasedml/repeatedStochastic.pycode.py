"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_repeatedStochastic
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

workingDir = r'/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_repeatedStochastic'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'repeatedStochastic.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# not part of any DataGenerator: task1

# Task <task2>
# not part of any DataGenerator: task2

# Task <repeat1>

repeat1 = []
__range__x = np.linspace(start=0.0, stop=10.0, num=11)
for __k__x, __value__x in enumerate(__range__x):
    model1.reset()
    # Task: <task1>
    task1 = [None]
    model1.setIntegrator('gillespie')
    model1.integrator.setValue('seed', 1003)
    model1.timeCourseSelections = ['[MKKK]', '[MKKK_P]', '[MAPK]', '[MAPK_PP]', '[MKK_P]', '[MAPK_P]', 'time', '[MKK]']
    task1[0] = model1.simulate(start=0.0, end=4000.0, steps=1000)

    repeat1.extend(task1)

# Task <repeat2>

repeat2 = []
__range__x = np.linspace(start=0.0, stop=10.0, num=11)
for __k__x, __value__x in enumerate(__range__x):
    model1.reset()
    # Task: <task2>
    task2 = [None]
    model1.setIntegrator('gillespie')
    model1.timeCourseSelections = ['[MKKK]', '[MKKK_P]', '[MAPK]', '[MAPK_PP]', '[MKK_P]', '[MAPK_P]', 'time', '[MKK]']
    task2[0] = model1.simulate(start=0.0, end=4000.0, steps=1000)

    repeat2.extend(task2)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__repeat1_____time = np.transpose(np.array([sim['time'] for sim in repeat1]))
if len(__var__repeat1_____time.shape) == 1:
     __var__repeat1_____time.shape += (1,)
plot_0_0_0 = __var__repeat1_____time

# DataGenerator <plot_0_0_1>
__var__repeat1_____MAPK = np.transpose(np.array([sim['[MAPK]'] for sim in repeat1]))
if len(__var__repeat1_____MAPK.shape) == 1:
     __var__repeat1_____MAPK.shape += (1,)
plot_0_0_1 = __var__repeat1_____MAPK

# DataGenerator <plot_0_1_1>
__var__repeat1_____MAPK_P = np.transpose(np.array([sim['[MAPK_P]'] for sim in repeat1]))
if len(__var__repeat1_____MAPK_P.shape) == 1:
     __var__repeat1_____MAPK_P.shape += (1,)
plot_0_1_1 = __var__repeat1_____MAPK_P

# DataGenerator <plot_0_2_1>
__var__repeat1_____MAPK_PP = np.transpose(np.array([sim['[MAPK_PP]'] for sim in repeat1]))
if len(__var__repeat1_____MAPK_PP.shape) == 1:
     __var__repeat1_____MAPK_PP.shape += (1,)
plot_0_2_1 = __var__repeat1_____MAPK_PP

# DataGenerator <plot_0_3_1>
__var__repeat1_____MKK = np.transpose(np.array([sim['[MKK]'] for sim in repeat1]))
if len(__var__repeat1_____MKK.shape) == 1:
     __var__repeat1_____MKK.shape += (1,)
plot_0_3_1 = __var__repeat1_____MKK

# DataGenerator <plot_0_4_1>
__var__repeat1_____MKK_P = np.transpose(np.array([sim['[MKK_P]'] for sim in repeat1]))
if len(__var__repeat1_____MKK_P.shape) == 1:
     __var__repeat1_____MKK_P.shape += (1,)
plot_0_4_1 = __var__repeat1_____MKK_P

# DataGenerator <plot_0_5_1>
__var__repeat1_____MKKK = np.transpose(np.array([sim['[MKKK]'] for sim in repeat1]))
if len(__var__repeat1_____MKKK.shape) == 1:
     __var__repeat1_____MKKK.shape += (1,)
plot_0_5_1 = __var__repeat1_____MKKK

# DataGenerator <plot_0_6_1>
__var__repeat1_____MKKK_P = np.transpose(np.array([sim['[MKKK_P]'] for sim in repeat1]))
if len(__var__repeat1_____MKKK_P.shape) == 1:
     __var__repeat1_____MKKK_P.shape += (1,)
plot_0_6_1 = __var__repeat1_____MKKK_P

# DataGenerator <plot_1_0_0>
__var__repeat2_____time = np.transpose(np.array([sim['time'] for sim in repeat2]))
if len(__var__repeat2_____time.shape) == 1:
     __var__repeat2_____time.shape += (1,)
plot_1_0_0 = __var__repeat2_____time

# DataGenerator <plot_1_0_1>
__var__repeat2_____MAPK = np.transpose(np.array([sim['[MAPK]'] for sim in repeat2]))
if len(__var__repeat2_____MAPK.shape) == 1:
     __var__repeat2_____MAPK.shape += (1,)
plot_1_0_1 = __var__repeat2_____MAPK

# DataGenerator <plot_1_1_1>
__var__repeat2_____MAPK_P = np.transpose(np.array([sim['[MAPK_P]'] for sim in repeat2]))
if len(__var__repeat2_____MAPK_P.shape) == 1:
     __var__repeat2_____MAPK_P.shape += (1,)
plot_1_1_1 = __var__repeat2_____MAPK_P

# DataGenerator <plot_1_2_1>
__var__repeat2_____MAPK_PP = np.transpose(np.array([sim['[MAPK_PP]'] for sim in repeat2]))
if len(__var__repeat2_____MAPK_PP.shape) == 1:
     __var__repeat2_____MAPK_PP.shape += (1,)
plot_1_2_1 = __var__repeat2_____MAPK_PP

# DataGenerator <plot_1_3_1>
__var__repeat2_____MKK = np.transpose(np.array([sim['[MKK]'] for sim in repeat2]))
if len(__var__repeat2_____MKK.shape) == 1:
     __var__repeat2_____MKK.shape += (1,)
plot_1_3_1 = __var__repeat2_____MKK

# DataGenerator <plot_1_4_1>
__var__repeat2_____MKK_P = np.transpose(np.array([sim['[MKK_P]'] for sim in repeat2]))
if len(__var__repeat2_____MKK_P.shape) == 1:
     __var__repeat2_____MKK_P.shape += (1,)
plot_1_4_1 = __var__repeat2_____MKK_P

# DataGenerator <plot_1_5_1>
__var__repeat2_____MKKK = np.transpose(np.array([sim['[MKKK]'] for sim in repeat2]))
if len(__var__repeat2_____MKKK.shape) == 1:
     __var__repeat2_____MKKK.shape += (1,)
plot_1_5_1 = __var__repeat2_____MKKK

# DataGenerator <plot_1_6_1>
__var__repeat2_____MKKK_P = np.transpose(np.array([sim['[MKKK_P]'] for sim in repeat2]))
if len(__var__repeat2_____MKKK_P.shape) == 1:
     __var__repeat2_____MKKK_P.shape += (1,)
plot_1_6_1 = __var__repeat2_____MKKK_P

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.MAPK')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.MAPK_P')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.MAPK_PP')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.MKK')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_4_1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.MKK_P')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_4_1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_5_1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.MKKK')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_5_1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_6_1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat1.MKKK_P')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_6_1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Repeats with SEED', fontweight='bold')
plt.xlabel('repeat1.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()

# Output <plot_1>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_1_0_0[:,k], plot_1_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.MAPK')
    else:
        plt.plot(plot_1_0_0[:,k], plot_1_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_1_0_0[:,k], plot_1_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.MAPK_P')
    else:
        plt.plot(plot_1_0_0[:,k], plot_1_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_1_0_0[:,k], plot_1_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.MAPK_PP')
    else:
        plt.plot(plot_1_0_0[:,k], plot_1_2_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_1_0_0[:,k], plot_1_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.MKK')
    else:
        plt.plot(plot_1_0_0[:,k], plot_1_3_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_1_0_0[:,k], plot_1_4_1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.MKK_P')
    else:
        plt.plot(plot_1_0_0[:,k], plot_1_4_1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_1_0_0[:,k], plot_1_5_1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.MKKK')
    else:
        plt.plot(plot_1_0_0[:,k], plot_1_5_1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_1_0_0[:,k], plot_1_6_1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8, label='repeat2.MKKK_P')
    else:
        plt.plot(plot_1_0_0[:,k], plot_1_6_1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Repeats without SEED', fontweight='bold')
plt.xlabel('repeat2.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_1.png'), dpi=100)
plt.show()


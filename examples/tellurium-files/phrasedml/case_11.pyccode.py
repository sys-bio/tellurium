"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_11
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

workingDir = '/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_11'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'case_11.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# not part of any DataGenerator: task1

# Task <rtask1>
# not part of any DataGenerator: rtask1

# Task <rtask2>
# not part of any DataGenerator: rtask2

# Task <rtask3>

rtask3 = []
__range__vector_for_S1 = [5.0, 10.0]
for __k__vector_for_S1, __value__vector_for_S1 in enumerate(__range__vector_for_S1):
    mod1.reset()
    
    rtask2 = []
    __range__uniform_linear_for_k2 = np.linspace(start=0.0, stop=1.0, num=4)
    for __k__uniform_linear_for_k2, __value__uniform_linear_for_k2 in enumerate(__range__uniform_linear_for_k2):
        if __k__uniform_linear_for_k2 == 0:
            mod1.reset()
        
        rtask1 = []
        __range__uniform_linear_for_k1 = np.linspace(start=0.0, stop=1.0, num=3)
        for __k__uniform_linear_for_k1, __value__uniform_linear_for_k1 in enumerate(__range__uniform_linear_for_k1):
            if __k__uniform_linear_for_k1 == 0:
                mod1.reset()
            # Task: <task1>
            task1 = [None]
            mod1.setIntegrator('cvode')
            mod1['S1'] = __value__vector_for_S1
            mod1['k2'] = __value__uniform_linear_for_k2
            mod1['k1'] = __value__uniform_linear_for_k1
            mod1.timeCourseSelections = ['S2', 'S1', 'time', 'k1', 'k2']
            task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

            rtask1.extend(task1)

        rtask2.extend(rtask1)

    rtask3.extend(rtask2)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__rtask3_____time = np.transpose(np.array([sim['time'] for sim in rtask3]))
if len(__var__rtask3_____time.shape) == 1:
     __var__rtask3_____time.shape += (1,)
plot_0_0_0 = __var__rtask3_____time

# DataGenerator <plot_0_0_1>
__var__rtask3_____S1 = np.transpose(np.array([sim['S1'] for sim in rtask3]))
if len(__var__rtask3_____S1.shape) == 1:
     __var__rtask3_____S1.shape += (1,)
plot_0_0_1 = __var__rtask3_____S1

# DataGenerator <plot_0_1_1>
__var__rtask3_____S2 = np.transpose(np.array([sim['S2'] for sim in rtask3]))
if len(__var__rtask3_____S2.shape) == 1:
     __var__rtask3_____S2.shape += (1,)
plot_0_1_1 = __var__rtask3_____S2

# DataGenerator <plot_1_0_0>
__var__rtask3_____k1 = np.transpose(np.array([sim['k1'] for sim in rtask3]))
if len(__var__rtask3_____k1.shape) == 1:
     __var__rtask3_____k1.shape += (1,)
plot_1_0_0 = __var__rtask3_____k1

# DataGenerator <plot_1_0_1>
__var__rtask3_____k2 = np.transpose(np.array([sim['k2'] for sim in rtask3]))
if len(__var__rtask3_____k2.shape) == 1:
     __var__rtask3_____k2.shape += (1,)
plot_1_0_1 = __var__rtask3_____k2

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='rtask3.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='rtask3.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('RepeatedTask of RepeatedTask', fontweight='bold')
plt.xlabel('rtask3.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()

# Output <plot_1>
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
ax = plt.subplot(__gs[0], projection='3d')
for k in range(plot_1_0_0.shape[1]):
    if k == 0:
        ax.plot(plot_1_0_0[:,k], plot_1_0_1[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='rtask3.S1')
    else:
        ax.plot(plot_1_0_0[:,k], plot_1_0_1[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
ax.set_title('plot_1', fontweight='bold')
ax.set_xlabel('rtask3.k1', fontweight='bold')
ax.set_ylabel('rtask3.k2', fontweight='bold')
ax.set_zlabel('rtask3.S1', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=10)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.savefig(os.path.join(workingDir, 'plot_1.png'), dpi=100)
plt.show()


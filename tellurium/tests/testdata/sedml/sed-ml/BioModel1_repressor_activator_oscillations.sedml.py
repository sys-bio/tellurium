"""
    tellurium 1.3.1

    auto-generated code (2016-03-07T12:18:48)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml
    inputType: SEDML_FILE
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <repressor_activator_oscillations>
repressor_activator_oscillations = te.loadSBMLModel(os.path.join(workingDir, '../models/BioModel1_repressor_activator_oscillations.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task_0_0>
# not part of any DataGenerator: task_0_0

# Task <repeatedTask_0_0>

repeatedTask_0_0 = []
__range__range_0_0_common_delta_A = np.linspace(start=0.2, stop=1.0, num=4)
for __k__range_0_0_common_delta_A, __value__range_0_0_common_delta_A in enumerate(__range__range_0_0_common_delta_A):
    repressor_activator_oscillations.reset()
    # Task: <task_0_0>
    task_0_0 = [None]
    repressor_activator_oscillations.setIntegrator('cvode')
    repressor_activator_oscillations['common_delta_A'] = __value__range_0_0_common_delta_A
    repressor_activator_oscillations.timeCourseSelections = ['[mRNA_A_]', '[PrmR]', '[C]', '[PrmA]', '[PrmA_bound]', '[A]', '[mRNA_R]', '[R]', 'time', '[PrmR_bound]']
    task_0_0[0] = repressor_activator_oscillations.simulate(start=0.0, end=200.0, steps=400)

    repeatedTask_0_0.extend(task_0_0)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time_repeatedTask_0_0>
__var__t = np.transpose(np.array([sim['time'] for sim in repeatedTask_0_0]))
if len(__var__t.shape) == 1:
     __var__t.shape += (1,)
time_repeatedTask_0_0 = __var__t

# DataGenerator <dataGen_repeatedTask_0_0_mRNA_R>
__var__mRNA_R = np.transpose(np.array([sim['[mRNA_R]'] for sim in repeatedTask_0_0]))
if len(__var__mRNA_R.shape) == 1:
     __var__mRNA_R.shape += (1,)
dataGen_repeatedTask_0_0_mRNA_R = __var__mRNA_R

# DataGenerator <dataGen_repeatedTask_0_0_A>
__var__A = np.transpose(np.array([sim['[A]'] for sim in repeatedTask_0_0]))
if len(__var__A.shape) == 1:
     __var__A.shape += (1,)
dataGen_repeatedTask_0_0_A = __var__A

# DataGenerator <dataGen_repeatedTask_0_0_R>
__var__R = np.transpose(np.array([sim['[R]'] for sim in repeatedTask_0_0]))
if len(__var__R.shape) == 1:
     __var__R.shape += (1,)
dataGen_repeatedTask_0_0_R = __var__R

# DataGenerator <dataGen_repeatedTask_0_0_PrmA>
__var__PrmA = np.transpose(np.array([sim['[PrmA]'] for sim in repeatedTask_0_0]))
if len(__var__PrmA.shape) == 1:
     __var__PrmA.shape += (1,)
dataGen_repeatedTask_0_0_PrmA = __var__PrmA

# DataGenerator <dataGen_repeatedTask_0_0_PrmR>
__var__PrmR = np.transpose(np.array([sim['[PrmR]'] for sim in repeatedTask_0_0]))
if len(__var__PrmR.shape) == 1:
     __var__PrmR.shape += (1,)
dataGen_repeatedTask_0_0_PrmR = __var__PrmR

# DataGenerator <dataGen_repeatedTask_0_0_C>
__var__C = np.transpose(np.array([sim['[C]'] for sim in repeatedTask_0_0]))
if len(__var__C.shape) == 1:
     __var__C.shape += (1,)
dataGen_repeatedTask_0_0_C = __var__C

# DataGenerator <dataGen_repeatedTask_0_0_PrmA_bound>
__var__PrmA_bound = np.transpose(np.array([sim['[PrmA_bound]'] for sim in repeatedTask_0_0]))
if len(__var__PrmA_bound.shape) == 1:
     __var__PrmA_bound.shape += (1,)
dataGen_repeatedTask_0_0_PrmA_bound = __var__PrmA_bound

# DataGenerator <dataGen_repeatedTask_0_0_PrmR_bound>
__var__PrmR_bound = np.transpose(np.array([sim['[PrmR_bound]'] for sim in repeatedTask_0_0]))
if len(__var__PrmR_bound.shape) == 1:
     __var__PrmR_bound.shape += (1,)
dataGen_repeatedTask_0_0_PrmR_bound = __var__PrmR_bound

# DataGenerator <dataGen_repeatedTask_0_0_mRNA_A_>
__var__mRNA_A_ = np.transpose(np.array([sim['[mRNA_A_]'] for sim in repeatedTask_0_0]))
if len(__var__mRNA_A_.shape) == 1:
     __var__mRNA_A_.shape += (1,)
dataGen_repeatedTask_0_0_mRNA_A_ = __var__mRNA_A_

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot2d_scan_for_delta_A>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_mRNA_R[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_0')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_mRNA_R[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_A[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_1')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_A[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_R[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_2')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_R[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmA[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_3')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmA[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmR[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_4')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmR[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_C[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_5')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_C[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmA_bound[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_6')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmA_bound[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmR_bound[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_7')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_PrmR_bound[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time_repeatedTask_0_0.shape[1]):
    if k == 0:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_mRNA_A_[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='curve_8')
    else:
        plt.plot(time_repeatedTask_0_0[:,k], dataGen_repeatedTask_0_0_mRNA_A_[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('repressor_activator_oscillationsplots', fontweight='bold')
plt.xlabel('time_repeatedTask_0_0', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot2d_scan_for_delta_A.png'), dpi=100)
plt.show()


"""
    tellurium 1.3.1

    auto-generated code (2016-03-07T08:42:56)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_EllowitzRepressilator
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_EllowitzRepressilator'

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
model1.timeCourseSelections = ['[X]', '[Y]', '[PX]', 'time', '[PZ]', '[PY]', '[Z]']
task1[0] = model1.simulate(start=0.0, end=10.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time1>
__var__time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__time.shape) == 1:
     __var__time.shape += (1,)
time1 = __var__time

# DataGenerator <PX1>
__var__PX = np.transpose(np.array([sim['[PX]'] for sim in task1]))
if len(__var__PX.shape) == 1:
     __var__PX.shape += (1,)
PX1 = __var__PX

# DataGenerator <PY1>
__var__PY = np.transpose(np.array([sim['[PY]'] for sim in task1]))
if len(__var__PY.shape) == 1:
     __var__PY.shape += (1,)
PY1 = __var__PY

# DataGenerator <PZ1>
__var__PZ = np.transpose(np.array([sim['[PZ]'] for sim in task1]))
if len(__var__PZ.shape) == 1:
     __var__PZ.shape += (1,)
PZ1 = __var__PZ

# DataGenerator <X1>
__var__X = np.transpose(np.array([sim['[X]'] for sim in task1]))
if len(__var__X.shape) == 1:
     __var__X.shape += (1,)
X1 = __var__X

# DataGenerator <Y1>
__var__Y = np.transpose(np.array([sim['[Y]'] for sim in task1]))
if len(__var__Y.shape) == 1:
     __var__Y.shape += (1,)
Y1 = __var__Y

# DataGenerator <Z1>
__var__Z = np.transpose(np.array([sim['[Z]'] for sim in task1]))
if len(__var__Z.shape) == 1:
     __var__Z.shape += (1,)
Z1 = __var__Z

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot1>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], PX1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='Lactose operon repressor')
    else:
        plt.plot(time1[:,k], PX1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], PY1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='Tetracycline repressor')
    else:
        plt.plot(time1[:,k], PY1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], PZ1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='Repressor protein CI')
    else:
        plt.plot(time1[:,k], PZ1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], X1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='transcript LacI')
    else:
        plt.plot(time1[:,k], X1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], Y1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8, label='transcript TetR')
    else:
        plt.plot(time1[:,k], Y1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], Z1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8, label='transcript CI')
    else:
        plt.plot(time1[:,k], Z1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('Elowitz2000_Repressilator', fontweight='bold')
plt.xlabel('time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()


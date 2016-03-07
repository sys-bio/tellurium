"""
    tellurium 1.3.1

    auto-generated code (2016-03-07T10:12:48)
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
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, '../models/lorenz.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# Task: <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[Z]', '[X]', '[Y]', 'time']
task1[0] = model1.simulate(start=0.0, end=200.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time1>
__var__time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__time.shape) == 1:
     __var__time.shape += (1,)
time1 = __var__time

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
        plt.plot(time1[:,k], X1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='X1')
    else:
        plt.plot(time1[:,k], X1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], Y1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='Y1')
    else:
        plt.plot(time1[:,k], Y1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], Z1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='Z1')
    else:
        plt.plot(time1[:,k], Z1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('The Lorenz Attractor (time series)', fontweight='bold')
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
for k in range(X1.shape[1]):
    if k == 0:
        plt.plot(X1[:,k], Y1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='Y1')
    else:
        plt.plot(X1[:,k], Y1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('The Lorenz Attractor (phase plot x vs y)', fontweight='bold')
plt.xlabel('X1', fontweight='bold')
plt.ylabel('Y1', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot2.png'), dpi=100)
plt.show()

# Output <plot3>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(X1.shape[1]):
    if k == 0:
        plt.plot(X1[:,k], Z1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='Z1')
    else:
        plt.plot(X1[:,k], Z1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('The Lorenz Attractor (phase plot x vs z)', fontweight='bold')
plt.xlabel('X1', fontweight='bold')
plt.ylabel('Z1', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot3.png'), dpi=100)
plt.show()

# Output <plot4>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(Y1.shape[1]):
    if k == 0:
        plt.plot(Y1[:,k], Z1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='Z1')
    else:
        plt.plot(Y1[:,k], Z1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('The Lorenz Attractor (phase plot y vs z)', fontweight='bold')
plt.xlabel('Y1', fontweight='bold')
plt.ylabel('Z1', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot4.png'), dpi=100)
plt.show()


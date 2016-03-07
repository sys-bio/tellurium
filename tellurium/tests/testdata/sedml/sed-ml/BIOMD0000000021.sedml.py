"""
    tellurium 1.3.1

    auto-generated code (2016-03-07T10:12:31)
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
import tellurium.temiriam as temiriam
__model1_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000021')
model1 = te.loadSBMLModel(__model1_sbml)

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# Task: <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[P0]', '[T1]', '[T0]', '[CC]', '[P2]', '[T2]', '[P1]', '[Cn]', '[Mp]', 'time', '[Mt]']
task1[0] = model1.simulate(start=0.0, end=100.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time>
__var__var_time_0 = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__var_time_0.shape) == 1:
     __var__var_time_0.shape += (1,)
time = __var__var_time_0

# DataGenerator <P0_1>
__var__P0 = np.transpose(np.array([sim['[P0]'] for sim in task1]))
if len(__var__P0.shape) == 1:
     __var__P0.shape += (1,)
P0_1 = __var__P0

# DataGenerator <T0_1>
__var__T0 = np.transpose(np.array([sim['[T0]'] for sim in task1]))
if len(__var__T0.shape) == 1:
     __var__T0.shape += (1,)
T0_1 = __var__T0

# DataGenerator <P1_1>
__var__P1 = np.transpose(np.array([sim['[P1]'] for sim in task1]))
if len(__var__P1.shape) == 1:
     __var__P1.shape += (1,)
P1_1 = __var__P1

# DataGenerator <T1_1>
__var__T1 = np.transpose(np.array([sim['[T1]'] for sim in task1]))
if len(__var__T1.shape) == 1:
     __var__T1.shape += (1,)
T1_1 = __var__T1

# DataGenerator <P2_1>
__var__P2 = np.transpose(np.array([sim['[P2]'] for sim in task1]))
if len(__var__P2.shape) == 1:
     __var__P2.shape += (1,)
P2_1 = __var__P2

# DataGenerator <T2_1>
__var__T2 = np.transpose(np.array([sim['[T2]'] for sim in task1]))
if len(__var__T2.shape) == 1:
     __var__T2.shape += (1,)
T2_1 = __var__T2

# DataGenerator <CC_1>
__var__CC = np.transpose(np.array([sim['[CC]'] for sim in task1]))
if len(__var__CC.shape) == 1:
     __var__CC.shape += (1,)
CC_1 = __var__CC

# DataGenerator <Cn_1>
__var__Cn = np.transpose(np.array([sim['[Cn]'] for sim in task1]))
if len(__var__Cn.shape) == 1:
     __var__Cn.shape += (1,)
Cn_1 = __var__Cn

# DataGenerator <Mp_1>
__var__Mp = np.transpose(np.array([sim['[Mp]'] for sim in task1]))
if len(__var__Mp.shape) == 1:
     __var__Mp.shape += (1,)
Mp_1 = __var__Mp

# DataGenerator <Mt_1>
__var__Mt = np.transpose(np.array([sim['[Mt]'] for sim in task1]))
if len(__var__Mt.shape) == 1:
     __var__Mt.shape += (1,)
Mt_1 = __var__Mt

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot1>
plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
plt.subplot(__gs[0])
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], P0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='P0_1')
    else:
        plt.plot(time[:,k], P0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], T0_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='T0_1')
    else:
        plt.plot(time[:,k], T0_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], P1_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='P1_1')
    else:
        plt.plot(time[:,k], P1_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], T1_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='T1_1')
    else:
        plt.plot(time[:,k], T1_1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], P2_1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8, label='P2_1')
    else:
        plt.plot(time[:,k], P2_1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], T2_1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8, label='T2_1')
    else:
        plt.plot(time[:,k], T2_1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], CC_1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8, label='CC_1')
    else:
        plt.plot(time[:,k], CC_1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], Cn_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='Cn_1')
    else:
        plt.plot(time[:,k], Cn_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], Mp_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='Mp_1')
    else:
        plt.plot(time[:,k], Mp_1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time.shape[1]):
    if k == 0:
        plt.plot(time[:,k], Mt_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='Mt_1')
    else:
        plt.plot(time[:,k], Mt_1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('plot1', fontweight='bold')
plt.xlabel('time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot1.png'), dpi=100)
plt.show()


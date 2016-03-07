"""
    tellurium 1.3.1

    auto-generated code (2016-03-07T10:13:00)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_JanaWolf
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_JanaWolf'

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
model1.timeCourseSelections = ['[fructose_1_6_bisphosphate]', '[NAD]', '[glycerate_3_phosphate]', 'time', '[ATP]', '[NADH]', '[Acetyladehyde]', '[Glucose]', '[pyruvate]', '[ADP]', '[glyceraldehyde_3_phosphate]', '[External_acetaldehyde]']
task1[0] = model1.simulate(start=0.0, end=10.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <time1>
__var__time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__time.shape) == 1:
     __var__time.shape += (1,)
time1 = __var__time

# DataGenerator <Glucose1>
__var__Glucose = np.transpose(np.array([sim['[Glucose]'] for sim in task1]))
if len(__var__Glucose.shape) == 1:
     __var__Glucose.shape += (1,)
Glucose1 = __var__Glucose

# DataGenerator <fructose_1_6_bisphosphate1>
__var__fructose_1_6_bisphosphate = np.transpose(np.array([sim['[fructose_1_6_bisphosphate]'] for sim in task1]))
if len(__var__fructose_1_6_bisphosphate.shape) == 1:
     __var__fructose_1_6_bisphosphate.shape += (1,)
fructose_1_6_bisphosphate1 = __var__fructose_1_6_bisphosphate

# DataGenerator <glyceraldehyde_3_phosphate1>
__var__glyceraldehyde_3_phosphate = np.transpose(np.array([sim['[glyceraldehyde_3_phosphate]'] for sim in task1]))
if len(__var__glyceraldehyde_3_phosphate.shape) == 1:
     __var__glyceraldehyde_3_phosphate.shape += (1,)
glyceraldehyde_3_phosphate1 = __var__glyceraldehyde_3_phosphate

# DataGenerator <glycerate_3_phosphate1>
__var__glycerate_3_phosphate = np.transpose(np.array([sim['[glycerate_3_phosphate]'] for sim in task1]))
if len(__var__glycerate_3_phosphate.shape) == 1:
     __var__glycerate_3_phosphate.shape += (1,)
glycerate_3_phosphate1 = __var__glycerate_3_phosphate

# DataGenerator <pyruvate1>
__var__pyruvate = np.transpose(np.array([sim['[pyruvate]'] for sim in task1]))
if len(__var__pyruvate.shape) == 1:
     __var__pyruvate.shape += (1,)
pyruvate1 = __var__pyruvate

# DataGenerator <Acetyladehyde1>
__var__Acetyladehyde = np.transpose(np.array([sim['[Acetyladehyde]'] for sim in task1]))
if len(__var__Acetyladehyde.shape) == 1:
     __var__Acetyladehyde.shape += (1,)
Acetyladehyde1 = __var__Acetyladehyde

# DataGenerator <External_acetaldehyde1>
__var__External_acetaldehyde = np.transpose(np.array([sim['[External_acetaldehyde]'] for sim in task1]))
if len(__var__External_acetaldehyde.shape) == 1:
     __var__External_acetaldehyde.shape += (1,)
External_acetaldehyde1 = __var__External_acetaldehyde

# DataGenerator <ATP1>
__var__ATP = np.transpose(np.array([sim['[ATP]'] for sim in task1]))
if len(__var__ATP.shape) == 1:
     __var__ATP.shape += (1,)
ATP1 = __var__ATP

# DataGenerator <ADP1>
__var__ADP = np.transpose(np.array([sim['[ADP]'] for sim in task1]))
if len(__var__ADP.shape) == 1:
     __var__ADP.shape += (1,)
ADP1 = __var__ADP

# DataGenerator <NAD1>
__var__NAD = np.transpose(np.array([sim['[NAD]'] for sim in task1]))
if len(__var__NAD.shape) == 1:
     __var__NAD.shape += (1,)
NAD1 = __var__NAD

# DataGenerator <NADH1>
__var__NADH = np.transpose(np.array([sim['[NADH]'] for sim in task1]))
if len(__var__NADH.shape) == 1:
     __var__NADH.shape += (1,)
NADH1 = __var__NADH

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
        plt.plot(time1[:,k], Glucose1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='Glucose')
    else:
        plt.plot(time1[:,k], Glucose1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], fructose_1_6_bisphosphate1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='fructose_1_6_bisphosphate')
    else:
        plt.plot(time1[:,k], fructose_1_6_bisphosphate1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], glyceraldehyde_3_phosphate1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='glyceraldehyde_3_phosphate')
    else:
        plt.plot(time1[:,k], glyceraldehyde_3_phosphate1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], glycerate_3_phosphate1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='glycerate_3_phosphate')
    else:
        plt.plot(time1[:,k], glycerate_3_phosphate1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], pyruvate1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8, label='pyruvate')
    else:
        plt.plot(time1[:,k], pyruvate1[:,k], '-o', color='c', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], Acetyladehyde1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8, label='Acetyladehyde')
    else:
        plt.plot(time1[:,k], Acetyladehyde1[:,k], '-o', color='y', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], External_acetaldehyde1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8, label='External_acetaldehyde')
    else:
        plt.plot(time1[:,k], External_acetaldehyde1[:,k], '-o', color='k', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], ATP1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='ATP')
    else:
        plt.plot(time1[:,k], ATP1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], ADP1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8, label='ADP')
    else:
        plt.plot(time1[:,k], ADP1[:,k], '-o', color='b', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], NAD1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8, label='NAD')
    else:
        plt.plot(time1[:,k], NAD1[:,k], '-o', color='g', linewidth=1.5, markersize=3.0, alpha=0.8)
for k in range(time1.shape[1]):
    if k == 0:
        plt.plot(time1[:,k], NADH1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8, label='NADH')
    else:
        plt.plot(time1[:,k], NADH1[:,k], '-o', color='m', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('JanaWolf Glycolysis', fontweight='bold')
plt.xlabel('time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot1.png'), dpi=100)
plt.show()


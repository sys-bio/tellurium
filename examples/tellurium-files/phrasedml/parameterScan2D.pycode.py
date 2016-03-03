"""
    tellurium 1.3.1

    auto-generated code (2016-03-03T08:48:12)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpY88p3I_sedml/_te_parameterScan2D
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

workingDir = '/tmp/tmpY88p3I_sedml/_te_parameterScan2D'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model_3>
model_3 = te.loadSBMLModel(os.path.join(workingDir, 'parameterScan2D.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task_1>
task_1 = [None]
model_3.setIntegrator('cvode')
Config = model_3
model_3.conservedMoietyAnalysis = True
model_3.steadyStateSelections = []
model_3.steadyState()
task_1[0] = dict(zip(model_3.steadyStateSelections, model_3.getSteadyStateValues()))
model_3.conservedMoietyAnalysis = False

# Task <repeatedtask_1>
__range__vector_for_J1_KK2 = [1.0, 5.0, 10.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
repeatedtask_1 = [None]*len(__range__vector_for_J1_KK2)
for k in range(len(__range__vector_for_J1_KK2)):
    if k == 0:
        model_3.reset()
    __value__vector_for_J1_KK2 = __range__vector_for_J1_KK2[k]
    model_3['J1_KK2'] = __value__vector_for_J1_KK2
    model_3.setIntegrator('cvode')
    Config = model_3
    model_3.conservedMoietyAnalysis = True
    model_3.steadyStateSelections = []
    model_3.steadyState()
    repeatedtask_1[k] = dict(zip(model_3.steadyStateSelections, model_3.getSteadyStateValues()))
    model_3.conservedMoietyAnalysis = False

# Task <repeatedtask_2>
__range__uniform_linear_for_J4_KK5 = list(np.linspace(start=1.0, stop=40.0, num=101))
repeatedtask_2 = [None]*len(__range__uniform_linear_for_J4_KK5)
for k in range(len(__range__uniform_linear_for_J4_KK5)):

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__repeatedtask_2_____J4_KK5 = np.transpose(np.array([sim['J4_KK5'] for sim in repeatedtask_2]))
__var__repeatedtask_2_____J4_KK5 = np.concatenate(np.transpose(__var__repeatedtask_2_____J4_KK5))
if len(__var__repeatedtask_2_____J4_KK5.shape) == 1:
     __var__repeatedtask_2_____J4_KK5.shape += (1,)
plot_0_0_0 = __var__repeatedtask_2_____J4_KK5

# DataGenerator <plot_0_0_1>
__var__repeatedtask_2_____MKK = np.transpose(np.array([sim['MKK'] for sim in repeatedtask_2]))
__var__repeatedtask_2_____MKK = np.concatenate(np.transpose(__var__repeatedtask_2_____MKK))
if len(__var__repeatedtask_2_____MKK.shape) == 1:
     __var__repeatedtask_2_____MKK.shape += (1,)
plot_0_0_1 = __var__repeatedtask_2_____MKK

# DataGenerator <plot_0_1_1>
__var__repeatedtask_2_____MKK_P = np.transpose(np.array([sim['MKK_P'] for sim in repeatedtask_2]))
__var__repeatedtask_2_____MKK_P = np.concatenate(np.transpose(__var__repeatedtask_2_____MKK_P))
if len(__var__repeatedtask_2_____MKK_P.shape) == 1:
     __var__repeatedtask_2_____MKK_P.shape += (1,)
plot_0_1_1 = __var__repeatedtask_2_____MKK_P

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeatedtask_2.MKK')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='repeatedtask_2.MKK_P')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
plt.title('plot_0', fontweight='bold')
plt.xlabel('repeatedtask_2.J4_KK5', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()


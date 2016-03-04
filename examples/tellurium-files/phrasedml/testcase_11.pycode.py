"""
    tellurium 1.3.1

    auto-generated code (2016-03-04T15:02:26)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmpUeC6Mu_sedml/_te_testcase_11
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

workingDir = '/tmp/tmpUeC6Mu_sedml/_te_testcase_11'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_11.xml'))

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
for k, __value__vector_for_S1 in enumerate(__range__vector_for_S1):
    mod1['S1'] = __value__vector_for_S1
    
    rtask2 = []
    __range__uniform_linear_for_k2 = np.linspace(start=0.0, stop=1.0, num=6)
    for k, __value__uniform_linear_for_k2 in enumerate(__range__uniform_linear_for_k2):
        mod1['k2'] = __value__uniform_linear_for_k2
        
        rtask1 = []
        __range__uniform_linear_for_k1 = np.linspace(start=0.0, stop=1.0, num=6)
        for k, __value__uniform_linear_for_k1 in enumerate(__range__uniform_linear_for_k1):
            if k == 0:
                mod1.reset()
            mod1['k1'] = __value__uniform_linear_for_k1
            
            # execute simpleTask: <task1>
            task1 = [None]
            mod1.setIntegrator('cvode')
            mod1.timeCourseSelections = ['S2', 'S1', 'time']
            task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

        rtask1.extend(task1)

    rtask2.extend(rtask1)

rtask3.extend(rtask2)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__offsets__rtask3 = np.cumsum(np.array([sim['time'][-1] for sim in rtask3]))
__offsets__rtask3 = np.insert(__offsets__rtask3, 0, 0)
__var__rtask3_____time = np.transpose(np.array([sim['time']+__offsets__rtask3[k] for k, sim in enumerate(rtask3)]))
__var__rtask3_____time = np.concatenate(np.transpose(__var__rtask3_____time))
if len(__var__rtask3_____time.shape) == 1:
     __var__rtask3_____time.shape += (1,)
plot_0_0_0 = __var__rtask3_____time

# DataGenerator <plot_0_0_1>
__var__rtask3_____S1 = np.transpose(np.array([sim['S1'] for sim in rtask3]))
__var__rtask3_____S1 = np.concatenate(np.transpose(__var__rtask3_____S1))
if len(__var__rtask3_____S1.shape) == 1:
     __var__rtask3_____S1.shape += (1,)
plot_0_0_1 = __var__rtask3_____S1

# DataGenerator <plot_0_1_1>
__var__rtask3_____S2 = np.transpose(np.array([sim['S2'] for sim in rtask3]))
__var__rtask3_____S2 = np.concatenate(np.transpose(__var__rtask3_____S2))
if len(__var__rtask3_____S2.shape) == 1:
     __var__rtask3_____S2.shape += (1,)
plot_0_1_1 = __var__rtask3_____S2

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8, label='rtask3.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=4.0, alpha=0.8)
for k in range(plot_0_0_0.shape[1]):
    if k == 0:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8, label='rtask3.S2')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_1_1[:,k], '-o', color='b', linewidth=1.5, markersize=4.0, alpha=0.8)
plt.title('plot_0', fontweight='bold')
plt.xlabel('rtask3.time', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.show()


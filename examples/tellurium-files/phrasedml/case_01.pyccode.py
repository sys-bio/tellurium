"""
    tellurium 1.3.1

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_01
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

workingDir = '/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_01'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model0>
model0 = te.loadSBMLModel(os.path.join(workingDir, 'case_01.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
# Task: <task0>
task0 = [None]
model0.setIntegrator('cvode')
model0.timeCourseSelections = ['S1', 'time']
task0[0] = model0.simulate(start=0.0, end=10.0, steps=100)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task0_____time = np.transpose(np.array([sim['time'] for sim in task0]))
if len(__var__task0_____time.shape) == 1:
     __var__task0_____time.shape += (1,)
plot_0_0_0 = __var__task0_____time

# DataGenerator <plot_0_0_1>
__var__task0_____S1 = np.transpose(np.array([sim['S1'] for sim in task0]))
if len(__var__task0_____S1.shape) == 1:
     __var__task0_____S1.shape += (1,)
plot_0_0_1 = __var__task0_____S1

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='task0.S1')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], '-o', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('UniformTimecourse', fontweight='bold')
plt.xlabel('task0.time', fontweight='bold')
plt.ylabel('task0.S1', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()

# Output <report_1>
__dfs__report_1 = []
for k in range(plot_0_0_0.shape[1]):
    print('-'*80)
    print('report_1, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([plot_0_0_0[:,k], plot_0_0_1[:,k]]), 
    columns=['task0.time', 'task0.S1'])
    print(__df__k.head(10))
    __dfs__report_1.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_1_{}.csv'.format(k)), sep='	', index=False)


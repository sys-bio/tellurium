"""
    tellurium 1.3.3

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_07
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

workingDir = r'/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/_te_case_07'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <mod1>
mod1 = te.loadSBMLModel(os.path.join(workingDir, 'case_07.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# Task: <task1>
task1 = [None]
mod1.setIntegrator('cvode')
mod1.timeCourseSelections = ['[S1]', '[S2]', 'time']
task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

# Task <repeat1>

repeat1 = []
__range__vector_for_S1 = [1.0, 3.0, 5.0]
for __k__vector_for_S1, __value__vector_for_S1 in enumerate(__range__vector_for_S1):
    mod1.reset()
    # Task: <task1>
    task1 = [None]
    mod1.setIntegrator('cvode')
    mod1['init([S1])'] = __value__vector_for_S1
    mod1.timeCourseSelections = ['[S2]', 'time', '[S1]']
    task1[0] = mod1.simulate(start=0.0, end=10.0, steps=100)

    repeat1.extend(task1)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <report_0_0_0>
__var__task1_____time = np.transpose(np.array([sim['time'] for sim in task1]))
if len(__var__task1_____time.shape) == 1:
     __var__task1_____time.shape += (1,)
report_0_0_0 = __var__task1_____time

# DataGenerator <report_0_0_1>
__var__task1_____S1 = np.transpose(np.array([sim['[S1]'] for sim in task1]))
if len(__var__task1_____S1.shape) == 1:
     __var__task1_____S1.shape += (1,)
report_0_0_1 = __var__task1_____S1

# DataGenerator <report_0_0_2>
__var__task1_____S2 = np.transpose(np.array([sim['[S2]'] for sim in task1]))
if len(__var__task1_____S2.shape) == 1:
     __var__task1_____S2.shape += (1,)
report_0_0_2 = __var__task1_____S2

# DataGenerator <report_0_0_3>
__var__task1_____S1 = np.transpose(np.array([sim['[S1]'] for sim in task1]))
if len(__var__task1_____S1.shape) == 1:
     __var__task1_____S1.shape += (1,)
__var__task1_____S2 = np.transpose(np.array([sim['[S2]'] for sim in task1]))
if len(__var__task1_____S2.shape) == 1:
     __var__task1_____S2.shape += (1,)
report_0_0_3 = __var__task1_____S1 / __var__task1_____S2

# DataGenerator <report_1_0_0>
__var__repeat1_____time = np.transpose(np.array([sim['time'] for sim in repeat1]))
if len(__var__repeat1_____time.shape) == 1:
     __var__repeat1_____time.shape += (1,)
report_1_0_0 = __var__repeat1_____time

# DataGenerator <report_1_0_1>
__var__repeat1_____S1 = np.transpose(np.array([sim['[S1]'] for sim in repeat1]))
if len(__var__repeat1_____S1.shape) == 1:
     __var__repeat1_____S1.shape += (1,)
report_1_0_1 = __var__repeat1_____S1

# DataGenerator <report_1_0_2>
__var__repeat1_____S2 = np.transpose(np.array([sim['[S2]'] for sim in repeat1]))
if len(__var__repeat1_____S2.shape) == 1:
     __var__repeat1_____S2.shape += (1,)
report_1_0_2 = __var__repeat1_____S2

# DataGenerator <report_1_0_3>
__var__repeat1_____S1 = np.transpose(np.array([sim['[S1]'] for sim in repeat1]))
if len(__var__repeat1_____S1.shape) == 1:
     __var__repeat1_____S1.shape += (1,)
__var__repeat1_____S2 = np.transpose(np.array([sim['[S2]'] for sim in repeat1]))
if len(__var__repeat1_____S2.shape) == 1:
     __var__repeat1_____S2.shape += (1,)
report_1_0_3 = __var__repeat1_____S1 / __var__repeat1_____S2

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <report_0>
__dfs__report_0 = []
for k in range(report_0_0_0.shape[1]):
    print('-'*80)
    print('report_0, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([report_0_0_0[:,k], report_0_0_1[:,k], report_0_0_2[:,k], report_0_0_3[:,k]]), 
    columns=['task1.time', 'task1.S1', 'task1.S2', 'task1.S1/task1.S2'])
    print(__df__k.head(5))
    __dfs__report_0.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_0_{}.csv'.format(k)), sep='	', index=False)

# Output <report_1>
__dfs__report_1 = []
for k in range(report_1_0_0.shape[1]):
    print('-'*80)
    print('report_1, Repeat:', k)
    print('-'*80)
    __df__k = pandas.DataFrame(np.column_stack([report_1_0_0[:,k], report_1_0_1[:,k], report_1_0_2[:,k], report_1_0_3[:,k]]), 
    columns=['repeat1.time', 'repeat1.S1', 'repeat1.S2', 'repeat1.S1/repeat1.S2'])
    print(__df__k.head(5))
    __dfs__report_1.append(__df__k)
    __df__k.to_csv(os.path.join(workingDir, 'report_1_{}.csv'.format(k)), sep='	', index=False)


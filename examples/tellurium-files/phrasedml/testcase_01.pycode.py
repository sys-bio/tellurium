"""
    tellurium 1.3.1

    auto-generated code (2016-03-01T12:13:21)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmphoozdS_sedml/_te_testcase_01
    inputType: COMBINE_FILE
"""
from __future__ import print_function, division
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import pandas
import os.path

workingDir = '/tmp/tmphoozdS_sedml/_te_testcase_01'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - model0 

# Model <model0>
model0 = te.loadSBMLModel(os.path.join(workingDir, 'testcase_01.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task0 

# Task <task0>
task0 = [None]
model0.setIntegrator('cvode')
model0.timeCourseSelections = ['S1', 'time']
task0[0] = model0.simulate(start=0.0, end=10.0, steps=100)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - plot_0_0_0 (task0.time)
#  - plot_0_0_1 (task0.S1)

# DataGenerator <plot_0_0_0>
plot_0_0_0 = [sim['time'] for sim in task0]

# DataGenerator <plot_0_0_1>
plot_0_0_1 = [sim['S1'] for sim in task0]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot_0 

# Output <plot_0>
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5, label='S1')
    else:
        plt.plot(plot_0_0_0[k], plot_0_0_1[k], '-o', color='b', linewidth=1.5)
plt.title('plot_0')
plt.legend()
plt.show()


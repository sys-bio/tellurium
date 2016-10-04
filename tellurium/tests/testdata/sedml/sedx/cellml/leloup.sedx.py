"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:05:50)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_leloup
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_leloup'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - leloup_gonze_goldbeter_1999_a_cellml 

# Model <leloup_gonze_goldbeter_1999_a_cellml>
leloup_gonze_goldbeter_1999_a_cellml = te.loadCellMLModel(os.path.join(workingDir, 'model1.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - sim1_task1 

# Task <sim1_task1>
sim1_task1 = [None]
leloup_gonze_goldbeter_1999_a_cellml.setIntegrator('cvode')
leloup_gonze_goldbeter_1999_a_cellml.timeCourseSelections = ['MT', 'MP', 'time']
sim1_task1[0] = leloup_gonze_goldbeter_1999_a_cellml.simulate(start=0.0, end=100.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - dg_environment_time (environment_time)
#  - dg_MP_MP (MP_MP)
#  - dg_MT_MT (MT_MT)

# DataGenerator <dg_environment_time>
dg_environment_time = [sim['time'] for sim in sim1_task1]

# DataGenerator <dg_MP_MP>
dg_MP_MP = [sim['MP'] for sim in sim1_task1]

# DataGenerator <dg_MT_MT>
dg_MT_MT = [sim['MT'] for sim in sim1_task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 

# Output <plot1>
for k in range(len(dg_environment_time)):
    if k == 0:
        plt.plot(dg_environment_time[k], dg_MP_MP[k], color='b', linewidth=1.5, label='MP')
    else:
        plt.plot(dg_environment_time[k], dg_MP_MP[k], color='b', linewidth=1.5)
for k in range(len(dg_environment_time)):
    if k == 0:
        plt.plot(dg_environment_time[k], dg_MT_MT[k], color='g', linewidth=1.5, label='MT')
    else:
        plt.plot(dg_environment_time[k], dg_MT_MT[k], color='g', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


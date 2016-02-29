"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:11)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sed-ml
    inputType: SEDML_FILE
"""
from __future__ import print_function, division
import tellurium as te
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
#  - model1 (Curien)

# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, '../models/curien.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 (time course simulation with standard parameters)

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[Phser]', 'time']
task1[0] = model1.simulate(start=0.0, end=500.0, steps=500)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (Time)
#  - uM (Metabolites)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <uM>
uM = [sim['[Phser]'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (Number of metabolite Phser over time)

# Output <plot1>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], uM[k], color='b', linewidth=1.5, label='[Phser]')
    else:
        plt.plot(time[k], uM[k], color='b', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


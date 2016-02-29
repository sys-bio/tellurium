"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:02)
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
#  - model1 
#  - model2 

# Model <model1>
import tellurium.temiriam as temiriam
__model1_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000021')
model1 = te.loadSBMLModel(__model1_sbml)
# Model <model2>
import tellurium.temiriam as temiriam
__model2_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000021')
model2 = te.loadSBMLModel(__model2_sbml)
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id="V_dT"]/@value 4.8
model2['V_dT'] = 4.8
# /sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id="V_mT"]/@value 0.28
model2['V_mT'] = 0.28

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 
#  - task2 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['[Mt]', 'time']
model1.simulate(start=0.0, end=50.0, points=2)
task1[0] = model1.simulate(start=50.0, end=1000.0, steps=1000)

# Task <task2>
task2 = [None]
model2.setIntegrator('cvode')
model2.timeCourseSelections = ['[Mt]']
model2.simulate(start=0.0, end=50.0, points=2)
task2[0] = model2.simulate(start=50.0, end=1000.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (time)
#  - tim1 (tim1)
#  - tim2 (tim2)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <tim1>
tim1 = [sim['[Mt]'] for sim in task1]

# DataGenerator <tim2>
tim2 = [sim['[Mt]'] for sim in task2]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (tim mRNA with Oscillation and Chaos)

# Output <plot1>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], tim1[k], color='b', linewidth=1.5, label='[Mt]')
    else:
        plt.plot(time[k], tim1[k], color='b', linewidth=1.5)
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], tim2[k], color='g', linewidth=1.5, label='[Mt]')
    else:
        plt.plot(time[k], tim2[k], color='g', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


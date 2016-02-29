"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T17:11:12)
    sedmlDoc: L1V1  
    workingDir: /home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_BIOMD0000000139
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

workingDir = '/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/sedx/_te_BIOMD0000000139'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - model1 

# Model <model1>
import tellurium.temiriam as temiriam
__model1_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000139')
model1 = te.loadSBMLModel(__model1_sbml)

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['Total_NFkBn', 'time']
task1[0] = model1.simulate(start=0.0, end=2500.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (time)
#  - Total_NFkBn (Total_NFkBn)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <Total_NFkBn>
Total_NFkBn = [sim['Total_NFkBn'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (BM139 Total_NFkBn)

# Output <plot1>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Total_NFkBn[k], color='b', linewidth=1.5, label='Total_NFkBn')
    else:
        plt.plot(time[k], Total_NFkBn[k], color='b', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()


"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T16:36:12)
    sedmlDoc: L1V2  
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

# Model <model1>
import tellurium.temiriam as temiriam
__model1_sbml = temiriam.getSBMLFromBiomodelsURN('urn:miriam:biomodels.db:BIOMD0000000140')
model1 = te.loadSBMLModel(__model1_sbml)

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task1 

# Task <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['Total_IkBeps', 'Total_NFkBn', 'Total_IkBalpha', 'Total_IkBbeta', 'time']
task1[0] = model1.simulate(start=0.0, end=2500.0, steps=1000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - time (time)
#  - Total_NFkBn (Total_NFkBn)
#  - Total_IkBbeta (Total_IkBbeta)
#  - Total_IkBeps (Total_IkBeps)
#  - Total_IkBalpha (Total_IkBalpha)

# DataGenerator <time>
time = [sim['time'] for sim in task1]

# DataGenerator <Total_NFkBn>
Total_NFkBn = [sim['Total_NFkBn'] for sim in task1]

# DataGenerator <Total_IkBbeta>
Total_IkBbeta = [sim['Total_IkBbeta'] for sim in task1]

# DataGenerator <Total_IkBeps>
Total_IkBeps = [sim['Total_IkBeps'] for sim in task1]

# DataGenerator <Total_IkBalpha>
Total_IkBalpha = [sim['Total_IkBalpha'] for sim in task1]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (BM140 Total_NFkBn)
#  - plot2 (BM140 Total_IkBbeta)
#  - plot3 (BM140 Total_IkBeps)
#  - plot4 (BM140 Total_IkBalpha)

# Output <plot1>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Total_NFkBn[k], color='b', linewidth=1.5, label='Total_NFkBn')
    else:
        plt.plot(time[k], Total_NFkBn[k], color='b', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()

# Output <plot2>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Total_IkBbeta[k], color='b', linewidth=1.5, label='Total_IkBbeta')
    else:
        plt.plot(time[k], Total_IkBbeta[k], color='b', linewidth=1.5)
plt.title('plot2')
plt.legend()
plt.show()

# Output <plot3>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Total_IkBeps[k], color='b', linewidth=1.5, label='Total_IkBeps')
    else:
        plt.plot(time[k], Total_IkBeps[k], color='b', linewidth=1.5)
plt.title('plot3')
plt.legend()
plt.show()

# Output <plot4>
for k in range(len(time)):
    if k == 0:
        plt.plot(time[k], Total_IkBalpha[k], color='b', linewidth=1.5, label='Total_IkBalpha')
    else:
        plt.plot(time[k], Total_IkBalpha[k], color='b', linewidth=1.5)
plt.title('plot4')
plt.legend()
plt.show()


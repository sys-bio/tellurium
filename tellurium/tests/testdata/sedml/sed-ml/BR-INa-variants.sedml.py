"""
    tellurium 1.3.1

    auto-generated code (2016-02-29T15:26:22)
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
#  - BR 
#  - BREJ 
#  - BRDR 

# Model <BR>
BR = te.loadCellMLModel('http://models.cellml.org/workspace/a1/@@rawfile/7bc23d0526e23d54d45e1fb7deda0f55d7f0f086/models/1977_beeler/experiments/periodic-stimulus.xml')
# Model <BREJ>
BREJ = te.loadCellMLModel('http://models.cellml.org/workspace/a1/@@rawfile/7bc23d0526e23d54d45e1fb7deda0f55d7f0f086/models/1977_beeler/experiments/1980_ebihara_johnson.xml')
# Model <BRDR>
BRDR = te.loadCellMLModel('http://models.cellml.org/workspace/a1/@@rawfile/7bc23d0526e23d54d45e1fb7deda0f55d7f0f086/models/1977_beeler/experiments/1987_drouhard_roberge.xml')

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - BRtask 
#  - BREJtask 
#  - BRDRtask 

# Task <BRtask>
BRtask = [None]
BR.setIntegrator('cvode')
BR.timeCourseSelections = ["time']/cellml:variabl", "exposed_variables']/cellml:variabl"]
BRtask[0] = BR.simulate(start=0.0, end=1500.0, steps=1500)

# Task <BREJtask>
BREJtask = [None]
BREJ.setIntegrator('cvode')
BREJ.timeCourseSelections = ["time']/cellml:variabl", "fast_sodium_current']/cellml:variabl"]
BREJtask[0] = BREJ.simulate(start=0.0, end=1500.0, steps=1500)

# Task <BRDRtask>
BRDRtask = [None]
BRDR.setIntegrator('cvode')
BRDR.timeCourseSelections = ["time']/cellml:variabl", "fast_sodium_current']/cellml:variabl"]
BRDRtask[0] = BRDR.simulate(start=0.0, end=1500.0, steps=1500)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - BRtime (BR time)
#  - BRVm (BR Vm)
#  - BREJtime (BREJ time)
#  - BREJVm (BREJ Vm)
#  - BRDRtime (BRDR time)
#  - BRDRVm (BRDR Vm)

# DataGenerator <BRtime>
BRtime = [sim['time']/cellml:variabl'] for sim in BRtask]

# DataGenerator <BRVm>
BRVm = [sim['exposed_variables']/cellml:variabl'] for sim in BRtask]

# DataGenerator <BREJtime>
BREJtime = [sim['time']/cellml:variabl'] for sim in BREJtask]

# DataGenerator <BREJVm>
BREJVm = [sim['fast_sodium_current']/cellml:variabl'] for sim in BREJtask]

# DataGenerator <BRDRtime>
BRDRtime = [sim['time']/cellml:variabl'] for sim in BRDRtask]

# DataGenerator <BRDRVm>
BRDRVm = [sim['fast_sodium_current']/cellml:variabl'] for sim in BRDRtask]

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
#  - plot1 (Action Potentials)

# Output <plot1>
for k in range(len(BRtime)):
    if k==0:
        plt.plot(BRtime[k], BRVm[k], color='b', linewidth=1.5, label='exposed_variables']/cellml:variabl')
    else:
        plt.plot(BRtime[k], BRVm[k], color='b', linewidth=1.5)
for k in range(len(BREJtime)):
    if k==0:
        plt.plot(BREJtime[k], BREJVm[k], color='g', linewidth=1.5, label='fast_sodium_current']/cellml:variabl')
    else:
        plt.plot(BREJtime[k], BREJVm[k], color='g', linewidth=1.5)
for k in range(len(BRDRtime)):
    if k==0:
        plt.plot(BRDRtime[k], BRDRVm[k], color='r', linewidth=1.5, label='fast_sodium_current']/cellml:variabl')
    else:
        plt.plot(BRDRtime[k], BRDRVm[k], color='r', linewidth=1.5)
plt.title('plot1')
plt.legend()
plt.show()

"""
    tellurium 2.0.0

    auto-generated code
    sedmlDoc: L1V2
    workingDir: /tmp/tmp85ho_9d1_sedml/_te_m1
    inputType: COMBINE_FILE
"""
import tellurium as te
from roadrunner import Config
from tellurium.sedml.mathml import *
from tellurium.sedml.tesedml import process_trace, terminate_trace
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
try:
    import tesedml as libsedml
except ImportError:
    import libsedml
import pandas
import os.path
Config.LOADSBMLOPTIONS_RECOMPILE = True

workingDir = r'/tmp/tmp85ho_9d1_sedml/_te_m1'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model0>
model0 = te.loadSBMLModel(os.path.join(workingDir, 'm1.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
# Task: <task0>
task0 = [None]
model0.setIntegrator('cvode')
model0.integrator.setValue('absolute_tolerance', 1e-08)
if model0.conservedMoietyAnalysis == True: model0.conservedMoietyAnalysis = False
model0.timeCourseSelections = ['time', '[S1]']
model0.reset()
task0[0] = model0.simulate(start=0.0, end=10.0, steps=100)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task0_____time = np.concatenate([process_trace(sim['time']) for sim in task0])
if len(__var__task0_____time.shape) == 1:
     __var__task0_____time.shape += (1,)
plot_0_0_0 = __var__task0_____time

# DataGenerator <plot_0_0_1>
__var__task0_____S1 = np.concatenate([process_trace(sim['[S1]']) for sim in task0])
if len(__var__task0_____S1.shape) == 1:
     __var__task0_____S1.shape += (1,)
plot_0_0_1 = __var__task0_____S1

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot_0>
stacked=False
if not stacked:
    fig = te.getPlottingEngine().newFigure(title='plot_0')
else:
    fig = te.getPlottingEngine().newStackedFigure(title='plot_0')
if plot_0_0_0.shape[1] > 1:
    for k in range(plot_0_0_0.shape[1]):
        if k == 0:
            fig.addXYDataset(plot_0_0_0[:,k], plot_0_0_1[:,k], color='C0', tag='tag0', name='task0.S1')
        else:
            fig.addXYDataset(plot_0_0_0[:,k], plot_0_0_1[:,k], color='C0', tag='tag0')
else:
    for k in range(plot_0_0_0.shape[1]):
        if k == 0:
            fig.addXYDataset(plot_0_0_0[:,k], plot_0_0_1[:,k], color='C0', tag='tag0', name='task0.S1')
        else:
            fig.addXYDataset(plot_0_0_0[:,k], plot_0_0_1[:,k], color='C0', tag='tag0')
fig.render()
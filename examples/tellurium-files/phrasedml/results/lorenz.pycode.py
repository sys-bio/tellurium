"""
    tellurium 1.3.5

    auto-generated code
    sedmlDoc: L1V2  
    workingDir: /home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/results/_te_lorenz
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

workingDir = r'/home/mkoenig/git/tellurium/examples/tellurium-files/phrasedml/results/_te_lorenz'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'lorenz.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task1>
# Task: <task1>
task1 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = ['x', 'z']
task1[0] = model1.simulate(start=0.0, end=15.0, steps=2000)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task1_____z = np.transpose(np.array([sim['z'] for sim in task1]))
if len(__var__task1_____z.shape) == 1:
     __var__task1_____z.shape += (1,)
plot_0_0_0 = __var__task1_____z

# DataGenerator <plot_0_0_1>
__var__task1_____x = np.transpose(np.array([sim['x'] for sim in task1]))
if len(__var__task1_____x.shape) == 1:
     __var__task1_____x.shape += (1,)
plot_0_0_1 = __var__task1_____x

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
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], marker = '.', color='r', linewidth=1.5, markersize=3.0, alpha=0.8, label='task1.x')
    else:
        plt.plot(plot_0_0_0[:,k], plot_0_0_1[:,k], marker = '.', color='r', linewidth=1.5, markersize=3.0, alpha=0.8)
plt.title('plot_0', fontweight='bold')
plt.xlabel('task1.z', fontweight='bold')
plt.ylabel('task1.x', fontweight='bold')
__lg = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
__lg.draw_frame(False)
plt.setp(__lg.get_texts(), fontsize='small')
plt.setp(__lg.get_texts(), fontweight='bold')
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()


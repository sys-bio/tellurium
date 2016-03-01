"""
    tellurium 1.3.1

    auto-generated code (2016-03-01T12:05:47)
    sedmlDoc: L1V2  
    workingDir: /tmp/tmp7bXZxr_sedml/_te_onestep
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

workingDir = '/tmp/tmp7bXZxr_sedml/_te_onestep'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
#  - model1 

# Model <model1>
model1 = te.loadSBMLModel(os.path.join(workingDir, 'onestep.xml'))

# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
#  - task0 
#  - task1 

# Task <task0>
task0 = [None]
model1.setIntegrator('cvode')
model1.timeCourseSelections = []
task0[0] = model1.simulate(start=0.0, end=0.1, points=2)

# Task <task1>
__range_task1 = [0.0, 0.10101010101010101, 0.20202020202020202, 0.30303030303030304, 0.40404040404040403, 0.50505050505050508, 0.60606060606060608, 0.70707070707070707, 0.80808080808080807, 0.90909090909090906, 1.0101010101010102, 1.1111111111111112, 1.2121212121212122, 1.3131313131313131, 1.4141414141414141, 1.5151515151515151, 1.6161616161616161, 1.7171717171717171, 1.8181818181818181, 1.9191919191919191, 2.0202020202020203, 2.1212121212121211, 2.2222222222222223, 2.3232323232323231, 2.4242424242424243, 2.5252525252525251, 2.6262626262626263, 2.7272727272727271, 2.8282828282828283, 2.9292929292929291, 3.0303030303030303, 3.131313131313131, 3.2323232323232323, 3.3333333333333335, 3.4343434343434343, 3.5353535353535355, 3.6363636363636362, 3.7373737373737375, 3.8383838383838382, 3.9393939393939394, 4.0404040404040407, 4.141414141414141, 4.2424242424242422, 4.3434343434343434, 4.4444444444444446, 4.545454545454545, 4.6464646464646462, 4.7474747474747474, 4.8484848484848486, 4.9494949494949498, 5.0505050505050502, 5.1515151515151514, 5.2525252525252526, 5.3535353535353538, 5.4545454545454541, 5.5555555555555554, 5.6565656565656566, 5.7575757575757578, 5.8585858585858581, 5.9595959595959593, 6.0606060606060606, 6.1616161616161618, 6.2626262626262621, 6.3636363636363633, 6.4646464646464645, 6.5656565656565657, 6.666666666666667, 6.7676767676767673, 6.8686868686868685, 6.9696969696969697, 7.0707070707070709, 7.1717171717171713, 7.2727272727272725, 7.3737373737373737, 7.4747474747474749, 7.5757575757575752, 7.6767676767676765, 7.7777777777777777, 7.8787878787878789, 7.9797979797979792, 8.0808080808080813, 8.1818181818181817, 8.282828282828282, 8.3838383838383841, 8.4848484848484844, 8.5858585858585865, 8.6868686868686869, 8.7878787878787872, 8.8888888888888893, 8.9898989898989896, 9.0909090909090899, 9.191919191919192, 9.2929292929292924, 9.3939393939393945, 9.4949494949494948, 9.5959595959595951, 9.6969696969696972, 9.7979797979797976, 9.8989898989898997, 10.0]
task1 = [None] * len(__range_task1)
for k, value in enumerate(__range_task1):
    model1['J0_v0'] = value
    model1.setIntegrator('cvode')
    model1.timeCourseSelections = ['S2', 'S1', 'J0_v0', 'time']
    task1[k] = model1.simulate(start=0.0, end=0.1, points=2)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
#  - plot_0_0_0 (task1.time)
#  - plot_0_0_1 (task1.S1)
#  - plot_0_1_1 (task1.S2)
#  - plot_0_2_1 (task1.J0_v0)

# DataGenerator <plot_0_0_0>
plot_0_0_0 = [sim['time'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_0_0 = [np.cumsum(plot_0_0_0)]

# DataGenerator <plot_0_0_1>
plot_0_0_1 = [sim['S1'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_0_1 = [np.concatenate(plot_0_0_1)]

# DataGenerator <plot_0_1_1>
plot_0_1_1 = [sim['S2'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_1_1 = [np.concatenate(plot_0_1_1)]

# DataGenerator <plot_0_2_1>
plot_0_2_1 = [sim['J0_v0'] for sim in task1]
# resetModel=False in RepeatedTask
plot_0_2_1 = [np.concatenate(plot_0_2_1)]

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
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5, label='S2')
    else:
        plt.plot(plot_0_0_0[k], plot_0_1_1[k], '-o', color='g', linewidth=1.5)
for k in range(len(plot_0_0_0)):
    if k == 0:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5, label='J0_v0')
    else:
        plt.plot(plot_0_0_0[k], plot_0_2_1[k], '-o', color='r', linewidth=1.5)
plt.title('plot_0')
plt.legend()
plt.show()


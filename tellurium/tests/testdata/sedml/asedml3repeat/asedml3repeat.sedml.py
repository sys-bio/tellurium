# Translated SED-ML
# Beginning of generated script
import roadrunner
import numpy as np
import matplotlib.pyplot as plt

# Execute the tasks of model: Application0
Application0 = roadrunner.RoadRunner()
Application0.load('/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/asedml3repeat/asedml3repeat_Application0.xml')

Application0.simulateOptions.resetModel = True

Application0.model["init([s1])"] = 10.0
Application0.timeCourseSelections = ["time","s0","s1"]
rt_0_0_0 = Application0.simulate(0, 30, 1000)

Application0.model["init([s1])"] = 20.0
Application0.timeCourseSelections = ["time","s0","s1"]
rt_0_0_1 = Application0.simulate(0, 30, 1000)

Application0.model["init([s1])"] = 30.0
Application0.timeCourseSelections = ["time","s0","s1"]
rt_0_0_2 = Application0.simulate(0, 30, 1000)

# List of Data Generators
time_rt_0_0_0 = rt_0_0_0[0:,0]
dGen_rt_0_0_s0_0 = rt_0_0_0[0:,1]
dGen_rt_0_0_s1_0 = rt_0_0_0[0:,2]

time_rt_0_0_1 = rt_0_0_1[0:,0]
dGen_rt_0_0_s0_1 = rt_0_0_1[0:,1]
dGen_rt_0_0_s1_1 = rt_0_0_1[0:,2]

time_rt_0_0_2 = rt_0_0_2[0:,0]
dGen_rt_0_0_s0_2 = rt_0_0_2[0:,1]
dGen_rt_0_0_s1_2 = rt_0_0_2[0:,2]

# List of Outputs
Y_0 = np.array([dGen_rt_0_0_s0_0, dGen_rt_0_0_s1_0]).T
plt.plot(time_rt_0_0_0, Y_0)
plt.title('Application0plots')
plt.show()

# End of generated script

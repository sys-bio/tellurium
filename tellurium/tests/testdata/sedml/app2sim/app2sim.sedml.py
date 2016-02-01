# Translated SED-ML
# Beginning of generated script
import roadrunner
import numpy as np
import matplotlib.pyplot as plt

# Execute the tasks of model: Application0
Application0 = roadrunner.RoadRunner()
Application0.load('/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/app2sim/BioModel1_Application0.xml')
Application0.timeCourseSelections = ["time","s0","s1"]
t_0_0 = Application0.simulate(0, 20, 1000)

# Execute the tasks of model: Application0_0
Application0_0 = roadrunner.RoadRunner()
Application0_0.load('/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/app2sim/BioModel1_Application0.xml')
Application0_0.model["init([s1])"] = 10.0
Application0_0.timeCourseSelections = ["time","s0","s1"]
t_0_1 = Application0_0.simulate(0, 30, 1000)

# List of Data Generators
time_t_0_0 = t_0_0[0:,0]
dGen_t_0_0_s0 = t_0_0[0:,1]
dGen_t_0_0_s1 = t_0_0[0:,2]

time_t_0_1 = t_0_1[0:,0]
dGen_t_0_1_s0 = t_0_1[0:,1]
dGen_t_0_1_s1 = t_0_1[0:,2]

# List of Outputs
Y_0 = np.array([dGen_t_0_0_s0, dGen_t_0_0_s1]).T
plt.plot(time_t_0_0, Y_0)
plt.title('Application0plots')
plt.show()

Y_1 = np.array([dGen_t_0_1_s0, dGen_t_0_1_s1]).T
plt.plot(time_t_0_1, Y_1)
plt.title('Application0plots')
plt.show()

# End of generated script

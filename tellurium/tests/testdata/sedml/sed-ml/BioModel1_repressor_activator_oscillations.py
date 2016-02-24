# Translated SED-ML
# Beginning of generated script
import roadrunner
import numpy as np
import matplotlib.pyplot as plt

# Execute the tasks of model: repressor_activator_oscillations
repressor_activator_oscillations = roadrunner.RoadRunner()
repressor_activator_oscillations.load('/home/mkoenig/git/tellurium/tellurium/tests/testdata/sedml/constant_maybe/BioModel1_repressor_activator_oscillations.xml')

repressor_activator_oscillations.simulateOptions.resetModel = True

repressor_activator_oscillations.model["common_delta_A"] = 0.2
repressor_activator_oscillations.timeCourseSelections = ["time","mRNA_R","A","R","PrmA","PrmR","C","PrmA_bound","PrmR_bound","mRNA_A_"]
rt_0_0_0 = repressor_activator_oscillations.simulate(0, 200, 400)

repressor_activator_oscillations.model["common_delta_A"] = 0.6
repressor_activator_oscillations.timeCourseSelections = ["time","mRNA_R","A","R","PrmA","PrmR","C","PrmA_bound","PrmR_bound","mRNA_A_"]
rt_0_0_1 = repressor_activator_oscillations.simulate(0, 200, 400)

repressor_activator_oscillations.model["common_delta_A"] = 1.0
repressor_activator_oscillations.timeCourseSelections = ["time","mRNA_R","A","R","PrmA","PrmR","C","PrmA_bound","PrmR_bound","mRNA_A_"]
rt_0_0_2 = repressor_activator_oscillations.simulate(0, 200, 400)

# List of Data Generators
time_rt_0_0_0 = rt_0_0_0[0:,0]
dGen_rt_0_0_mRNA_R_0 = rt_0_0_0[0:,1]
dGen_rt_0_0_A_0 = rt_0_0_0[0:,2]
dGen_rt_0_0_R_0 = rt_0_0_0[0:,3]
dGen_rt_0_0_PrmA_0 = rt_0_0_0[0:,4]
dGen_rt_0_0_PrmR_0 = rt_0_0_0[0:,5]
dGen_rt_0_0_C_0 = rt_0_0_0[0:,6]
dGen_rt_0_0_PrmA_bound_0 = rt_0_0_0[0:,7]
dGen_rt_0_0_PrmR_bound_0 = rt_0_0_0[0:,8]
dGen_rt_0_0_mRNA_A__0 = rt_0_0_0[0:,9]

time_rt_0_0_1 = rt_0_0_1[0:,0]
dGen_rt_0_0_mRNA_R_1 = rt_0_0_1[0:,1]
dGen_rt_0_0_A_1 = rt_0_0_1[0:,2]
dGen_rt_0_0_R_1 = rt_0_0_1[0:,3]
dGen_rt_0_0_PrmA_1 = rt_0_0_1[0:,4]
dGen_rt_0_0_PrmR_1 = rt_0_0_1[0:,5]
dGen_rt_0_0_C_1 = rt_0_0_1[0:,6]
dGen_rt_0_0_PrmA_bound_1 = rt_0_0_1[0:,7]
dGen_rt_0_0_PrmR_bound_1 = rt_0_0_1[0:,8]
dGen_rt_0_0_mRNA_A__1 = rt_0_0_1[0:,9]

time_rt_0_0_2 = rt_0_0_2[0:,0]
dGen_rt_0_0_mRNA_R_2 = rt_0_0_2[0:,1]
dGen_rt_0_0_A_2 = rt_0_0_2[0:,2]
dGen_rt_0_0_R_2 = rt_0_0_2[0:,3]
dGen_rt_0_0_PrmA_2 = rt_0_0_2[0:,4]
dGen_rt_0_0_PrmR_2 = rt_0_0_2[0:,5]
dGen_rt_0_0_C_2 = rt_0_0_2[0:,6]
dGen_rt_0_0_PrmA_bound_2 = rt_0_0_2[0:,7]
dGen_rt_0_0_PrmR_bound_2 = rt_0_0_2[0:,8]
dGen_rt_0_0_mRNA_A__2 = rt_0_0_2[0:,9]

# List of Outputs
Y_0 = np.array([dGen_rt_0_0_mRNA_R_0, dGen_rt_0_0_A_0, dGen_rt_0_0_R_0, dGen_rt_0_0_PrmA_0, dGen_rt_0_0_PrmR_0, dGen_rt_0_0_C_0, dGen_rt_0_0_PrmA_bound_0, dGen_rt_0_0_PrmR_bound_0, dGen_rt_0_0_mRNA_A__0]).T
plt.plot(time_rt_0_0_0, Y_0)
plt.title('repressor_activator_oscillationsplots')
plt.show()

# End of generated script

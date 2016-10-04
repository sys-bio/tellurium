
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# #### Reset model values

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
r.integrator.setValue('variable_step_size', True)
# simulate model
sim1 = r.simulate(0, 5)
print('*** sim1 ***')
r.plot(sim1)

# continue from end concentration of sim1
r.k1 = 2.0
sim2 = r.simulate(0, 5)
print('-- sim2 --')
print('continue simulation from final concentrations with changed parameter')
r.plot(sim2)

# Reset initial concentrations, does not affect the changed parameter
r.reset()
sim3 = r.simulate(0, 5)
print('-- sim3 --')
print('reset initial concentrations but keep changed parameter')
r.plot(sim3)

# Reset model to the state it was loaded
r.resetToOrigin()
sim4 = r.simulate(0, 5)
print('-- sim4 --')
print('reset all to origin')
r.plot(sim4);


# In[2]:




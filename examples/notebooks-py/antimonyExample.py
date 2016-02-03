
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# ### Antimony model building
# Description Text

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

print('-' * 80)
te.printVersionInfo()
print('-' * 80)

r = te.loada('''
model example
    p1 = 0;
    at time>=10: p1=10;
    at time>=20: p1=0;
end
''')

# look at model
ant_str = r.getCurrentAntimony()
sbml_str = r.getCurrentSBML()
print(ant_str)
print(sbml_str)
# r.exportToSBML('/home/mkoenig/Desktop/test.xml')

# set selections
r.selections=['time', 'p1']
r.integrator.setValue("variable_step_size", False)
s1 = r.simulate(0, 40, 40)
r.plot()
print(s1)
# hitting the trigger point directly works
s2 = r.simulate(0, 40, 21)
r.plot()
print(s2)

# variable step size also does not work
r.integrator.setValue("variable_step_size", True)
s3 = r.simulate(0, 40)
r.plot()
print(s3)


# In[2]:

r.getSimulationData()


# In[3]:




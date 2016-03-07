
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# ### Model Loading
# To load models use the load functions
# 
# * `te.loadAntimony` (`te.loada`): load Antimony model
# * `te.loadSBML`: load SBML model
# * `te.loadCellML`: load CellML model

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

model = """
model test
    compartment C1;
    C1 = 1.0;
    species S1, S2;
    
    S1 = 10.0;
    S2 = 0.0;
    S1 in C1; S2 in C1;
    J1: S1 -> S2; k1*S1;
    
    k1 = 1.0;
end
"""
# load models
r = te.loada(model)


# ### Integrator and Integrator Settings
# To set the integrator use `r.setIntegrator(integrator)`.
# 
# To set integrator settings use `r.integrator.setValue(key, value)`. For instance
# 
# * `variable_step_size`
# * `stiff`
# * `absolute_tolerance`
# * `relative_tolerance`
# * `seed`

# In[2]:

# set integrator
r.setIntegrator('rk4')
r.setIntegrator('gillespie')
r.setIntegrator('cvode')

# set integrator settings
r.integrator.setValue('variable_step_size', False)
r.integrator.setValue('stiff', True)

# print integrator settings
print(r.integrator)


# ### Simulation options
# The simulation options 
# 
# * `start`: start time
# * `end`: end time
# * `points`: number of points in solution
# * `steps`: number of steps in solution
# 
# are set as arguments in `r.simulate`

# In[3]:

# simulate from 0 to 6 with 6 points in the result
r.reset()
res1 = r.simulate(start=0, end=10, points=6)
print(res1)
r.reset()
res2 = r.simulate(0, 10, 6)
print(res2)


# ### Selections
# Selections can be either given as argument to `r.simulate` or set via `r.selections`.

# In[4]:

# set selections directly
r.selections = ['time', 'J1']
print(r.simulate(0,10,6))
# provide arguments to simulate
print(r.simulate(0,10,6, selections=r.getFloatingSpeciesIds()))


# ### Reset model variables
# To reset variables use the `r.reset()` and `r.reset(SelectionRecord.*)` functions.

# In[5]:

# show the current values
for s in ['S1', 'S2']:
    print('r.{} == {}'.format(s, r[s]))
# reset initial concentrations
r.reset()
print('reset')
# S1 and S2 have now again the initial values
for s in ['S1', 'S2']:
    print('r.{} == {}'.format(s, r[s]))


# In[6]:




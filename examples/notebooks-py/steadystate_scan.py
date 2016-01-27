
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# ### Steady state scan
# Using `te.ParameterScan.SteadyStateScan` for scanning the steady state.

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te
import matplotlib.pyplot as plt
import tellurium as te
import numpy as np
from roadrunner import Config

Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, True) 

r = te.loada('''
    $Xo -> S1; vo;
    S1 -> S2; k1*S1 - k2*S2;
    S2 -> $X1; k3*S2;
    
    vo = 1
    k1 = 2; k2 = 0; k3 = 3;
''')

p = te.ParameterScan.SteadyStateScan(r)
p.value = 'k3'
p.startValue = 2
p.endValue = 3
p.numberOfPoints = 20
p.selection = ['S1', 'S2']
p.plotArray()

Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, False) 


# In[2]:




# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:06:52 2014

@author: mgaldzic
"""
import tellurium as te
# Simple UniUni reaction with first-order mass-action kinetics
model = '''
  model pathway()
     S1 -> S2; k1*S1

     # Initialize values
     S1 = 10; S2 = 0
     k1 = 1
  end
'''

# Load the model
r = te.loadAntimonyModel(model)

# Carry out a time course simulation
# results returned in array result.
# Arguments are: time start, time end, number of points
result = r.simulate (0, 10, 100)

# Plot the results
te.plotArray(result)
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:06:33 2014

@author: mgaldzic
"""
import tellurium as te
from roadrunner import Config

Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, True) 
model = '''
  model pathway()
     $Xo -> S1; k1*Xo - k2*S1
      S1 -> S2; k3*S2
      S2 -> $X1; k4*S2

     Xo = 1;   X1 = 0
     S1 = 0;   S2 = 0
     k1 = 0.1; k2 = 0.56
     k3 = 1.2; k4 = 0.9
  end
'''

r = te.loadAntimonyModel(model)

# Compute the steady state
r.getSteadyStateValues()
Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, False) 
print "S1 =", r.S1, ", S2 =", r.S2


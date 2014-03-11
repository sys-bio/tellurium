# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:53:42 2014

@author: mgaldzic
"""

import tellurium as te
#Single gene expressing protein and protein undergoing degradation
model = '''
  model mygene() 

      # Reactions: 
      J1:   -> P; Vm*T^4/(K+T^4)
      J2: P ->  ; k1*P; 

      # Species initializations: 
      P = 0;   T = 5; Vm = 10
      K = 0.5; k1 = 4.5;   
  end
''' 

r = te.loadAntimonyModel(model)
result = r.simulate(0, 10, 50)
te.plotArray(result)
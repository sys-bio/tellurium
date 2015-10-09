# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:04:25 2014

@author: mgaldzic
"""

# Example of Non-unit Stoichiometries
model = '''
  model pathway()
    S1 + S2 -> 2 S3; k1*S1*S2
    3 S3 -> 4 S4 + 6 S5; k2*S3^3
    k1 = 0.1;k2 = 0.1;
  end
'''
import tellurium as te
r = te.loadAntimonyModel(model)
# -*- coding: utf-8 -*-
"""
Example of Non-unit Stoichiometries.
"""
from __future__ import print_function
import tellurium as te

model = '''
  model pathway()
    S1 + S2 -> 2 S3; k1*S1*S2
    3 S3 -> 4 S4 + 6 S5; k2*S3^3
    k1 = 0.1;k2 = 0.1;
  end
'''
r = te.loada(model)
print(r)

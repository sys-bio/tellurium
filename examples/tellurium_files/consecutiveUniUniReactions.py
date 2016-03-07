# -*- coding: utf-8 -*-
"""
Consecutive UniUni reactions using first-order mass-action kinetics
"""
from __future__ import print_function
import tellurium as te

model = '''
  model pathway()
    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3

    # Initialize values
    S1 = 5; S2 = 0; S3 = 0; S4 = 0;
    k1 = 0.1;  k2 = 0.55; k3 = 0.76
  end
'''

r = te.loada(model)
result = r.simulate(0, 20, 50)
te.plotArray(result)

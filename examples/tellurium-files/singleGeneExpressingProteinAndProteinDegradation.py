# -*- coding: utf-8 -*-
"""
Single gene expressing protein and protein undergoing degradation.
"""
from __future__ import print_function
import tellurium as te

r = te.loada('''
model mygene()
  # Reactions:
  J1:   -> P; Vm*T^4/(K+T^4)
  J2: P ->  ; k1*P;

  # Species initializations:
  P = 0;   T = 5; Vm = 10
  K = 0.5; k1 = 4.5;
end
''')

result = r.simulate(0, 10, 51)
r.plot(result)

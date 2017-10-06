# -*- coding: utf-8 -*-
"""
Simple UniUni reaction with first-order mass-action kinetics.
"""
from __future__ import print_function
import tellurium as te

model = '''
model pathway()
    S1 -> S2; k1*S1

    # Initialize values
    S1 = 10; S2 = 0
    k1 = 1
end
'''

# load model
r = te.loada(model)

# carry out a time course simulation
# arguments are: start time, end time, number of points
result = r.simulate(0, 10, 100)

# plot results
r.plot(result)

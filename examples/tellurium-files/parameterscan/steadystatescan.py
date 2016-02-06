"""
Steady state scan.
"""
from __future__ import print_function, division
import tellurium as te
from roadrunner import Config

Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, True) 

model = '''
    $Xo -> S1; vo;
    S1 -> S2; k1*S1 - k2*S2;
    S2 -> $X1; k3*S2;
    
    vo = 1
    k1 = 2; k2 = 0; k3 = 3;
'''

    
rr = te.loada(model)

p = te.SteadyStateScan(rr,
    value='k3',
    startValue=2,
    endValue=3,
    numberOfPoints=20,
    selection=['S1', 'S2']                                     
)
p.plotArray()

Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, False) 
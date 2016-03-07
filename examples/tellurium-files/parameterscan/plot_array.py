"""
Plot array.
"""
from __future__ import print_function, division
import tellurium as te

model = '''
    $Xo -> S1; vo;
    S1 -> S2; k1*S1 - k2*S2;
    S2 -> $X1; k3*S2;
    
    vo = 1
    k1 = 2; k2 = 0; k3 = 3;
'''

rr = te.loada(model)
p = te.ParameterScan(rr,
    startTime = 0,
    endTime = 20,
    numberOfPoints = 50,
    width = 2,
    xlabel = 'Time',
    ylabel = 'Concentration',
    title = 'Cell')
p.plotArray()

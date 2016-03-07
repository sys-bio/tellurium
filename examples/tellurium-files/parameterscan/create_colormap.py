"""
Create a colormap.
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
# load model
rr = te.loada(model)

# perform parameter scan
colormap = te.ParameterScan.createColormap([.86, .08, .23], [.12, .56, 1])
p = te.ParameterScan(rr,
    endTime=3,
    colormap=colormap
)
p.createColorPoints()
p.plotSurface()

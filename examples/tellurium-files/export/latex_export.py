"""
Export simulation result to latex.
"""
from __future__ import print_function, division
import tellurium as te
import tempfile

model = '''
       $Xo -> S1; k1*Xo;
       S1 -> S2; k2*S1;
       S2 -> $X1; k3*S2; 
       
       Xo = 50; X1=0; S1 = 0; S2 = 0;
       k1 = 0.2; k2 = 0.4; k3 = 2;
'''

r = te.loada(model)
result = r.simulate(0, 30)
p = te.LatexExport(r,
                     color=['blue', 'green'],
                     legend=['S1', 'S2'],
                     xlabel='Time',
                     ylabel='Concentration',
                     exportComplete=True,
                     saveto=tempfile.mkdtemp(),
                     fileName='newModel')
p.saveToFile(result)

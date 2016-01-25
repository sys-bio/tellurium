"""
Export simulation result to latex.
"""
import tellurium as te

newModel = '''
       $Xo -> S1; k1*Xo;
       S1 -> S2; k2*S1;
       S2 -> $X1; k3*S2; 
       
       Xo = 50; S1 = 0; S2 = 0;
       k1 = 0.2; k2 = 0.4; k3 = 2;
'''

rr = te.loadAntimonyModel(newModel)
result = rr.simulate(0, 30)
p = te.Export.export(rr,
                     color=['blue', 'green'],
                     legend=['S1', 'S2'],
                     xlabel='Time',
                     ylabel='Concentration',
                     exportComplete=True,
                     saveto='./',
                     fileName='newModel')
p.saveToFile(result)

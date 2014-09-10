import tellurium as te
import teExport as ex

newModel = '''
       $Xo -> S1; k1*Xo;
       S1 -> S2; k2*S1;
       S2 -> $X1; k3*S2; 
       
       Xo = 50; S1 = 0; S2 = 0;
       k1 = 0.2; k2 = 0.4; k3 = 2;
'''

rr = te.loadAntimonyModel(newModel)
result = rr.simulate(0, 30)
p = ex.export(rr)

p.color = ['blue', 'green']
p.legend = ['S1', 'S2']
p.xlabel = 'Time'
p.ylabel = 'Concentration'
p.exportComplete = True
p.exportClipboard = True
p.location = 'C:\\Users\\user\\Documents\\LaTeX docs'
p.filename = 'newModel'
p.saveToFile(result)
p.getString()
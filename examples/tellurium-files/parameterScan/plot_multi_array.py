import tellurium as te

cell = '''
    $Xo -> S1; vo;
    S1 -> S2; k1*S1 - k2*S2;
    S2 -> $X1; k3*S2;
    
    vo = 1
    k1 = 2; k2 = 0; k3 = 3;
'''

rr = te.loadAntimonyModel(cell)
p = te.ParameterScan.ParameterScan(rr)

p.startTime = 0
p.endTime = 20
p.numberOfPoints = 50
p.width = 2
p.title = 'Cell'
p.selection = ['Time', 'S1', 'S2']

p.plotMultiArray('k1', [1, 1.5, 2], 'k3', [.5, 1, 1.5])

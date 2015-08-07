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
p.endTime = 3
p.colormap = p.createColormap([.86,.08,.23], [.12,.56,1])
p.createColorPoints()


p.plotSurface()

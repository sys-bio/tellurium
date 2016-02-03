# This script shows how to export run parameter scan and plot the output
# as a surface plot.
import tellurium as te

model = '''
    $Xo -> S1; vo;
    S1 -> S2; k1*S1 - k2*S2;
    S2 -> $X1; k3*S2;

    vo = 1
    k1 = 2; k2 = 0; k3 = 3;
    Xo = 0; S1 = 0; S2 = 0; X1 = 0;
'''

rr = te.loada(model)
p = te.ParameterScan.ParameterScan(rr)

p.startTime = 0
p.endTime = 6
p.numberOfPoints = 50
p.startValue = 1
p.endValue = 5

p.independent = ["Time", "k1"]
p.dependent = "S1"

p.xlabel = "Time"
p.ylabel = r"$k_{1}$"
p.zlabel = r"$S_{1}$"

p.plotSurface()
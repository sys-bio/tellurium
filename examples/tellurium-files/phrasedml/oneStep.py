# -*- coding: utf-8 -*-
"""
phrasedml one step test
"""
from __future__ import print_function
import tellurium as te
import os

antimonyStr = '''
// Created by libAntimony v2.9
model *oneStep()

// Compartments and Species:
compartment compartment_;
species S1 in compartment_, S2 in compartment_, $X0 in compartment_, $X1 in compartment_;
species $X2 in compartment_;

// Reactions:
J0: $X0 => S1; J0_v0;
J1: S1 => $X1; J1_k3*S1;
J2: S1 => S2; (J2_k1*S1 - J2_k_1*S2)*(1 + J2_c*S2^J2_q);
J3: S2 => $X2; J3_k2*S2;

// Species initializations:
S1 = 0;
S2 = 1;
X0 = 1;
X1 = 0;
X2 = 0;

// Compartment initializations:
compartment_ = 1;

// Variable initializations:
J0_v0 = 8;
J1_k3 = 0;
J2_k1 = 1;
J2_k_1 = 0;
J2_c = 1;
J2_q = 3;
J3_k2 = 5;

// Other declarations:
const compartment_, J0_v0, J1_k3, J2_k1, J2_k_1, J2_c, J2_q, J3_k2;
end
'''

phrasedmlStr = '''
model1 = model "oneStep"
stepper = simulate onestep(0.1)
task0 = run stepper on model1
task1 = repeat task0 for local.x in uniform(0, 10, 100), J0_v0 = piecewise(8, x<4, 0.1, 4<=x<6, 8)
plot "One Step Simulation" task1.time vs task1.S1, task1.S2, task1.J0_v0
report task1.time vs task1.S1, task1.S2, task1.J0_v0
'''

# phrasedml experiment
exp = te.experiment(antimonyStr, phrasedmlStr)

# write python code
realPath = os.path.realpath(__file__)
workingDir = os.path.dirname(realPath)
with open(realPath + 'code.py', 'w') as f:
    f.write(exp._toPython(phrasedmlStr, workingDir=workingDir))

# execute python
exp.execute(phrasedmlStr, workingDir=workingDir)

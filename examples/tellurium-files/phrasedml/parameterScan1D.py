# -*- coding: utf-8 -*-
"""
phrasedml 1D parameter scan
see https://github.com/sys-bio/tellurium/issues/99

UserWarning: Unsupported listOfChanges on RepeatedTask
"""
from __future__ import print_function
import tellurium as te
import phrasedml.phrasedml as phrasedml

antimonyStr = '''
// Created by libAntimony v2.9
model *oscli()

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
model1 = model "oscli"
timecourse1 = simulate uniform(0, 20, 1000)
task0 = run timecourse1 on model1
task1 = repeat task0 for J0_v0 in [8, 4, 0.4], reset=true
plot task1.time vs task1.S1, task1.S2
'''

r = te.loada(antimonyStr)
sbml = r.getSBML()

phrasedml.setReferencedSBML("oscli", sbml)
sedml = phrasedml.convertString(phrasedmlStr)

# phrasedml experiment
exp = te.experiment(antimonyStr, phrasedmlStr)
exp.execute()


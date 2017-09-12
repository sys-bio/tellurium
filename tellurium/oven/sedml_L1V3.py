"""
Tellurium test case for SED-ML conversion.
"""

import roadrunner


'''
import tellurium as te
from tellurium.sedml.tephrasedml import experiment


""" Minimal example which should work. """
antimonyStr = """
model test
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""
phrasedmlStr = """
    model0 = model "test"
    sim0 = simulate uniform(0, 10, 100)
    task0 = run sim0 on model0
    plot task0.time vs task0.S1
"""
exp = experiment(antimonyStr, phrasedmlStr)
exp.execute(phrasedmlStr)
'''
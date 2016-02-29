"""
Minimal experiment
Gillespie simulation / stochastic.
"""
from __future__ import print_function
import tellurium as te

antimonyStr = """
model test
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""

phrasedmlStr = """
    model0 = model "test"
    sim0 = simulate uniform_stochastic(0, 10, 100)
    task0 = run sim0 on model0
    plot task0.time vs task0.S1
"""

exp = te.experiment(antimonyStr, phrasedmlStr)
exp.execute(phrasedmlStr)

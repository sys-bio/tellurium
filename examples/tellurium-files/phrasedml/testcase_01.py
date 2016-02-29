"""
Minimal experiment
CVODE uniformTime course on model
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
    sim0 = simulate uniform(0, 10, 100)
    task0 = run sim0 on model0
    plot task0.time vs task0.S1
"""

exp = te.experiment(antimonyStr, phrasedmlStr)
print('*'*80)
exp.printPython()
print('*'*80)


# import tempfile
# tempdir = tempfile.mkdtemp(suffix="_sedml")
import os
exp.execute(phrasedmlStr, workingDir=os.getcwd())

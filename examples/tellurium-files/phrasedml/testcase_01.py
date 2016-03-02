"""
Minimal experiment
CVODE uniformTime course on model
"""
from __future__ import print_function
import tellurium as te

antimonyStr = """
model testcase_01
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""

phrasedmlStr = """
    model0 = model "testcase_01"
    sim0 = simulate uniform(0, 10, 100)
    task0 = run sim0 on model0
    plot "UniformTimecourse" task0.time vs task0.S1
"""

# phrasedml experiment
exp = te.experiment(antimonyStr, phrasedmlStr)

# python code
import os
with open(os.path.realpath(__file__) + 'code.py', 'w') as f:
    f.write(exp._toPython(phrasedmlStr))

# execute python
import os
exp.execute(phrasedmlStr, workingDir=os.getcwd())

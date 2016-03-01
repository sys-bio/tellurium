"""
Repeated simulation

"""

from __future__ import print_function
import tellurium as te

antimonyStr = """
model testcase_02
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""

phrasedmlStr = """
    model0 = model "testcase_02"
    model1 = model "testcase_02" with S1=5.0
    sim0 = simulate uniform(0, 10, 100)
    task0 = run sim0 on model1
    task1 = repeat task0 for k1 in uniform(0.0, 5.0, 5), reset = true
    plot task1.time vs task1.S1, task1.S2
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

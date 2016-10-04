"""
Repeated simulation.

Perform repeated simulation after change of initial concentration to model.
Within every repeat the value of a parameter k1 is changed.
The model is reset after every repeat.
"""

from __future__ import print_function
import tellurium as te
import os

antimonyStr = """
model case_02
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""

phrasedmlStr = """
    model0 = model "case_02"
    model1 = model model0 with S1=5.0
    sim0 = simulate uniform(0, 6, 100)
    task0 = run sim0 on model1
    task1 = repeat task0 for k1 in uniform(0.0, 5.0, 5), reset = true
    plot "Repeated task with reset" task1.time vs task1.S1, task1.S2
    report task1.time vs task1.S1, task1.S2
    plot "Repeated task varying k1" task1.k1 vs task1.S1
    report task1.k1 vs task1.S1
"""

# phrasedml experiment
exp = te.experiment(antimonyStr, phrasedmlStr)

# write python code
realPath = os.path.realpath(__file__)
workingDir = os.path.dirname(realPath)
with open(realPath + 'code.py', 'w') as f:
    f.write(exp._toPython(phrasedmlStr, workingDir=workingDir))

# execute python
exp.execute(phrasedmlStr, workingDir=workingDir)

# remove sedx (not hashable due to timestamp)
os.remove(os.path.join(workingDir, 'case_02.sedx'))

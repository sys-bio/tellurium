"""
Model changes via formulas.

Use ComputeChanges on models setting initial conditions based on model variables.
"""

from __future__ import print_function
import tellurium as te
import os

antimonyStr = '''
model case_03()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''

phrasedmlStr = '''
  mod1 = model "case_03"
  mod2 = model mod1 with S2=S1+4
  sim1 = simulate uniform(0, 10, 100)
  task1 = run sim1 on mod1
  task2 = run sim1 on mod2
  plot "ComputeChanges" task1.time vs task1.S1, task1.S2, task2.S1, task2.S2
  report task1.time vs task1.S1, task1.S2, task2.S1, task2.S2
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
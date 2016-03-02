"""
Coupled ranges
"""
from __future__ import print_function
import tellurium as te

antimonyStr = '''
model testcase_06()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''

phrasedmlStr = '''
  mod1 = model "testcase_06"
  sim1 = simulate uniform(0, 10, 100)
  task1 = run sim1 on mod1
  repeat1 = repeat task1 for S1 in [1, 3, 5], S2 in uniform(0, 10, 2)
  plot "Example plot" repeat1.time vs repeat1.S1, repeat1.S2
'''

# phrasedml experiment
exp = te.experiment(antimonyStr, phrasedmlStr)

# python code
import os
with open(os.path.realpath(__file__) + 'code.py', 'w') as f:
    f.write(exp._toPython(phrasedmlStr))

# execute python
import os
exp.execute(phrasedmlStr, workingDir=os.getcwd())

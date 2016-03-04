"""
Set values in repeated Task & multiple tasks via same range
Multiple subtasks which have to be joined.
"""
from __future__ import print_function
import tellurium as te

antimonyStr = '''
model testcase_08()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''

phrasedmlStr = '''
  mod1 = model "testcase_08"
  mod2 = model "testcase_08"
  sim1 = simulate uniform(0, 10, 20)
  sim2 = simulate uniform(0, 3, 10)
  task1 = run sim1 on mod1
  task2 = run sim2 on mod1
  repeat1 = repeat [task1, task2] for S2 in uniform(0, 10, 9), mod1.S1 = S2+3, reset=False
  plot "Repeated Multiple Subtasks" repeat1.mod1.time vs repeat1.mod1.S1, repeat1.mod1.S2
  # plot "Repeated Multiple Subtasks" repeat1.mod2.time vs repeat1.mod2.S1, repeat1.mod2.S2
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

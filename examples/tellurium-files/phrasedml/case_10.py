"""
Set values in repeated Task & multiple tasks via same range
"""
import os
from tellurium.sedml.utils import run_case

a_str = '''
model case_10()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''

p_str = '''
  mod1 = model "case_10"
  mod2 = model "case_10"
  sim1 = simulate uniform(0, 10, 100)
  sim2 = simulate uniform(0, 3, 10)
  task1 = run sim1 on mod1
  task2 = run sim2 on mod2
  repeat1 = repeat [task1, task2] for local.X in uniform(0, 10, 9), mod1.S1 = X, mod2.S1 = X+3
  plot repeat1.mod1.time vs repeat1.mod1.S1, repeat1.mod1.S2, repeat1.mod2.time vs repeat1.mod2.S1, repeat1.mod2.S2
'''

run_case(os.path.realpath(__file__), a_str, p_str)

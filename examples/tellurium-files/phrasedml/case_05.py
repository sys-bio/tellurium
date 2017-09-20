"""
DataGenerator via formula
"""
import os
from tellurium.sedml.utils import run_case

a_str = '''
model case_05()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''
p_str = '''
  mod1 = model "case_05"
  sim1 = simulate uniform(0, 10, 100)
  task1 = run sim1 on mod1
  plot "Example plot" task1.time vs task1.S1, task1.S2, task1.S1/task1.S2
  report task1.time vs task1.S1, task1.S2, task1.S1/task1.S2
  plot "Normalized plot" task1.S1/max(task1.S1) vs task1.S2/max(task1.S2)
  report task1.S1/max(task1.S1) vs task1.S2/max(task1.S2)
'''

run_case(os.path.realpath(__file__), a_str, p_str)

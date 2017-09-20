"""
Simple report & report of repeated tasks.
"""
import os
from tellurium.sedml.utils import run_case

a_str = '''
model case_07()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''
p_str = '''
  mod1 = model "case_07"
  sim1 = simulate uniform(0, 10, 100)
  task1 = run sim1 on mod1
  repeat1 = repeat task1 for S1 in [1, 3, 5], reset=True
  report task1.time, task1.S1, task1.S2, task1.S1/task1.S2
  report repeat1.time, repeat1.S1, repeat1.S2, repeat1.S1/repeat1.S2
'''

run_case(os.path.realpath(__file__), a_str, p_str)

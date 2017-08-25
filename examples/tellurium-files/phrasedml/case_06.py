"""
Coupled ranges.
Two ranges with one of the ranges being master range, the other following in lock.
"""
from __future__ import print_function
import os
from tellurium.sedml.case_template import run_case

antimonyStr = '''
model case_06()
  J0: S1 -> S2; k1*S1-k2*S2
  S1 = 10.0; S2 = 0.0;
  k1 = 0.5; k2=0.4
end
'''

phrasedmlStr = '''
  mod1 = model "case_06"
  sim1 = simulate uniform(0, 10, 100)
  task1 = run sim1 on mod1
  repeat1 = repeat task1 for S1 in [1, 3, 5], S2 in uniform(0, 10, 2), reset=True
  repeat2 = repeat task1 for S1 in [1, 3, 5], S2 in uniform(0, 10, 2), reset=False
  plot "Example plot" repeat1.time vs repeat1.S1, repeat1.S2
  report repeat1.time vs repeat1.S1, repeat1.S2
  plot "Example plot" repeat2.time vs repeat2.S1, repeat2.S2
  report repeat2.time vs repeat2.S1, repeat2.S2
'''

run_case(os.path.realpath(__file__), antimonyStr, phrasedmlStr)

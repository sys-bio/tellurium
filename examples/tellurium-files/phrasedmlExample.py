# -*- coding: utf-8 -*-
"""
Testing phrasedml.
"""
from __future__ import print_function
import tellurium as te

ant = '''
model myModel
  S1 -> S2; k1*S1
  S1 = 10; S2 = 0
  k1 = 1
end
'''

phrasedml = '''
  model1 = model "myModel"
  sim1 = simulate uniform(0, 5, 100)
  task1 = run sim1 on model1
  plot "Figure 1" time vs S1, S2
'''

# create experiment
exp = te.experiment(ant, phrasedml)
exp.execute()
exp.printPython()



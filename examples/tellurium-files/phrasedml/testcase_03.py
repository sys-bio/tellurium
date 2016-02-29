from __future__ import print_function
import tellurium as te

antimonyStr = '''
model test()
  J0: -> S1; 0.3
  S1 = 0
end
'''

phrasedmlStr = '''
  mod1 = model "test"
  sim1 = simulate uniform(0,10,100)
  task1 = run sim1 on mod1
  plot "Example plot" time vs S1
'''

exp = te.experiment(antimonyStr, phrasedmlStr)
exp.execute()

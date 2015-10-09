antimony = '''
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

import tellurium as te

exp = te.experiment(antimony, phrasedml)

exp.execute()
exp.printpython()

### export testing - put the full path of zip file you want to create
#exp.exportAsCombine() 


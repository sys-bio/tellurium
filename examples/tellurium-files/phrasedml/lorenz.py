'''
Lorenz attractor

This is a sample file that demonstrates the use of 
Antimony and phraSEDML to simulate Lorenz attractor.
This script requires Tellurium (http://tellurium.analogmachine.org/) to run.
'''

import tellurium as te

antimonyStr = '''
model lorenz
  x' = sigma*(y - x);
  y' = x*(rho - z) - y;
  z' = x*y - beta*z;
  x = 0.96259;  y = 2.07272;  z = 18.65888;
  sigma = 10;  rho = 28; beta = 2.67;
end
'''

phrasedmlStr = '''
model1 = model "lorenz"
sim1 = simulate uniform(0,15,2000)
task1 = run sim1 on model1
plot task1.z vs task1.x
'''

exp = te.experiment(antimonyStr, phrasedmlStr)
exp.execute(phrasedmlStr)

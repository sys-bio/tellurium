"""
Lorenz attractor.

This is a sample file that demonstrates the use of 
Antimony and phraSEDML to simulate Lorenz attractor.
"""
from __future__ import print_function
import os
from tellurium.sedml.case_template import run_case

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

run_case(os.path.realpath(__file__), antimonyStr, phrasedmlStr)

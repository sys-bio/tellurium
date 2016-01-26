
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!


# ### Non-unit stoichiometries
# The following example demonstrates how to create a model with non-unit stoichiometries.

# In[2]:

from __future__ import print_function
import tellurium as te

r = te.loada('''
  model pathway()
    S1 + S2 -> 2 S3; k1*S1*S2
    3 S3 -> 4 S4 + 6 S5; k2*S3^3
    k1 = 0.1;k2 = 0.1;
  end
''')
print(r.getAntimony())


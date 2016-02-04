
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# ### phrasedml experiment
# Tellurium provides support for simulation descriptions in SED-ML the export in Combine Archive format.

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

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

# create an experiment and perform it
exp = te.experiment(antimony, phrasedml)

exp.execute()
exp.printpython()


# ### Combine Archive
# The experiment, i.e. model with the simulation description, can be stored as Combine Archive.

# In[2]:

# create Combine Archive
import tempfile
f = tempfile.NamedTemporaryFile()
exp.exportAsCombine(f.name)

# print the content of the Combine Archive
import zipfile
zip=zipfile.ZipFile(f.name)
print(zip.namelist())


# In[3]:




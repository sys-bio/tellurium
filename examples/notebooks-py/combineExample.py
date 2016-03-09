
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# ### Combine archives
# The experiment, i.e. model with the simulation description, can be stored as Combine Archive.

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

antimonyStr = """
model test()
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""

phrasedmlStr = """
    model0 = model "test"
    sim0 = simulate uniform(0, 6, 100)
    task0 = run sim0 on model0
    plot "Timecourse test model" task0.time vs task0.S1
"""

# phrasedml experiment
exp = te.experiment(antimonyStr, phrasedmlStr)
exp.execute(phrasedmlStr)

# create Combine Archive
import tempfile
f = tempfile.NamedTemporaryFile()
exp.exportAsCombine(f.name)

# print the content of the Combine Archive
import zipfile
zip=zipfile.ZipFile(f.name)
print(zip.namelist())


# ### Create combine archive
# TODO

# In[2]:

import tellurium as te
import phrasedml

antTest1Str = """
model test1()
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""

antTest2Str = """
model test2()
    v0: X1 -> X2; p1*X1;
    X1 = 5.0; X2 = 20.0;
    k1 = 0.2;
end
"""

phrasedmlStr = """
    model1 = model "test1"
    model2 = model "test2"
    model3 = model model1 with S1=S2+20
    sim1 = simulate uniform(0, 6, 100)
    task1 = run sim1 on model1
    task2 = run sim1 on model2
    plot "Timecourse test1" task1.time vs task1.S1, task1.S2
    plot "Timecourse test2" task2.time vs task2.X1, task2.X2
"""

# phrasedml.setReferencedSBML("test1")
exp = te.experiment(phrasedmlList=[phrasedmlStr], antimonyList=[antTest1Str])
print(exp)

# set first model
phrasedml.setReferencedSBML("test1", te.antimonyToSBML(antTest1Str))
phrasedml.setReferencedSBML("test2", te.antimonyToSBML(antTest2Str))

sedmlstr = phrasedml.convertString(phrasedmlStr)
if sedmlstr is None:
    raise Exception(phrasedml.getLastError())
print(sedmlstr)


# In[3]:




# In[3]:




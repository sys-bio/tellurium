
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# #### SBML

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te
import tempfile

# load model
r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
# file for export
f_sbml = tempfile.NamedTemporaryFile(suffix=".xml")

# export current model state
r.exportToSBML(f_sbml.name)

# to export the initial state when the model was loaded
# set the current argument to False
r.exportToSBML(f_sbml.name, current=False)

# The string representations of the current model are available via
str_sbml = r.getCurrentSBML()

# and of the initial state when the model was loaded via
str_sbml = r.getSBML()
print(str_sbml)


# #### Antimony

# In[2]:

import tellurium as te
import tempfile

# load model
r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
# file for export
f_antimony = tempfile.NamedTemporaryFile(suffix=".txt")

# export current model state
r.exportToAntimony(f_antimony.name)

# to export the initial state when the model was loaded
# set the current argument to False
r.exportToAntimony(f_antimony.name, current=False)

# The string representations of the current model are available via
str_antimony = r.getCurrentAntimony()

# and of the initial state when the model was loaded via
str_antimony = r.getAntimony()
print(str_antimony)


# #### CellML

# In[3]:

import tellurium as te
import tempfile

# load model
r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
# file for export
f_cellml = tempfile.NamedTemporaryFile(suffix=".cellml")

# export current model state
r.exportToCellML(f_cellml.name)

# to export the initial state when the model was loaded
# set the current argument to False
r.exportToCellML(f_cellml.name, current=False)

# The string representations of the current model are available via
str_cellml = r.getCurrentCellML()

# and of the initial state when the model was loaded via
str_cellml = r.getCellML()
print(str_cellml)


# #### Matlab

# In[4]:

import tellurium as te
import tempfile

# load model
r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
# file for export
f_matlab = tempfile.NamedTemporaryFile(suffix=".m")

# export current model state
r.exportToMatlab(f_matlab.name)

# to export the initial state when the model was loaded
# set the current argument to False
r.exportToMatlab(f_matlab.name, current=False)

# The string representations of the current model are available via
str_matlab = r.getCurrentMatlab()

# and of the initial state when the model was loaded via
str_matlab = r.getMatlab()
print(str_matlab)


# In[5]:

import antimony
antimony.loadAntimonyString('''S1 -> S2; k1*S1; k1 = 0.1; S1 = 10''')
ant_str = antimony.getCellMLString(antimony.getMainModuleName())
print(ant_str)


# In[6]:




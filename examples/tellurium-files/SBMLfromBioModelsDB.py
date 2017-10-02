# -*- coding: utf-8 -*-
"""
Load model from biomodels.
"""
from __future__ import print_function, division
import tellurium as te

r = te.loadSBMLModel("http://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000010")
result = r.simulate(0, 3000, 5000)
r.plot(result)

# -*- coding: utf-8 -*-
"""
Load model from biomodels.
"""
from __future__ import print_function, division
import tellurium as te

r = te.loadSBMLModel("https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000010.2?filename=BIOMD0000000010_url.xml")
result = r.simulate(0, 3000, 5000)
r.plot(result)

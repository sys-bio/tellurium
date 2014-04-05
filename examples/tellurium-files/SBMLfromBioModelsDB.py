# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 18:17:27 2014

@author: mgaldzic
"""
import tellurium as te

r = te.loadSBMLModel("http://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000010")
result = r.simulate(0, 3000, 5000)
te.plotWithLegend (r, result)
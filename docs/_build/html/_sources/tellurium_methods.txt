===================
Tellurium Methods
===================

----------------
Utility Methods
----------------
The most useful methods here are the notices routines. Roadrunner will offen issue warning or informational messages. For repeated simulation such messages will clutter up the outputs. noticesOff and noticesOn can be used to turn on an off the messages.

.. autofunction:: tellurium.getVersionInfo
.. autofunction:: tellurium.printVersionInfo
.. autofunction:: tellurium.getTelluriumVersion
.. autofunction:: tellurium.noticesOff
.. autofunction:: tellurium.noticesOn
.. autofunction:: tellurium.saveToFile
.. autofunction:: tellurium.readFromFile

.. include:: _notebooks/core/tellurium_utility.rst

-------------------------
Model Loading 
-------------------------
There are a variety of methods to load models into libRoadrunner. 

.. autofunction:: tellurium.loada
.. autofunction:: tellurium.loadAntimonyModel
.. autofunction:: tellurium.loadSBMLModel
.. autofunction:: tellurium.loadCellMLModel

.. include:: _notebooks/core/tellurium_model_loading.rst

----------------------------------------
Interconversion Utilities
----------------------------------------
Use these routines interconvert verious standard formats

.. autofunction:: tellurium.antimonyToSBML
.. autofunction:: tellurium.antimonyToCellML
.. autofunction:: tellurium.sbmlToAntimony
.. autofunction:: tellurium.sbmlToCellML
.. autofunction:: tellurium.cellmlToAntimony
.. autofunction:: tellurium.cellmlToSBML

.. include:: _notebooks/core/tellurium_interconversion.rst

----------------------------------------
Export Utilities
----------------------------------------
Use these routines to convert the current model state into other formats, like
Matlab, CellML, Antimony and SBML.

.. autoclass:: tellurium.ExtendedRoadRunner
   :members: exportToSBML, exportToAntimony, exportToCellML, exportToMatlab, getAntimony, getCurrentAntimony, getCellML, getCurrentCellML, getMatlab, getCurrentMatlab

::

	r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	print(r.getCurrentMatlab())
	r.exportToMatlab("mymodel.m")


----------------------------------------
Stochastic Simulation
----------------------------------------
Use these routines to carry out Gillespie style stochastic simulations.

.. autoclass:: tellurium.ExtendedRoadRunner
   :members: getSeed, setSeed, gillespie

**Stochastic simulation**::

	r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 40')
	r.setSeed(87675)
	result = r.gillespie (0, 100)
	r.plot(result)

**Run two simulations and combine the two**::

	import numpy as np
	import tellurium as te

	r = te.loadSBMLModel ('mymodel.xml')
	seed= r.getSeed()
	result1 = r.gillespie (0, 100)
	r.model.k1 = r.model.k1*20
	result2 = r.gillespie (100, 200)
	# Merge the two runs together
	rr.plot(np.vstack ((result1, result))

----------------------------------------
Math
----------------------------------------
Only one routine is currently available in this group which is a routine to compute the eigenvalues of given a matrix.

.. autofunction:: tellurium.getEigenvalues

----------------------------------------
Plotting
----------------------------------------
Two useful plotting routines. They assume that the first column in the array is the x-axis and the second and subsequent columns represent curves on the y-axis.

.. autofunction:: tellurium.plotArray
.. autoclass:: tellurium.ExtendedRoadRunner
   :members: plot, plotWithLegend, simulateAndPlot

::

	# Load a model and carry out a simulation generating 100 points
	r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	result = r.simulate (0, 10, 100)

	# No legend will be add to the plot, useful for plotting large 
	# numbers of curves where a legend would get in the way
	te.plotArray (result)

	# To get a legend use the roadrunner plot command
	r.plot (result)

----------------------------------------
Model Reset
----------------------------------------
Use these routines reset your model back to particular states

.. autoclass:: tellurium.ExtendedRoadRunner
   :members: resetToOrigin, resetAll

::

	r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	result = r.simulate (0, 10, 100)
	p.model.S1 = 2.0
	result = r.simulate (0, 10, 100)
	# Reset the model back to its original state
	r.reset()

If you wish to reset a model back to the state it was what it was loaded, use the resetToOrigin method
::

	r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	result = r.simulate (0, 10, 100)
	# Make lots of different kinds of changes to the model
	# Reset the model back to the state it had when it was created
	r.resetToOrigin()

----------------------------------------
jarnac Short-cuts
----------------------------------------
Routines to support the Jarnac compatibility layer

.. autoclass:: tellurium.ExtendedRoadRunner
   :members: fjac, sm, rs, fs, bs, ps, vs, dv, rv, sv

----------------------------------------
Test Models
----------------------------------------
RoadRunner has built into it a number of predefined models that can be use
to easily try and test tellurium.

.. autofunction:: tellurium.loadTestModel
.. autofunction:: tellurium.getTestModel
.. autofunction:: tellurium.listTestModels

::

	# To get the number of builtin models use listTestModels
	print(roadrunner.listTestModels())
	['feedback.xml', 'test_1.xml']

To load one of the test models use loadTestModel:
::

	r = roadrunner.loadTestModel ('feedback.xml')
	result = r.simulate (0, 10, 100)
	r.plot (result)

If you need to obtain the SBML for the test model, use getTestModel
::

	sbmlStr = roadrunner.getTestModel()
	saveToFile('model.xml', sbmlStr)

To look at one of the test model in Antimony form:
::

	antstr = te.sbmlToAntimony (roadrunner.getTestModel ('feedback.xml'))
	print(antStr)

----------------------------------------
Model Methods
----------------------------------------
Routines flattened from model, aves typing and easier for finding the methods

.. autoclass:: tellurium.ExtendedRoadRunner
   :members: getRatesOfChange, getBoundarySpeciesConcentrations, getBoundarySpeciesIds, getNumBoundarySpecies, getFloatingSpeciesConcentrations, getFloatingSpeciesIds, getNumFloatingSpecies, getGlobalParameterIds, getGlobalParameterValues, getNumGlobalParameters, getCompartmentIds, getCompartmentVolumes, getNumCompartments, getConservedMoietyValues, getNumConservedMoieties, getNumDepFloatingSpecies, getNumIndFloatingSpecies, getNumReactions, getReactionIds, getReactionRates, getNumEvents, setStartTime, setEndTime, getStartTime, getEndTime, getNumberOfPoints, setNumberOfPoints, getNumRateRules


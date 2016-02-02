===================
Tellurium Methods
===================

----------------
Utility Methods
----------------
The most useful methods here are the notices routines. Roadrunner will offen issue warning or informational messages. For repeated simulation such messages will clutter up the outputs. noticesOff and noticesOn can be used to turn on an off the messages.

**Print Version information**
:: 

	import tellurium as te
	te.getVersionInfo()

**Repeat simulation without notification**
::

	# Load SBML file
	r = roadrunner.RoadRunner('mymodel.xml')
	# Turn of notices so they don't clutter the output
	roadrunner.noticesOff()
	for i in range (0:20):
	  result = r.simulate (0, 10)
	  r.plot (result)
	  r.model.k1 = r.model.k1 + 0.2
	# Turn the notices back on
	roadrunner.noticesOn()

**File helpers for reading and writing**
::

	r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	saveToFile('mymodel.m', r.getMatlab())

	sbmlstr = readFromFile('mymodel.xml')

.. autofunction:: tellurium.getVersionInfo
.. autofunction:: tellurium.printVersionInfo
.. autofunction:: tellurium.getTelluriumVersion
.. autofunction:: tellurium.noticesOff
.. autofunction:: tellurium.noticesOn
.. autofunction:: tellurium.saveToFile
.. autofunction:: tellurium.readFromFile

-------------------------
Model Loading 
-------------------------
There are a variety of methods to load models into libRoadrunner. At the most basic level one can load the model directly using libRoadRunner:
::

	r = roadrunner.RoadRunner('mymodel.xml')

Alternatively one can use these methods:

This is the same as roadrunner.RoadRunner() but the method name is more suggestive of what it does. Like RoadRunner, loadSBML can accept a file name or a SBML string as it argument
::

	r = te.loadSBMLModel ('mymodel.xml')

	# To load an Antimony model use:
	r = te.loadAntimonyModel (antStr)

	# Or alternatively
	r = te.loadAntimonyModel ('mymodel.ant')

	# The method loada is simply a shortcut to loadAntimonyModel
	r = loada('''
		S1 -> S2; k1*S1;
		S2 -> S3; k2*S2;
	   
		k1= 0.1; k2 = 0.2; 
		S1 = 10; S2 = 0; S3 = 0;
		''')
		result = r.simulate (0, 10, 100)
		r.plot (result)

.. autofunction:: tellurium.loada
.. autofunction:: tellurium.loadAntimonyModel
.. autofunction:: tellurium.loadSBMLModel
.. autofunction:: tellurium.loadCellMLModel

----------------------------------------
Interconversion Utilities
----------------------------------------
Use these routines interconvert verious standard formats

**Convert an SBML model into Antimony**
::

	# Load an SBML file
	sbmlStr = te.readFromFile('mymodel.xml')
	# Generate the Antimony format of the SBML model
	print(te.sbmlToAntimony(sbmlStr))

**Convert an Antimony model into SBML**
::

	# Load an Antimony file
	antStr = te.readFromFile('mymodel.ant')
	# Generate the SBML format of the Antimony model
	print te.antimonyToSBML(antStr)

.. autofunction:: tellurium.antimonyToSBML
.. autofunction:: tellurium.antimonyToCellML
.. autofunction:: tellurium.sbmlToAntimony
.. autofunction:: tellurium.sbmlToCellML
.. autofunction:: tellurium.cellmlToAntimony
.. autofunction:: tellurium.cellmlToSBML

----------------------------------------
Stochastic Simulation
----------------------------------------
Use these routines to carry out Gillespie style stochastic simulations.

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


.. autofunction:: tellurium.getSeed
.. autofunction:: tellurium.setSeed
.. autofunction:: tellurium.gillespie

----------------------------------------
SEDML
----------------------------------------
.. autofunction:: tellurium.experiment

----------------------------------------
Math
----------------------------------------
Only one routine is currently available in this group which is a routine to compute the eigenvalues of given a matrix.
::

	import numpy as np
	import tellurium as te

	m = np.matrix([[1,2],[5,7]])
	print(te.getEigenvalues(m))

.. autofunction:: tellurium.getEigenvalues

----------------------------------------
Plotting
----------------------------------------
Two useful plotting routines. They assume that the first column in the array is the x-axis and the second and subsequent columns represent curves on the y-axis.
::

	# Load a model and carry out a simulation generating 100 points
	r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	result = r.simulate (0, 10, 100)

	# No legend will be add to the plot, useful for plotting large 
	# numbers of curves where a legend would get in the way
	te.plotArray (result)

	# To get a legend use the roadrunner plot command
	r.plot (result)

.. autofunction:: tellurium.plotWithLegend
.. autofunction:: tellurium.simulateAndPlot
.. autofunction:: tellurium.plotArray
.. autofunction:: tellurium.plot

----------------------------------------
Model Reset
----------------------------------------
Use these routines reset your model back to particular states
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

.. autofunction:: tellurium.resetToOrigin
.. autofunction:: tellurium.resetAll

----------------------------------------
Export
----------------------------------------
**Matlab export utilities**

Use these routines to convert your model into a Matlab function.
::

	r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	print(r.getMatlab())
	r.exportToMatlab("mymodel.m")

.. autofunction:: tellurium.getMatlab
.. autofunction:: tellurium.exportToMatlab
.. autofunction:: tellurium.getAntimony

----------------------------------------
jarnac Short-cuts
----------------------------------------
Routines to support the Jarnac compatibility layer

.. autofunction:: tellurium.getSm
.. autofunction:: tellurium.getRs
.. autofunction:: tellurium.getFs
.. autofunction:: tellurium.getBs
.. autofunction:: tellurium.getPs
.. autofunction:: tellurium.getVs
.. autofunction:: tellurium.getDv
.. autofunction:: tellurium.getRv
.. autofunction:: tellurium.getSv
.. autofunction:: tellurium.getfJac

----------------------------------------
Test Models
----------------------------------------
**Methods to acess the builtin test models.**

RoadRunner has built into it a number of predefined models that can be use
to easily try out roadrunner if so exmaple you don't have a model at hand.
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

.. autofunction:: tellurium.loadTestModel
.. autofunction:: tellurium.getTestModel

----------------------------------------
Model Methods
----------------------------------------
Routines flattened from model, aves typing and easier for finding the methods

.. autofunction:: tellurium.tellurium.getRatesOfChange
.. autofunction:: tellurium.getBoundarySpeciesConcentrations
.. autofunction:: tellurium.getBoundarySpeciesIds
.. autofunction:: tellurium.getNumBoundarySpecies
.. autofunction:: tellurium.getFloatingSpeciesConcentrations
.. autofunction:: tellurium.getFloatingSpeciesIds
.. autofunction:: tellurium.getNumFloatingSpecies
.. autofunction:: tellurium.getGlobalParameterIds
.. autofunction:: tellurium.getGlobalParameterValues
.. autofunction:: tellurium.getNumGlobalParameters
.. autofunction:: tellurium.getCompartmentIds
.. autofunction:: tellurium.getCompartmentVolumes
.. autofunction:: tellurium.getNumCompartments
.. autofunction:: tellurium.getConservedMoietyValues
.. autofunction:: tellurium.getNumConservedMoieties
.. autofunction:: tellurium.getNumDepFloatingSpecies
.. autofunction:: tellurium.getNumIndFloatingSpecies
.. autofunction:: tellurium.getNumReactions
.. autofunction:: tellurium.getReactionIds
.. autofunction:: tellurium.getReactionRates
.. autofunction:: tellurium.getNumEvents
.. autofunction:: tellurium.setStartTime
.. autofunction:: tellurium.setEndTime
.. autofunction:: tellurium.getStartTime
.. autofunction:: tellurium.getEndTime
.. autofunction:: tellurium.getNumberOfPoints
.. autofunction:: tellurium.setNumberOfPoints
.. autofunction:: tellurium.getNumRateRules


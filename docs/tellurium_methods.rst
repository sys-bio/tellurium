===================
Tellurium Methods
===================

-------------------
Installing Packages
-------------------

Tellurium provides utility methods for installing Python packages from `PyPI <https://pypi.python.org/pypi>`_. These methods simply delegate to ``pip``, and are usually
more reliable than running ``!pip install xyz``.

.. autofunction:: tellurium.installPackage
.. autofunction:: tellurium.upgradePackage
.. autofunction:: tellurium.removePackage
.. autofunction:: tellurium.searchPackage

.. include:: _notebooks/core/methods_installing_packages.rst

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

.. autoclass:: tellurium.tellurium.ExtendedRoadRunner
   :members: exportToSBML, exportToAntimony, exportToCellML, exportToMatlab, getAntimony, getCurrentAntimony, getCellML, getCurrentCellML, getMatlab, getCurrentMatlab

.. include:: _notebooks/core/tellurium_export.rst

----------------------------------------
Stochastic Simulation
----------------------------------------

Use these routines to carry out Gillespie style stochastic simulations.

.. autoclass:: tellurium.tellurium.ExtendedRoadRunner
   :members: getSeed, setSeed, gillespie

.. include:: _notebooks/core/tellurium_stochastic.rst

----------------------------------------
Distributed Stochastic Simulation
----------------------------------------

Use these in order to run simulations in distributed environment. 

.. autoclass:: tellurium.StochasticSimulationModel
   :members: model, seed, variable_step_size, from_time, to_time, step_points, integrator

----------------------------------------
Distributed Stochastic Simulation Utility
----------------------------------------

Use these in order to run simulations in distributed environment. It uses the object defined with StochasticSimulationModel.

.. autofunction:: tellurium.distributed_stochastic_simulation


----------------------------------------
Plot Distributed Stochastic Simulation Results
----------------------------------------

To plot the results retrieved from distributed_stochastic_simulation.

.. autofunction:: tellurium.plot_stochastic_result

----------------------------------------
Distributed Parameter Scanning
----------------------------------------

Parameter Scanning one/more models in a distributed environment

.. autofunction:: tellurium.distributed_parameter_scanning

----------------------------------------
Plotting Image of Parameter Scan 
----------------------------------------

Helps in plotting the results parameter Scanning of one/more models run in a distributed environment

.. autofunction:: tellurium.plotImage


----------------------------------------
Distributed Sensitivity Analysis
----------------------------------------

Use these in order to run Sensitivity Analysis in distributed environment. 

.. autoclass:: tellurium.SensitivityAnalysis
   :members: model, sbml, conservedMoietyAnalysis, filename, bounds, allowLog


----------------------------------------
Distributed Sensitivity Analysis Utility
----------------------------------------

Running the Sensitivity analysis using the model created using tellurium.SensitivityAnalysis

.. autofunction:: tellurium.distributed_sensitivity_analysis


----------------------------------------
Math
----------------------------------------

Only one routine is currently available in this group which is a routine to compute the eigenvalues of given a matrix.

.. autofunction:: tellurium.getEigenvalues

----------------------------------------
Plotting
----------------------------------------

Tellurium has a plotting engine which can target either Plotly (when used in a
notebook environment) or Matplotlib.

.. autofunction:: tellurium.plot

The function ``tellurium.plotArray`` assumes that the first column in the array is the x-axis and the second and subsequent columns represent curves on the y-axis.

.. autofunction:: tellurium.plotArray
.. autoclass:: tellurium.tellurium.ExtendedRoadRunner
   :members: draw, plot

.. include:: _notebooks/core/tellurium_plotting.rst

----------------------------------------
Model Reset
----------------------------------------

Use these routines reset your model back to particular states

.. autoclass:: tellurium.tellurium.ExtendedRoadRunner
   :members: resetToOrigin, resetAll

.. include:: _notebooks/core/tellurium_reset.rst

----------------------------------------
jarnac Short-cuts
----------------------------------------

Routines to support the Jarnac compatibility layer

.. autoclass:: tellurium.tellurium.ExtendedRoadRunner
   :members: fjac, sm, rs, fs, bs, ps, vs, dv, rv, sv

----------------------------------------
Test Models
----------------------------------------

RoadRunner has built into it a number of predefined models that can be use
to easily try and test tellurium.

.. autofunction:: tellurium.loadTestModel
.. autofunction:: tellurium.getTestModel
.. autofunction:: tellurium.listTestModels

.. include:: _notebooks/core/tellurium_test.rst

----------------------------------------
Model Methods
----------------------------------------
Routines flattened from model, aves typing and easier for finding the methods

.. autoclass:: tellurium.tellurium.ExtendedRoadRunner
   :members: getRatesOfChange, getBoundarySpeciesConcentrations, getBoundarySpeciesIds, getNumBoundarySpecies, getFloatingSpeciesConcentrations, getFloatingSpeciesIds, getNumFloatingSpecies, getGlobalParameterIds, getGlobalParameterValues, getNumGlobalParameters, getCompartmentIds, getCompartmentVolumes, getNumCompartments, getConservedMoietyValues, getNumConservedMoieties, getNumDepFloatingSpecies, getNumIndFloatingSpecies, getNumReactions, getReactionIds, getReactionRates, getNumEvents, setStartTime, setEndTime, getStartTime, getEndTime, getNumberOfPoints, setNumberOfPoints, getNumRateRules

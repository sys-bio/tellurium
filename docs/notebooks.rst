===================
Usage Examples
===================

All tellurium examples are available as interactive `Tellurium <http://tellurium.readthedocs.io/en/latest/installation.html#front-end-1-tellurium-notebook>`_ or `Jupyter <http://jupyter.readthedocs.org/en/latest/install.html>`_ notebooks.

To run the examples, clone the git repository:

.. code-block:: bash

    git clone https://github.com/sys-bio/tellurium.git

and use the `Tellurium notebook viewer <http://tellurium.readthedocs.io/en/latest/installation.html#front-end-1-tellurium-notebook>`_ or `Jupyter <http://jupyter.readthedocs.org/en/latest/install.html>`_ to open any notebook in the ``tellurium/examples/notebooks/core`` directory.

Tellurium Spyder comes with these examples under Tellurium Spyder installation directory. Look for folder called ``tellurium-winpython-examples``.

--------------------
Basics
--------------------

.. include:: _notebooks/core/roadrunnerBasics.rst

-------------------------
Models & Model Building
-------------------------

In this section, various types of models and different ways to building models are shown.

.. include:: _notebooks/core/model_modelFromBioModels.rst
.. include:: _notebooks/core/model_nonUnitStoichiometries.rst
.. include:: _notebooks/core/model_consecutiveUniUniReactions.rst
.. include:: _notebooks/core/model_generatingDifferentWaveforms.rst
.. include:: _notebooks/core/model_normalizedSpecies.rst

-------------------------------
Simulation and Analysis Methods
-------------------------------

In this section, different ways to simlate and analyse a model is shown.

.. include:: _notebooks/core/tellurium_stochastic.rst
.. include:: _notebooks/core/parameter_scan.rst
.. include:: _notebooks/core/plot2DParameterScan.rst

--------
SED-ML
--------

Tellurium exchangeability via the simulation experiment
description markup language `SED-ML <https://sed-ml.github.io/>`_ and `COMBINE archives <http://co.mbine.org/documents/archive>`_ (.omex files).
These formats are designed to allow modeling software to exchange models and
simulations. Whereas SBML encodes models, SED-ML encodes simulations, including
the solver (e.g. deterministic or stochastic), the type of simulation (timecourse or
steady state), and various parameters (start/end time, ODE solver tolerances, etc.).

.. include:: _notebooks/core/tesedmlExample.rst

---------------------
COMBINE & Inline OMEX
---------------------

COMBINE archives package related standards such as SBML models and SED-ML simulations
together so that they can be easily exchanged between software tools.
Tellurium provides the *inline OMEX* format
for editing the contents of COMBINE archives in a human-readable format.
You can use the function ``convertCombineArchive`` to convert a COMBINE archive
on disk to an inline OMEX string, and the function ``executeInlineOmex`` to execute
the inline OMEX string. Examples below.

.. autofunction:: tellurium.convertCombineArchive
.. autofunction:: tellurium.executeInlineOmex
.. autofunction:: tellurium.exportInlineOmex
.. autofunction:: tellurium.extractFileFromCombineArchive

.. include:: _notebooks/core/phrasedmlExample.rst

---------------------
Modeling Case Studies
---------------------

This series of case studies shows some slight more advanced
examples which correspond to common motifs in biological networks (negative feedback loops, etc.).
To draw the network diagrams seen here, you will need `graphviz <http://www.graphviz.org/>`_ installed.

.. include:: _notebooks/core/tellurium_examples.rst

-------------
Miscellaneous
-------------

.. include:: _notebooks/core/methods_installing_packages.rst

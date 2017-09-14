===================
Usage Examples
===================

All tellurium examples are available as interactive `Tellurium <http://tellurium.readthedocs.io/en/latest/installation.html#front-end-1-tellurium-notebook>`_ or `Jupyter <http://jupyter.readthedocs.org/en/latest/install.html>`_ notebooks.

To run the examples, clone the git repository:
.. code-block:: bash

    git clone https://github.com/sys-bio/tellurium.git

and use the `Tellurium notebook viewer <http://tellurium.readthedocs.io/en/latest/installation.html#front-end-1-tellurium-notebook>`_ or `Jupyter <http://jupyter.readthedocs.org/en/latest/install.html>`_ to open any notebook in the ``tellurium/examples/notebooks`` directory.

--------------------
Basics
--------------------

.. include:: _notebooks/core/roadrunnerBasics.rst

-------------------------
Models & Model Building
-------------------------

In this section model the creation of example models is shown.

.. include:: _notebooks/core/model_modelFromBioModels.rst
.. include:: _notebooks/core/model_nonUnitStoichiometries.rst
.. include:: _notebooks/core/model_consecutiveUniUniReactions.rst
.. include:: _notebooks/core/model_feedback_oscillations.rst
.. include:: _notebooks/core/model_generatingDifferentWaveforms.rst
.. include:: _notebooks/core/model_normalizedSpecies.rst

---------------------
COMBINE & Inline OMEX
---------------------

Tellurium exchangeability via the simulation experiment
description markup language `SED-ML <https://sed-ml.github.io/>`_ and `COMBINE archives <http://co.mbine.org/documents/archive>`_ (.omex files).
These formats are designed to allow modeling software to exchange models and
simulations. Whereas SBML encodes models, SED-ML encodes simulations, including
the solver (e.g. deterministic or stochastic), the type of simulation (timecourse or
steady state), and various parameters (start/end time, ODE solver tolerances, etc.).
SBML and SED-ML are separate standards and are encoded as separate files, but
are used to encode a complete study.
COMBINE archives package related standards together so that they can be easily
exchanged between software tools. Tellurium provides the *inline OMEX* format
for editing the contents of COMBINE archives in a human-readable format.
You can use the function ``convertCombineArchive`` to convert a COMBINE archive
on disk to an inline OMEX string, and the function ``executeInlineOmex`` to execute
the inline OMEX string. Examples below.

.. autofunction:: tellurium.convertCombineArchive
.. autofunction:: tellurium.executeInlineOmex
.. autofunction:: tellurium.exportInlineOmex
.. autofunction:: tellurium.extractFileFromCombineArchive

--------
SED-ML
--------

.. include:: _notebooks/core/phrasedmlExample.rst
.. include:: _notebooks/core/tesedmlExample.rst

--------------------
Misc
--------------------
Some used cases for tellurium

.. include:: _notebooks/core/tellurium_examples.rst

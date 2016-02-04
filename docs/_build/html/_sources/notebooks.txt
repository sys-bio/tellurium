===================
Examples
===================
All tellurium examples are available as interactive `jupyter notebooks <http://jupyter.readthedocs.org/en/latest/install.html>`_.

To run the examples clone the git repository
::

    git clone https://github.com/sys-bio/tellurium.git

and start jupyter in the notebooks folder
::

    cd tellurium/examples/notebooks
    jupyter notebook index.ipynb

--------------------
Basics
--------------------
.. include:: _notebooks/core/roadrunnerBasics.rst

-------------------------
Models & Model Building
-------------------------
In this section model the creation of example models is shown.

.. include:: _notebooks/core/modelFromBioModels.rst
.. include:: _notebooks/core/nonUnitStoichiometries.rst
.. include:: _notebooks/core/consecutiveUniUniReactions.rst
.. include:: _notebooks/core/feedback_oscillations.rst
.. include:: _notebooks/core/generatingDifferentWaveforms.rst

--------------------
SED-ML & Combine
--------------------
Tellurium supports the simulation description via the simulation experiment
description markup language (SED-ML). 

.. include:: _notebooks/core/phrasedmlExample.rst
.. include:: _notebooks/core/tesedmlExample.rst

--------------------
Parameter scan
--------------------
.. include:: _notebooks/core/parameter_scan.rst
.. include:: _notebooks/core/steadystate_scan.rst
.. include:: _notebooks/core/computeSteadyState.rst

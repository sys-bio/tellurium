===========
Walkthrough
===========

Notebook Walkthrough
====================

If you have not already done so, download and install the `Tellurium notebook front-end <https://github.com/sys-bio/tellurium#front-end-1-tellurium-notebook>`_ for your platform (Windows, Mac, and Linux supported).

Basics
~~~~~~

The notebook environment allows you to mix Python code, narrative, and exchangeable standards for models and simulations. When you first open the notebook, you will have a single Python cell. You can type Python code into this cell. To run the code:

* Press shift-enter,
* Click the play button at the upper right of the cell, or
* Choose ``Cell`` -> ``Run All`` from the menu.

The output of running the cell will be shown beneath the cell.

.. figure:: ./images/notebook-python-cell.png
    :align: center
    :alt: Output of running a Python cell
    :figclass: align-center

    Output of running a Python cell

Creating Cells
~~~~~~~~~~~~~~

You can add new cells by moving your cursor past the last cell in the notebook. You should see a menu with three options: ``New``, ``Import``, and ``Merge``. Choose ``New`` to create a new cell. You will see four choices:

* New Python Cell
* New Markdown Cell (for creating narrative)
* New Model Cell (for SBML/Antimony models)
* New OMEX Cell (for COMBINE archives)

For now, select ``New Markdown Cell``. Markdown cells allow you to place formatted text and hyperlinks in your notebook. For a review of Markdown syntax, please see `this reference <https://guides.github.com/features/mastering-markdown/>`_.

.. figure:: ./images/notebook-new-markdown-cell.png
    :align: center
    :alt: Creating a new Markdown cell
    :figclass: align-center

    Creating a new Markdown cell

.. figure:: ./images/notebook-python-cell.png
    :align: center
    :alt: Editing a Markdown cell
    :figclass: align-center

    Editing a Markdown cell

SBML Cells
~~~~~~~~~~

Unlike vanilla Jupyter, Tellurium allows you embed a human-readable representation of SBML directly in your notebook. To begin, first download the `SBML for the represillator circuit from BioModels <https://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000012>`_. Then, in the Tellurium notebook viewer, move your cursor past the last cell in the notebook and select ``Import`` -> ``Import SBML...``.

.. figure:: ./images/notebook-import-sbml.png
    :align: center
    :alt: Importing an SBML model
    :figclass: align-center

    Importing an SBML model

Navigate to the ``BIOMD0000000012.xml`` file that you downloaded and select it. A new cell will be created in the notebook with a human-readable representation of this model. The human-readable syntax is called Antimony, and you can find an `extensive reference on the syntax here <http://tellurium.readthedocs.io/en/latest/antimony.html>`_. For now, just change the name of the model from ``BIOMD0000000012`` to ``repressilator``.


.. figure:: ./images/notebook-sb-cell-change-name.png
    :align: center
    :alt: Changing the name of the model
    :figclass: align-center

    Changing the name of the model

Now, run the cell. You should see confirmation that the model was correctly loaded and is available under the variable ``repressilator`` in Python.

.. figure:: ./images/notebook-run-sb-cell.png
    :align: center
    :alt: Running the SBML cell
    :figclass: align-center

    Running the SBML cell

After the SBML cell, create a Python cell with the following content:

.. code-block:: python

    repressilator.reset() # in case you run the cell again
    repressilator.simulate(0,1000,1000) # simulate from time 0 to 1000 with 1000 points
    repressilator.plot() # plot the simulation

After you run this cell, you should see the following simulation plot:

.. figure:: ./images/notebook-simulate-sb-cell.png
    :align: center
    :alt: Simulating the SBML model
    :figclass: align-center

    Simulating the SBML model

The ``repressilator`` variable is actually an instance of the `RoadRunner simulator <http://libroadrunner.org/>`_. Please see the `official documentation for libRoadRunner <http://sys-bio.github.io/roadrunner/python_docs/index.html>`_ for an extensive list of methods and options that can be used with RoadRunner.

COMBINE Archive Cells
~~~~~~~~~~~~~~~~~~~~~

Another name for COMBINE archives is the Open Modeling and EXchange format (OMEX), which shows up in various Tellurium menus and functions. COMBINE archives are containers for various community standards in systems biology. They can contain `SBML <http://sbml.org/Main_Page>`_, `SED-ML <https://sed-ml.github.io/>`_, `CellML <https://www.cellml.org/>`_, and `NeuroML <https://www.neuroml.org/>`_. Tellurium supports importing COMBINE archives containing SBML and SED-ML.

To begin, download `this COMBINE archive <https://github.com/0u812/tellurium-combine-archive-test-cases/raw/master/swt/pulse_experiment.omex>`_ example (originally from the `SED-ML Web Tools <http://sysbioapps.dyndns.org/SED-ML_Web_Tools>`_). In the Tellurium notebook viewer, choose ``Import`` -> ``Import COMBINE archive (OMEX)...``.

This archive contains an SBML model and a SED-ML simulation. The simulation has a forcing function (representing external input to the system) in the form of a pulse. After running this cell, you should see the following output:

.. figure:: ./images/notebook-omex-pulse.png
    :align: center
    :alt: Running the OMEX cell
    :figclass: align-center

    Running the OMEX cell

As a demo of Tellurium's COMBINE archive editing functionality, we can change the duration of the pulse. Change the following line:

::

    task1 = repeat task0 for local.index in uniform(0, 10, 100), local.current = index -> piecewise(8, index < 1, 0.1, (index >= 4) && (index < 6), 8), model1.J0_v0 = current : current

To:

::

    task1 = repeat task0 for local.index in uniform(0, 10, 100), local.current = index -> piecewise(8, index < 1, 0.1, (index >= 4) && (index < 10), 8), model1.J0_v0 = current : current

In other words, ``index < 6`` was changed to ``index < 10``. Run the cell:

.. figure:: ./images/notebook-omex-longer-pulse.png
    :align: center
    :alt: Editing the OMEX cell
    :figclass: align-center

    Editing the OMEX cell

You can re-export this cell to a COMBINE archive by clicking the diskette icon in the upper right:

.. figure:: ./images/notebook-save-omex.png
    :align: center
    :alt: Exporting the COMBINE archive
    :figclass: align-center

    Exporting the COMBINE archive

Find/Replace in Notebook Cells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To search for text in a notebook cell, use ``ctrl+F``. To search for whole-words only, use ``/\bmyword\b`` where ``myword`` is the word you want to search for.

.. figure:: ./images/notebook-word-boundary.png
    :align: center
    :alt: Searching for whole words
    :figclass: align-center

    Searching for whole words

To search and replace, use ``ctrl+shift+R``. For example, to replace ``myvar`` but not ``myvar2`` (i.e. whole-word search & replace) in the code below, press ``ctrl+shift+R``, enter ``/\bmyvar\b/`` for the search field and ``newvar`` for the replace field. The result is that all instances of ``myvar`` are replaced, but not ``myvar2``:

.. figure:: ./images/notebook-search-replace-demo-whole-words.png
    :align: center
    :alt: Search & replace demo with whole words
    :figclass: align-center

    Search & replace demo with whole words

Example Notebooks
~~~~~~~~~~~~~~~~~

Tellurium comes with many example notebooks showing how to use its various features. To access these notebooks, use the ``File`` -> ``Open Example Notebook`` menu. Tellurium comes with five example notebooks:

.. figure:: ./images/notebook-open-example-notebook.png
    :align: center
    :alt: Search & replace demo with whole words
    :figclass: align-center

    Search & replace demo with whole words

Notebook Troubleshooting
========================

Problem: Cannot Load Kernel
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The notebook viewer ships with a Python3 kernel, which causes problems when trying to open a notebook saved (e.g. by Jupyter) with Python2.

.. figure:: ./images/notebook-failed-to-load-kernel.png
    :align: center
    :alt: Error message when kernel cannot be loaded
    :figclass: align-center

    Error message when kernel cannot be loaded

Solution
~~~~~~~~

In such a case, simply replace the kernel by choosing ``Language`` -> ``Python 3`` from the menu.

.. figure:: ./images/new-kernel-python-3.png
    :align: center
    :alt: Fix for kernel loading problem
    :figclass: align-center

    Fix for kernel loading problem

Problem: Saving the Notebook Takes Forever
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Solution
~~~~~~~~

When highly detailed / numerous plots are present, Plotly is known to slow down notebook saving. In such cases, please save the notebook without output. Choose ``Language`` -> ``Restart and Clear All Cells``, then save the notebook.

.. figure:: ./images/notebook-reset-clear.png
    :align: center
    :alt: Reset and clear all cells
    :figclass: align-center

    Reset and clear all cells



Further Reading
---------------

* Tellurium notebook is based on the `nteract app <https://blog.nteract.io/nteract-revolutionizing-the-notebook-experience-d106ca5d2c38>`_.
* `Jupyter. <http://jupyter.org/>`_

------------

IDE Walkthrough
====================

If you have not already done so, download and install the `Tellurium IDE front-end <https://github.com/sys-bio/tellurium#front-end-2-tellurium-ide>`_ for your platform (only for Windows, legacy versions supported Mac).

Further Reading
---------------

* `Official Spyder documentation <http://pythonhosted.org/spyder/>`_

------------

Additional Resources for Tellurium
==================================

* `Suggest a new feature for Tellurium with UserVoice. <http://sysbio.uservoice.com/>`_
* `Herbert Sauro's modeling textbook <http://tellurium.analogmachine.org/new-modeling-text-book/>`_, which uses Tellurium
* `YouTube video tutorials <https://www.youtube.com/channel/UCpNSURm4YWe7sF0561mcvkg>`_ (made prior to Tellurium notebook).

Learning Python
===============

* `Google's Python class. <https://developers.google.com/edu/python/>`_
* Official tutorial for `Python 2 <https://docs.python.org/2/tutorial/>`_ and `Python 3 <https://docs.python.org/3/tutorial/>`_.

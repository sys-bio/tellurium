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

Navigate to the ``BIOMD0000000012.xml`` file that you downloaded and select it. A new cell will be created in the notebook with a human-readable representation of this model. The human-readable syntax is called Antimony, and you can find an extensive reference on the syntax here. For now, just change the name of the model from ``BIOMD0000000012`` to ``repressilator``.


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

The ``repressilator`` variable is actually an instance of the `RoadRunner simulator <http://libroadrunner.org/>`_. Please see the `official documentation for libRoadRunner <http://sys-bio.github.io/roadrunner/python_docs/index.html>`_ for an extensive list of methods and options for running on RoadRunner.

* **TODO**: Add how to use inline OMEX cells.
* **TODO**: Show how to search/replace with CM and search word boundaries.
* **TODO**: Show how to access example notebooks.
* **TODO**: Demo interactive plotting online with Plotly

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

Notebook Troubleshooting
========================

Problem: Saving the Notebook Takes Forever
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Solution
~~~~~~~~

When highly detailed / numerous plots are presentPlotly is known to slow down notebook saving. In such cases, please save the notebook without output. Choose ``Language`` -> ``Restart and Clear All Cells``, then save the notebook.

.. figure:: ./images/new-kernel-python-3.png
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

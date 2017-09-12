

Model loading from BioModels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models can be easily retrieved from BioModels using the
``loadSBMLModel`` function in Tellurium. This example uses a download
URL to directly load ``BIOMD0000000010``.

.. code-block:: python

    import tellurium as te
    
    # Load model from biomodels (may not work with https).
    r = te.loadSBMLModel("http://biomodels.caltech.edu/download?mid=BIOMD0000000010")
    result = r.simulate(0, 3000, 5000)
    r.plot(result)


.. parsed-literal::

    /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages/matplotlib/__init__.py:1405: UserWarning: 
    This call to matplotlib.use() has no effect because the backend has already
    been chosen; matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
    or matplotlib.backends is imported for the first time.
    
      warnings.warn(_use_error_msg)



.. raw:: html

    <script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window.Plotly) {{require(['plotly'],function(plotly) {window.Plotly=plotly;});}}</script>


.. parsed-literal::

    /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages/matplotlib/__init__.py:1405: UserWarning:
    
    
    This call to matplotlib.use() has no effect because the backend has already
    been chosen; matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
    or matplotlib.backends is imported for the first time.
    
    



.. image:: _notebooks/core/model_modelFromBioModels_files/model_modelFromBioModels_2_3.png


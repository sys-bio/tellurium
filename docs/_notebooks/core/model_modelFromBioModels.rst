

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



.. raw:: html

    <script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window.Plotly) {{require(['plotly'],function(plotly) {window.Plotly=plotly;});}}</script>



.. image:: _notebooks/core/model_modelFromBioModels_files/model_modelFromBioModels_2_1.png


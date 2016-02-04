

Model loading from BioModels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models can be easily retrieved from BioModels via their identifier.

.. code:: python

    import tellurium as te
    
    # Load model from biomodels.
    r = te.loadSBMLModel("http://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000010")
    result = r.simulate(0, 3000, 5000)
    r.plot(result)



.. image:: _notebooks/core/modelFromBioModels_files/modelFromBioModels_2_0.png





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


::


    ---------------------------------------------------------------------------

    RuntimeError                              Traceback (most recent call last)

    <ipython-input-1-8a25f612667b> in <module>()
          5 
          6 # Load model from biomodels (may not work with https).
    ----> 7 r = te.loadSBMLModel("http://biomodels.caltech.edu/download?mid=BIOMD0000000010")
          8 result = r.simulate(0, 3000, 5000)
          9 r.plot(result)


    /extra/devel/src/tellurium/tellurium/tellurium.py in loadSBMLModel(sbml)
        557     :rtype: roadrunner.ExtendedRoadRunner
        558     """
    --> 559     return roadrunner.RoadRunner(sbml)
        560 
        561 


    /extra/devel/src/tellurium/tellurium/roadrunner/extended_roadrunner.py in __init__(self, *args, **kwargs)
         14 
         15     def __init__(self, *args, **kwargs):
    ---> 16         super(ExtendedRoadRunner, self).__init__(*args, **kwargs)
         17 
         18     # ---------------------------------------------------------------------


    ~/.config/Tellurium/telocal/python-3.6.3/lib/python3.6/site-packages/roadrunner/roadrunner.py in _new_init(self, *args)
       3513                 return
       3514     # Otherwise, use regular init
    -> 3515         RoadRunner._swig_init(self, *args)
       3516         RoadRunner._makeProperties(self)
       3517 


    ~/.config/Tellurium/telocal/python-3.6.3/lib/python3.6/site-packages/roadrunner/roadrunner.py in __init__(self, *args)
       2520 
       2521     def __init__(self, *args):
    -> 2522         this = _roadrunner.new_RoadRunner(*args)
       2523         try:
       2524             self.this.append(this)


    RuntimeError: static std::string rr::SBMLReader::read(const string&), could not open http://biomodels.caltech.edu/download?mid=BIOMD0000000010 as a file or uri


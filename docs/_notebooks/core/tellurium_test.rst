

Test models
~~~~~~~~~~~

.. code:: ipython2

    import tellurium as te
    
    # To get the builtin models use listTestModels
    print(te.listTestModels())


.. parsed-literal::

    ['linearPathwayClosed.xml', 'EcoliCore.xml', 'linearPathwayOpen.xml', 'feedback.xml', 'test_1.xml']


Load test model
^^^^^^^^^^^^^^^

.. code:: ipython2

    # To load one of the test models use loadTestModel:
    # r = te.loadTestModel('feedback.xml')
    # result = r.simulate (0, 10, 100)
    # r.plot (result)
    
    # If you need to obtain the SBML for the test model, use getTestModel
    sbml = te.getTestModel('feedback.xml')
    
    # To look at one of the test model in Antimony form:
    ant = te.sbmlToAntimony(te.getTestModel('feedback.xml'))
    print(ant)


::


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-2-7fb38c51b431> in <module>()
          8 
          9 # To look at one of the test model in Antimony form:
    ---> 10 ant = te.sbmlToAntimony(te.getTestModel('feedback.xml'))
         11 print(ant)


    /extra/devel/src/tellurium/tellurium/tellurium.py in sbmlToAntimony(sbml)
        637     else:
        638         code = antimony.loadSBMLString(str(sbml))
    --> 639     _checkAntimonyReturnCode(code)
        640     return antimony.getAntimonyString(None)
        641 


    /extra/devel/src/tellurium/tellurium/tellurium.py in _checkAntimonyReturnCode(code)
        291     """
        292     if code < 0:
    --> 293         raise Exception('Antimony: {}'.format(antimony.getLastError()))
        294 
        295 def colorCycle(color,polyNumber):


    Exception: Antimony: Unable to read SBML string due to errors encountered when parsing the file.  Error(s) from libSBML:
    
    line 2: (01035 [Error]) Main XML content is empty.
    



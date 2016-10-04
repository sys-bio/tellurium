

Test models
~~~~~~~~~~~

.. code:: python

    import tellurium as te
    
    # To get the builtin models use listTestModels
    print(te.listTestModels())


.. parsed-literal::

    ['linearPathwayOpen.xml', 'test_1.xml', 'EcoliCore.xml', 'feedback.xml', 'linearPathwayClosed.xml']


Load test model
^^^^^^^^^^^^^^^

.. code:: python

    # To load one of the test models use loadTestModel:
    # r = te.loadTestModel('feedback.xml')
    # result = r.simulate (0, 10, 100)
    # r.plot (result)
    
    # If you need to obtain the SBML for the test model, use getTestModel
    sbml = te.getTestModel('feedback.xml')
    
    # To look at one of the test model in Antimony form:
    ant = te.sbmlToAntimony(te.getTestModel('feedback.xml'))
    print(ant)


.. parsed-literal::

    // Created by libAntimony v2.9
    model *feedback()
    
      // Compartments and Species:
      compartment compartment_;
      species S1 in compartment_, S2 in compartment_, S3 in compartment_, S4 in compartment_;
      species $X0 in compartment_, $X1 in compartment_;
    
      // Reactions:
      J0: $X0 => S1; J0_VM1*(X0 - S1/J0_Keq1)/(1 + X0 + S1 + S4^J0_h);
      J1: S1 => S2; (10*S1 - 2*S2)/(1 + S1 + S2);
      J2: S2 => S3; (10*S2 - 2*S3)/(1 + S2 + S3);
      J3: S3 => S4; (10*S3 - 2*S4)/(1 + S3 + S4);
      J4: S4 => $X1; J4_V4*S4/(J4_KS4 + S4);
    
      // Species initializations:
      S1 = 0;
      S2 = 0;
      S3 = 0;
      S4 = 0;
      X0 = 10;
      X1 = 0;
    
      // Compartment initializations:
      compartment_ = 1;
    
      // Variable initializations:
      J0_VM1 = 10;
      J0_Keq1 = 10;
      J0_h = 10;
      J4_V4 = 2.5;
      J4_KS4 = 0.5;
    
      // Other declarations:
      const compartment_, J0_VM1, J0_Keq1, J0_h, J4_V4, J4_KS4;
    end
    


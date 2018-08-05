

Non-unit stoichiometries
~~~~~~~~~~~~~~~~~~~~~~~~

The following example demonstrates how to create a model with non-unit
stoichiometries.

.. code-block:: python

    import tellurium as te
    
    r = te.loada('''
      model pathway()
        S1 + S2 -> 2 S3; k1*S1*S2
        3 S3 -> 4 S4 + 6 S5; k2*S3^3
        k1 = 0.1;k2 = 0.1;
      end
    ''')
    print(r.getCurrentAntimony())


.. parsed-literal::

    // Created by libAntimony v2.9.4
    model *pathway()
    
      // Compartments and Species:
      species S1, S2, S3, S4, S5;
    
      // Reactions:
      _J0: S1 + S2 -> 2 S3; k1*S1*S2;
      _J1: 3 S3 -> 4 S4 + 6 S5; k2*S3^3;
    
      // Species initializations:
      S1 = 0;
      S2 = 0;
      S3 = 0;
      S4 = 0;
      S5 = 0;
    
      // Variable initializations:
      k1 = 0.1;
      k2 = 0.1;
    
      // Other declarations:
      const k1, k2;
    end
    



Consecutive UniUni reactions using first-order mass-action kinetics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model creation and simulation of a simple irreversible chain of
reactions S1 -> S2 -> S3 -> S4.

.. code:: python


.. code:: python

    from __future__ import print_function
    import tellurium as te
    
    r = te.loada('''
      model pathway()
        S1 -> S2; k1*S1
        S2 -> S3; k2*S2
        S3 -> S4; k3*S3
    
        # Initialize values
        S1 = 5; S2 = 0; S3 = 0; S4 = 0;
        k1 = 0.1;  k2 = 0.55; k3 = 0.76
      end
    ''')
    
    result = r.simulate(0, 20, 51)
    te.plotArray(result);



.. image:: _notebooks/core/consecutiveUniUniReactions_files/consecutiveUniUniReactions_2_0.png



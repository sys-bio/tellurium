

Steady state calculation
~~~~~~~~~~~~~~~~~~~~~~~~

Steady states can be calculated using ``r.getSteadyStateValues``

.. code:: ipython2

    import tellurium as te
    from roadrunner import Config
    
    Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, True) 
    
    r = te.loada('''
      model pathway()
         $Xo -> S1; k1*Xo - k2*S1
          S1 -> S2; k3*S2
          S2 -> $X1; k4*S2
    
         Xo = 1;   X1 = 0
         S1 = 0;   S2 = 0
         k1 = 0.1; k2 = 0.56
         k3 = 1.2; k4 = 0.9
      end
    ''')
    
    # Compute steady state
    values = r.getSteadyStateValues()
    for sid, value in zip(r.steadyStateSelections, r.getSteadyStateValues()):
        print(sid, "=", value)
    Config.setValue(Config.LOADSBMLOPTIONS_CONSERVED_MOIETIES, False)


.. parsed-literal::

    [S1] = 0.17857142857142858
    [S2] = 0.0


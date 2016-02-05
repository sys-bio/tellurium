

Stochastic simulation
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import tellurium as te
    import numpy as np
    
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 40')
    r.setIntegrator('gillespie')
    
    results = []
    for k in range(1, 50):
        r.reset()
        s = r.simulate(0, 40)
        results.append(s)
        r.plot(s, show=False, loc=None, color='black', alpha=0.7)



.. image:: _notebooks/core/tellurium_stochastic_files/tellurium_stochastic_2_0.png


.. code:: python

    # Setting the seed results in reproducible stochastic simulation
    results = []
    for k in range(1, 20):
        r.reset()
        r.setSeed(123456)
        s = r.simulate(0, 40)
        results.append(s)
        r.plot(s, show=False, loc=None, color='black', alpha=0.7)



.. image:: _notebooks/core/tellurium_stochastic_files/tellurium_stochastic_3_0.png


Run two simulations and combine the two
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import tellurium as te
    import numpy as np
    
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.02; S1 = 100')
    for k in range(1, 20):
        r.resetToOrigin()
        res1 = r.gillespie(0, 10)
        # change in parameter after the first half of the simulation
        r.k1 = r.k1*20
        res2 = r.gillespie (10, 20)
        r.plot(np.vstack([res1, res2]), color='black', alpha=0.7, show=False, loc=None)



.. image:: _notebooks/core/tellurium_stochastic_files/tellurium_stochastic_5_0.png



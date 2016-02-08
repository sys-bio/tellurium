

Simple Example
~~~~~~~~~~~~~~

.. code:: python

    import tellurium as te
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    r.simulate(0, 50, 100)
    r.plot()



.. image:: _notebooks/core/introduction_files/introduction_2_0.png




.. parsed-literal::

    <module 'matplotlib.pyplot' from '/usr/local/lib/python2.7/dist-packages/matplotlib/pyplot.pyc'>



More Complex Example
~~~~~~~~~~~~~~~~~~~~

Stochastic simulation of a linear chain.

.. code:: python

    import tellurium as te
    r = te.loada('''
        J1: S1 -> S2;  k1*S1; 
        J2: S2 -> S3; k2*S2 - k3*S3
        # J2_1: S2 -> S3; k2*S2
        # J2_2: S3 -> S2; k3*S3;
        J3: S3 -> S4; k4*S3;
    
        k1 = 0.1; k2 = 0.5; k3 = 0.5; k4 = 0.5;
        S1 = 100;
    ''')
    r.draw(width=300)
    
    # set integrator, seed and selections for output
    r.setIntegrator('gillespie')
    r.setSeed(1234)
    r.selections = ['time'] + r.getBoundarySpeciesIds() + r.getFloatingSpeciesIds()
    
    # run repeated simulation
    for k in range(1,10):
        r.resetToOrigin()
        s = r.simulate(0, 50)
        r.plot(s, show=False, loc=None, color='black', alpha=0.7)
    r.plot();



.. image:: _notebooks/core/introduction_files/introduction_4_0.png



.. image:: _notebooks/core/introduction_files/introduction_4_1.png



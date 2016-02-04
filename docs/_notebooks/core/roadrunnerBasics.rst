

Model Loading
~~~~~~~~~~~~~

To load models use the load functions

-  ``te.loadAntimony`` (``te.loada``): load Antimony model
-  ``te.loadSBML``: load SBML model
-  ``te.loadCellML``: load CellML model

.. code:: python

    import tellurium as te
    
    model = """
    model test
        compartment C1;
        C1 = 1.0;
        species S1, S2;
        
        S1 = 10.0;
        S2 = 0.0;
        S1 in C1; S2 in C1;
        J1: S1 -> S2; k1*S1;
        
        k1 = 1.0;
    end
    """
    # load models
    r = te.loada(model)

Integrator and Integrator Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set the integrator use ``r.setIntegrator(integrator)``.

To set integrator settings use ``r.integrator.setValue(key, value)``.
For instance

-  ``variable_step_size``
-  ``stiff``
-  ``absolute_tolerance``
-  ``relative_tolerance``
-  ``seed``

.. code:: python

    # set integrator
    r.setIntegrator('rk4')
    r.setIntegrator('gillespie')
    r.setIntegrator('cvode')
    
    # set integrator settings
    r.integrator.setValue('variable_step_size', False)
    r.integrator.setValue('stiff', True)
    
    # print integrator settings
    print(r.integrator)


.. parsed-literal::

    < roadrunner.Integrator() >
      settings:
          relative_tolerance: 0.00001
          absolute_tolerance: 0.0000000001
                       stiff: true
           maximum_bdf_order: 5
         maximum_adams_order: 12
           maximum_num_steps: 20000
           maximum_time_step: 0
           minimum_time_step: 0
           initial_time_step: 0
              multiple_steps: false
          variable_step_size: false
    


Simulation options
~~~~~~~~~~~~~~~~~~

The simulation options

-  ``start``: start time
-  ``end``: end time
-  ``points``: number of points in solution
-  ``steps``: number of steps in solution

are set as arguments in ``r.simulate``

.. code:: python

    # simulate from 0 to 6 with 6 points in the result
    r.reset()
    res1 = r.simulate(start=0, end=10, points=6)
    print(res1)
    r.reset()
    res2 = r.simulate(0, 10, 6)
    print(res2)


.. parsed-literal::

        time,        [S1],    [S2]
     [[    0,          10,       0],
      [    2,     1.35329, 8.64671],
      [    4,    0.183132, 9.81687],
      [    6,    0.024782, 9.97522],
      [    8,  0.00335358, 9.99665],
      [   10, 0.000453818, 9.99955]]
    
        time,        [S1],    [S2]
     [[    0,          10,       0],
      [    2,     1.35329, 8.64671],
      [    4,    0.183132, 9.81687],
      [    6,    0.024782, 9.97522],
      [    8,  0.00335358, 9.99665],
      [   10, 0.000453818, 9.99955]]
    


Selections
~~~~~~~~~~

Selections can be either given as argument to ``r.simulate`` or set via
``r.selections``.

.. code:: python

    # set selections directly
    r.selections = ['time', 'J1']
    print(r.simulate(0,10,6))
    # provide arguments to simulate
    print(r.simulate(0,10,6, selections=r.getFloatingSpeciesIds()))


.. parsed-literal::

        time,          J1
     [[    0, 0.000453818],
      [    2, 6.14191e-05],
      [    4, 8.31285e-06],
      [    6, 1.12523e-06],
      [    8, 1.52689e-07],
      [   10, 2.07032e-08]]
    
                  S1, S2
     [[  2.07032e-08, 10],
      [  2.71764e-09, 10],
      [  4.08585e-10, 10],
      [  6.85818e-11, 10],
      [  1.47247e-11, 10],
      [ -3.51877e-12, 10]]
    


Reset model variables
~~~~~~~~~~~~~~~~~~~~~

To reset variables use the ``r.reset()`` and
``r.reset(SelectionRecord.*)`` functions.

.. code:: python

    # show the current values
    for s in ['S1', 'S2']:
        print('r.{} == {}'.format(s, r[s]))
    # reset initial concentrations
    r.reset()
    print('reset')
    # S1 and S2 have now again the initial values
    for s in ['S1', 'S2']:
        print('r.{} == {}'.format(s, r[s]))


.. parsed-literal::

    r.S1 == -3.5187697416e-12
    r.S2 == 10.0
    reset
    r.S1 == 10.0
    r.S2 == 0.0



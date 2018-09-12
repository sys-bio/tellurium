

Reset model values
^^^^^^^^^^^^^^^^^^

The ``reset`` function of a
`RoadRunner <https://libroadrunner.readthedocs.io/en/latest/api_reference.html?highlight=reset#RoadRunner.RoadRunner.reset>`__
instance reset the system variables (usually species concentrations) to
their respective initial values. ``resetAll`` resets variables to their CURRENT initial as well as resets parameters.
``resetToOrigin`` completely resets the model.

.. code-block:: python

    import tellurium as te
    te.setDefaultPlottingEngine('matplotlib')

    r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    r.integrator.setValue('variable_step_size', True)

    # simulate model
    sim1 = r.simulate(0, 5)
    print('*** sim1 ***')
    r.plot(sim1)

    # continue from end concentration of sim1
    r.k1 = 2.0
    sim2 = r.simulate(0, 5)
    print('-- sim2 --')
    print('continue simulation from final concentrations with changed parameter')
    r.plot(sim2)

    # Reset initial concentrations, does not affect the changed parameter
    r.reset()
    sim3 = r.simulate(0, 5)
    print('-- sim3 --')
    print('reset initial concentrations but keep changed parameter')
    r.plot(sim3)

    # Change CURRENT initial of k1, resetAll clears parameter but 
    # resets to CURRENT initial
    r.setValue('init(k1)', 0.3)
    r.resetAll()
    sim4 = r.simulate(0, 5)
    print('-- sim4 --')
    print('reset to CURRENT initial of k1, reset to initial parameters')
    print('k1 = ' + str(r.k1))
    r.plot(sim4)

    # Reset model to the state it was loaded
    r.resetToOrigin()
    sim5 = r.simulate(0, 5)
    print('-- sim5 --')
    print('reset all to origin')
    r.plot(sim5);


.. parsed-literal::

    *** sim1 ***



.. image:: _notebooks/core/tellurium_reset_files/tellurium_reset_2_1.png


.. parsed-literal::

    -- sim2 --
    continue simulation from final concentrations with changed parameter



.. image:: _notebooks/core/tellurium_reset_files/tellurium_reset_2_3.png


.. parsed-literal::

    -- sim3 --
    reset initial concentrations but keep changed parameter



.. image:: _notebooks/core/tellurium_reset_files/tellurium_reset_2_5.png


.. parsed-literal::

    -- sim4 --
    reset to CURRENT initial of k1, reset to initial parameters
    k1 = 0.3

.. image:: _notebooks/core/tellurium_reset_files/tellurium_reset_2_6.png

.. parsed-literal::

    -- sim5 --
    reset all to origin


.. image:: _notebooks/core/tellurium_reset_files/tellurium_reset_2_7.png


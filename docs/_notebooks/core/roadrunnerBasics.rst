

Model Loading
~~~~~~~~~~~~~

To load models use any the following functions. Each function takes a
model with the corresponding format and converts it to a
```RoadRunner`` <http://sys-bio.github.io/roadrunner/python_docs/index.html>`__
simulator instance.

-  ``te.loadAntimony`` (``te.loada``): Load an Antimony model.
-  ``te.loadSBML``: Load an SBML model.
-  ``te.loadCellML``: Load a CellML model (this passes the model through
   Antimony and converts it to SBML, may be lossy).

.. code-block:: python

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


.. parsed-literal::

    /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages/matplotlib/__init__.py:1405: UserWarning: 
    This call to matplotlib.use() has no effect because the backend has already
    been chosen; matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
    or matplotlib.backends is imported for the first time.
    
      warnings.warn(_use_error_msg)



.. raw:: html

    <script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window.Plotly) {{require(['plotly'],function(plotly) {window.Plotly=plotly;});}}</script>


Integrator and Integrator Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set the integrator use ``r.setIntegrator(<integrator-name>)`` or
``r.integrator = <integrator-name>``. RoadRunner supports ``'cvode'``,
``'gillespie'``, and ``'rk4'`` for the integrator name. CVODE uses
adaptive stepping internally, regardless of whether the output is
gridded or not. The size of these

To set integrator settings use ``r.integrator.setValue(key, value)``.
Here are some important settings for the ``cvode`` integrator:

-  ``variable_step_size``: Adaptive step-size integration
   (``True``/``False``).
-  ``stiff``: Stiff solver for CVODE only (``True``/``False``). Enabled
   by default.
-  ``absolute_tolerance``: Absolute numerical tolerance for integrator
   internal stepping.
-  ``relative_tolerance``: Relative numerical tolerance for integrator
   internal stepping.

For the ``gillespie`` integrator:

-  ``seed``: The RNG seed for the Gillespie method. You can set this
   before running a simulation, or leave it alone for a different seed
   each time. Simulations initialized with the same seed will have the
   same results.

You can also use settings as properties, e.g.
``r.integrator.seed = 1234`` is a shorthand for ``setValue``.

.. code-block:: python

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
      name: cvode
      settings:
          relative_tolerance: 0.000001
          absolute_tolerance: 0.000000000001
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

The ``RoadRunner.simulate`` method is responsible for running
simulations using the current integrator. It accepts the following
arguments:

-  ``start``: Start time.
-  ``end``: End time.
-  ``points``: Number of points in solution (exclusive with steps, do
   not pass both). If the output is gridded, the points will be evenly
   spaced in time. If not, the simulation will stop when it reaches the
   ``end`` time or the number of points, whichever happens first.
-  ``steps``: Number of steps in solution (exclusive with points, do not
   pass both).

.. code-block:: python

    # simulate from 0 to 6 with 6 points in the result
    r.reset()
    # pass args explicitly via keywords
    res1 = r.simulate(start=0, end=10, points=6)
    print(res1)
    r.reset()
    # use positional args to pass start, end, num. points
    res2 = r.simulate(0, 10, 6)
    print(res2)


.. parsed-literal::

        time,       [S1],    [S2]
     [[    0,         10,       0],
      [    2,    1.35337, 8.64663],
      [    4,   0.183161, 9.81684],
      [    6,  0.0247885, 9.97521],
      [    8, 0.00335481, 9.99665],
      [   10, 0.00045403, 9.99955]]
    
        time,       [S1],    [S2]
     [[    0,         10,       0],
      [    2,    1.35337, 8.64663],
      [    4,   0.183161, 9.81684],
      [    6,  0.0247885, 9.97521],
      [    8, 0.00335481, 9.99665],
      [   10, 0.00045403, 9.99955]]
    


Selections
~~~~~~~~~~

The selections list can be used to set which state variables will appear
in the output array. By default, it includes all SBML species and the
``time`` variable. Selections can be either given as argument to
``r.simulate`` or set via ``r.selections``.

.. code-block:: python

    # set selections directly
    r.selections = ['time', 'J1']
    print(r.simulate(0,10,6))
    # provide arguments to simulate
    print(r.simulate(0,10,6, selections=r.getFloatingSpeciesIds()))


.. parsed-literal::

        time,          J1
     [[    0,  0.00045403],
      [    2, 6.14464e-05],
      [    4, 8.31595e-06],
      [    6, 1.12545e-06],
      [    8, 1.52314e-07],
      [   10, 2.06149e-08]]
    
                 S1, S2
     [[ 2.06149e-08, 10],
      [    2.79e-09, 10],
      [ 3.76786e-10, 10],
      [ 5.12139e-11, 10],
      [ 7.13659e-12, 10],
      [ 2.54938e-12, 10]]
    


Reset model variables
~~~~~~~~~~~~~~~~~~~~~

To reset the model's state variables use the ``r.reset()`` and
``r.reset(SelectionRecord.*)`` functions. If you have made modifications
to parameter values, use the ``r.resetAll()`` function to reset
parameters to their initial values when the model was loaded.

.. code-block:: python

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

    r.S1 == 2.5493789989501883e-12
    r.S2 == 9.999999999997451
    reset
    r.S1 == 10.0
    r.S2 == 0.0


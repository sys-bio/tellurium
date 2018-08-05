

Draw diagram
^^^^^^^^^^^^

This example shows how to draw a network diagram, `requires
graphviz <http://tellurium.readthedocs.io/en/latest/notebooks.html#preliminaries>`__.

.. code-block:: python

    import tellurium as te
    te.setDefaultPlottingEngine('matplotlib')
    
    r = te.loada('''
    model feedback()
       // Reactions:http://localhost:8888/notebooks/core/tellurium_export.ipynb#
       J0: $X0 -> S1; (VM1 * (X0 - S1/Keq1))/(1 + X0 + S1 +   S4^h);
       J1: S1 -> S2; (10 * S1 - 2 * S2) / (1 + S1 + S2);
       J2: S2 -> S3; (10 * S2 - 2 * S3) / (1 + S2 + S3);
       J3: S3 -> S4; (10 * S3 - 2 * S4) / (1 + S3 + S4);
       J4: S4 -> $X1; (V4 * S4) / (KS4 + S4);
    
      // Species initializations:
      S1 = 0; S2 = 0; S3 = 0;
      S4 = 0; X0 = 10; X1 = 0;
    
      // Variable initialization:
      VM1 = 10; Keq1 = 10; h = 10; V4 = 2.5; KS4 = 0.5;
    end''')
    
    # simulate using variable step size
    r.integrator.setValue('variable_step_size', True)
    s = r.simulate(0, 50)
    # draw the diagram
    r.draw(width=200)
    # and the plot
    r.plot(s, title="Feedback Oscillations", ylabel="concentration", alpha=0.9);


::


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-1-1762a727bd4c> in <module>()
         25 s = r.simulate(0, 50)
         26 # draw the diagram
    ---> 27 r.draw(width=200)
         28 # and the plot
         29 r.plot(s, title="Feedback Oscillations", ylabel="concentration", alpha=0.9);


    /extra/devel/src/tellurium/tellurium/roadrunner/extended_roadrunner.py in draw(self, **kwargs)
        286 
        287         from tellurium import SBMLDiagram
    --> 288         diagram = SBMLDiagram(self.getSBML())
        289         diagram.draw(**kwargs)
        290 


    /extra/devel/src/tellurium/tellurium/visualization/sbmldiagram.py in __init__(self, sbml, species, reactions, reactants, products, modifiers)
         59                                           reactants=reactants,
         60                                           products=products,
    ---> 61                                           modifiers=modifiers)
         62 
         63 


    /extra/devel/src/tellurium/tellurium/visualization/sbmldiagram.py in _createGraph(model, species, reactions, reactants, products, modifiers)
         89             warnings.warn("'pygraphviz' could not be imported, cannot draw network diagrams", ImportWarning, stacklevel=2)
         90 
    ---> 91         g = pgv.AGraph(strict=False, directed=True)
         92 
         93         # set some default node attributes


    AttributeError: 'NoneType' object has no attribute 'AGraph'


Plotting multiple simulations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All plotting is done via the ``r.plot`` or ``te.plotArray`` functions.
To plot multiple curves in one figure use the ``show=False`` setting.

.. code-block:: python

    import tellurium as te
    te.setDefaultPlottingEngine('matplotlib')
    import numpy as np
    import matplotlib.pylab as plt
    
    # Load a model and carry out a simulation generating 100 points
    r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    r.draw(width=100)
    
    # get colormap
    # Colormap instances are used to convert data values (floats) from the interval [0, 1]
    cmap = plt.get_cmap('Blues')
    
    k1_values = np.linspace(start=0.1, stop=1.5, num=15)
    max_k1 = max(k1_values)
    for k, value in enumerate(k1_values):
        r.reset()
        r.k1 = value
        s = r.simulate(0, 30, 100)
        
        color = cmap((value+max_k1)/(2*max_k1))
        # use show=False to plot multiple curves in the same figure
        r.plot(s, show=False, title="Parameter variation k1", xtitle="time", ytitle="concentration", 
              xlim=[-1, 31], ylim=[-0.1, 11])
    
    te.show()
    
    print('Reference Simulation: k1 = {}'.format(r.k1))
    print('Parameter variation: k1 = {}'.format(k1_values))


::


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-2-5a68953df668> in <module>()
          7 # Load a model and carry out a simulation generating 100 points
          8 r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    ----> 9 r.draw(width=100)
         10 
         11 # get colormap


    /extra/devel/src/tellurium/tellurium/roadrunner/extended_roadrunner.py in draw(self, **kwargs)
        286 
        287         from tellurium import SBMLDiagram
    --> 288         diagram = SBMLDiagram(self.getSBML())
        289         diagram.draw(**kwargs)
        290 


    /extra/devel/src/tellurium/tellurium/visualization/sbmldiagram.py in __init__(self, sbml, species, reactions, reactants, products, modifiers)
         59                                           reactants=reactants,
         60                                           products=products,
    ---> 61                                           modifiers=modifiers)
         62 
         63 


    /extra/devel/src/tellurium/tellurium/visualization/sbmldiagram.py in _createGraph(model, species, reactions, reactants, products, modifiers)
         89             warnings.warn("'pygraphviz' could not be imported, cannot draw network diagrams", ImportWarning, stacklevel=2)
         90 
    ---> 91         g = pgv.AGraph(strict=False, directed=True)
         92 
         93         # set some default node attributes


    AttributeError: 'NoneType' object has no attribute 'AGraph'


Logarithmic axis
^^^^^^^^^^^^^^^^

The axis scale can be adapted with the ``xscale`` and ``yscale``
settings.

.. code-block:: python

    import tellurium as te
    te.setDefaultPlottingEngine('matplotlib')
    r = te.loadTestModel('feedback.xml')
    r.integrator.variable_step_size = True
    s = r.simulate(0, 50)
    r.plot(s, logx=True, xlim=[10E-4, 10E2],
          title="Logarithmic x-Axis with grid", ylabel="concentration");



.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_6_0.png


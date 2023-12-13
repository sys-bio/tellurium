Add plot elements
~~~~~~~~~~~~~~~~~

Example showing how to embelish a graph - change title, axes labels, set axis limit.
Example also uses an event to pulse S1.

.. code-block:: python

    import tellurium as te, roadrunner
    
    r = te.loada ('''
       $Xo -> S1; k1*Xo;
       S1 -> $X1; k2*S1;
       
       k1 = 0.2; k2 = 0.4; Xo = 1; S1 = 0.5;
       at (time > 20): S1 = S1 + 0.35
    ''')
    
    # Simulate the first part up to 20 time units
    m = r.simulate (0, 50, 100, ["time", "S1"])
                                                                # using latex syntax to render math
    r.plot(m, ylim=(0.,1.), xlabel='Time', ylabel='Concentration', title='My First Plot ($y = x^2$)')

.. image:: _notebooks/core/tellurium_examples_files/tellurium_examples_9_0.png

Saving plots
~~~~~~~~~~~~

To save a plot, use ``r.plot`` and the ``savefig`` parameter. Use ``dpi`` to specify image quality. 
Pass in the save location along with the image name.

.. code-block:: python

    import tellurium as te, os
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    result = r.simulate(0, 50, 100)
    currentDir = os.getcwd() # gets the current directory
    r.plot(title='My plot', xlabel='Time', ylabel='Concentration', dpi=150,
           savefig=currentDir + '\\test.png')  # save image to current directory as "test.png"


The path can be specified as a written out string. The plot can also be saved as a pdf instead of png. 

.. code-block:: python

    savefig='C:\\Tellurium-Winpython-3.6\\settings\\.spyder-py3\\test.pdf'

Logarithmic axis
~~~~~~~~~~~~~~~~

The axis scale can be adapted with the ``xscale`` and ``yscale``
settings.

.. code-block:: python

    import tellurium as te
     
    r = te.loadTestModel('feedback.xml')
    r.integrator.variable_step_size = True
    s = r.simulate(0, 50)
    r.plot(s, logx=True, xlim=[10E-4, 10E2],
          title="Logarithmic x-Axis with grid", ylabel="concentration");
          

.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_4_0.png


Plotting multiple simulations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All plotting is done via the ``r.plot`` or ``te.plotArray`` functions.
To plot multiple curves in one figure use the ``show=False`` setting.

.. code-block:: python

    import tellurium as te
     
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
        r.plot(s, show=False, title="Parameter variation k1", xlabel="time", ylabel="concentration",
              xlim=[-1, 31], ylim=[-0.1, 11])
    
    te.show()
    
    print('Reference Simulation: k1 = {}'.format(r.k1))
    print('Parameter variation: k1 = {}'.format(k1_values))

.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_2_0.png

.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_2_1.png

.. parsed-literal::

    Reference Simulation: k1 = 1.5
    Parameter variation: k1 = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.  1.1 1.2 1.3 1.4 1.5]

Using Tags and Names
~~~~~~~~~~~~~~~~~~~~

Tags can be used to coordinate the color, opacity, and legend names between several sets of data. This can be used to highlight certain features that these datasets have in common. Names allow you to give a more meaningful description of the data in the legend.

.. code-block:: python

    import tellurium as te
    import numpy as np

    for i in range(1, 10):
        x = np.linspace(0, 10, num = 10)
        y = i*x**2 + 10*i

        if i % 2 == 0:
            next_tag = "positive slope"
        else:
            next_tag = "negative slope"
            y = -1*y

        next_name = next_tag + " (i = " + str(i) + ")"    
        te.plot(x, y, show = False, tag = next_tag, name = next_name)

    te.show()

.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_3_0.png

Note that only two items show up in the legend, one for each tag used. In this case, the name found in the legend will match the name of the last set of data plotted using that specific tag. The color and opacity for each tagged groups will also be chosen from the last dataset inputted with that given tag.


Subplots
~~~~~~~~

``te.plotArray`` can be used in conjunction with matplotlib functions to create subplots.

.. code-block:: python

    import tellurium as te
    import numpy as np
    import matplotlib.pylab as plt

    r = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 20')
    r.setIntegrator('gillespie')
    r.integrator.seed = '1234'
    kValues = np.linspace(0.1, 0.9, num=9) # generate k1 values

    plt.gcf().set_size_inches(10, 10) # size of figure
    plt.subplots_adjust(wspace=0.4, hspace=0.4) # adjust the space between subplots
    plt.suptitle('Variation in k1 value', fontsize=16) # main title

    for i in range(1, len(kValues) + 1):
        r.k1 = kValues[i - 1]
        # designates number of subplots (row, col) and spot to plot next
        plt.subplot(3, 3, i)  
        for j in range(1, 30):
            r.reset()
            s = r.simulate(0, 10)
            t = "k1 = " + '{:.1f}'.format(kValues[i - 1])
            # plot each subplot, use show=False to save multiple traces
            te.plotArray(s, show=False, title=t, xlabel='Time', 
                         ylabel='Concentration', alpha=0.7)

.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_1_0.png

External Plotting
~~~~~~~~~~~~~~~~~

For those more familiar with plotting in Python, other libraries such as ``matplotlib.pylab``
offer a wider range of plotting options. To use these external libraries, extract the simulation
timecourse data returned from ``r.simulate``. Data is returned in the form of a dictionary/NamedArray,
so specific elements can easily be extracted using the species name as the key.

.. code-block:: python

        import tellurium as te
        import matplotlib.pylab as plt

        antimonyString = ('''
        model feedback()
        // Reactions:
        J0: Nan1 + Mol -> Nan1Mol; (K1*Nan1*Mol);
        J1: Nan1Mol -> Nan1 + Mol; (K_1*Nan1Mol); 
        J2: Nan1Mol + Nan2 -> Nan1MolNan2; (K2*Nan1Mol*Nan2)
        J3: Nan1MolNan2 + GeneOff -> GeneOn; (K3*Nan1MolNan2*GeneOff);
        J4: GeneOn -> Nan1MolNan2 + GeneOff; (K_3*GeneOn);

        // Species initializations:
        Nan1 = 0.0001692; Mol = 0.0001692/2; Nan2 = 0.0001692; Nan1Mol = 0;
        Nan1MolNan2 = 0; GeneOff = 5*10^-5; GeneOn = 0;

        // Variable initialization:
        K1 = 6.1*10^5; K_1 = 8*10^-5; K2 = 3.3*10^5; K_2 = 5.7*10^-8;  K3 = 1*10^5; K_3 = 0;
        end''')

        r = te.loada(antimonyString)
        results = r.simulate(0,0.5,1000)
        r.plot()

        plt.figure(figsize=(30,10));
        plt.rc('font', size=30); 

        plt.subplot(1,2,1);
        plt.plot(results['time'], results['[Nan2]'], 'r', results['time'], results['[Nan1MolNan2]'], 'b');
        plt.legend({'Nan2', 'Nan1MolNan2'});

        plt.subplot(1,2,2);
        plt.plot(results['time'], results['[GeneOff]'], 'r', results['time'], results['[GeneOn]'], 'b');
        plt.legend({'GeneOff', 'GeneOn'});



.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_extendedplotting.png

Note that we can extract all the time course data for a specific species such as Nan2 by calling ``results['[Nan2]']``.
The extract brackets [  ] around Nan2 may or may not be required depending on if the units are in terms of
concentration or just a count. To check, simply print out results and you can see the names of each species.

Draw diagram
~~~~~~~~~~~~

This example shows how to draw a network diagram, `requires
graphviz <http://tellurium.readthedocs.io/en/latest/notebooks.html#preliminaries>`__.

.. code-block:: python

    import tellurium as te
     
    
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



.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_6_0.png



.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_6_1.png


Parameter Scans
~~~~~~~~~~~~~~~
To study the consequences of varying a specific parameter value or initial concentration on a simulation,
iteratively adjust the given parameter over a range of values of interest and re-run the simulation.
Using the ``show`` parameter and ``te.show`` we can plot all these simulations on a single figure.

.. code-block:: python

        import tellurium as te
        import roadrunner
        import numpy as np

        r = te.loada("""
             $Xo -> A; k1*Xo;
              A -> B; kf*A - kr*B;
              B -> ; k2*B;
              
              Xo = 5
              k1 = 0.1; k2 = 0.5;
              kf = 0.3; kr = 0.4    
        """)

        for Xo in np.arange(1.0, 10, 1):
            r.reset()
            r.Xo = Xo
            m = r.simulate (0, 50, 100, ['time', 'A'])  
            te.plotArray (m, show=False, labels=['Xo='+str(Xo)], resetColorCycle=False)
        te.show()

.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_parameter_scans.png


Parameter Uncertainty Modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most systems, some parameters are more sensitve to perturbations than others. When studying these systems,
it is important to understand which parameters are highly sensitive, as errors (i.e. measurement error) introduced
to these variables can create drastic differences between experimental and simulated results. To study the
sensitivity of these parameters, we can sweep over a range of values as we did in the parameter scan example above.
These ranges represent our uncertainty in the value of the parameter, and those parameters that create highly variable
results in some measure of an output variable are deemed to be sensitive.

.. code-block:: python

        import numpy as np
        import tellurium as te
        import roadrunner
        import antimony
        import matplotlib.pyplot as plt
        import math
        
        antimonyString = ('''
        model feedback()
          // Reactions:
          J0: Nan1 + Mol -> Nan1Mol; (K1*Nan1*Mol);
          J1: Nan1Mol -> Nan1 + Mol; (K_1*Nan1Mol); 
          J2: Nan1Mol + Nan2 -> Nan1MolNan2; (K2*Nan1Mol*Nan2)
          J3: Nan1MolNan2 + GeneOff -> GeneOn; (K3*Nan1MolNan2*GeneOff);
          J4: GeneOn -> Nan1MolNan2 + GeneOff; (K_3*GeneOn);

          // Species initializations:
          Nan1 = 0.0001692; Mol = 0.0001692/2; Nan2 = 0.0001692; Nan1Mol = 0;
          Nan1MolNan2 = 0; GeneOff = 5*10^-5; GeneOn = 0;

          // Variable initialization:
          K1 = 6.1*10^5; K_1 = 8*10^-5; K2 = 3.3*10^5; K_2 = 5.7*10^-8;  K3 = 1*10^5; K_3 = 0;
        end''')

        r = te.loada (model.antimonyString)

        def plot_param_uncertainty(model, startVal, name, num_sims):
            stdDev = 0.6
            
            # assumes initial parameter estimate as mean and iterates 60% above and below.
            vals = np.linspace((1-stdDev)*startVal, (1+stdDev)*startVal, 100)
            for val in vals:
                r.resetToOrigin()
                exec("r.%s = %f" % (name, val))
                result = r.simulate(0,0.5,1000, selections = ['time', 'GeneOn'])
                plt.plot(result[:,0],result[:,1])
                plt.title("uncertainty in " + name)
            plt.legend(["GeneOn"])
            plt.xlabel("Time (hours)")
            plt.ylabel("Concentration")

        startVals = r.getGlobalParameterValues();
        names = list(enumerate([x for x in r.getGlobalParameterIds() if ("K" in x or "k" in x)]));

        n = len(names) + 1;
        dim = math.ceil(math.sqrt(n))
        for i,next_param in enumerate(names):
            plt.subplot(dim,dim,i+1)
            plot_param_uncertainty(r, startVals[next_param[0]], next_param[1], 100)

        plt.tight_layout()
        plt.show()

.. image:: _notebooks/core/tellurium_plotting_files/tellurium_plotting_parameter_uncertainty.png

In the above code, the ``exec`` command is used to set the model parameters to their given value (i.e. ``r.K1 = 1.5``) and
the code sweeps through all the given parameters of interests (names).
Above, we see that the K3 parameter produces the widest distribution of outcomes, and is thus the most sensitive
under the given model, taking into account its assumptions and approximate parameter values. On the other hand, variations in  K_1, K1, and K_3 
seem to have very little effect on the outcome of the system.

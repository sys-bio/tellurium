Perform Parameter Scan
~~~~~~~~~~~~~~~~~~~~~~

``plotPolyArray()`` example

.. code-block:: python

    import tellurium as te
    
    r = te.loada('''
        J1: $Xo -> x; 0.1 + k1*x^4/(k2+x^4);
        x -> $w; k3*x;
    
        k1 = 0.9;
        k2 = 0.3;
        k3 = 0.7;
        x = 0;
    ''')
    
    # parameter scan
    p = te.ParameterScan(r,
        # settings
        startTime = 0,
        endTime = 15,
        numberOfPoints = 50,
        polyNumber = 10,
        endValue = 1.8,
        alpha = 0.8,
        value = "x",
        selection = "x",
        color = ['#0F0F3D', '#141452', '#1A1A66', '#1F1F7A', '#24248F', '#2929A3',
                   '#2E2EB8', '#3333CC', '#4747D1', '#5C5CD6']                    
    )
    # plot
    p.plotPolyArray()


.. image:: _notebooks/core/parameter_scan_files/parameter_scan_2_0.png

``plotSurface()`` example

.. code-block:: python

    r = te.loada('''
        $Xo -> S1; vo;
        S1 -> S2; k1*S1 - k2*S2;
        S2 -> $X1; k3*S2;
        
        vo = 1
        k1 = 2; k2 = 0; k3 = 3;
    ''')
    
    # parameter scan
    p = te.ParameterScan(r,
        # settings
        startTime = 0,
        endTime = 6,
        numberOfPoints = 50,
        startValue = 1,
        endValue = 5,
        colormap = "cool",
        independent = ["Time", "k1"],
        dependent = "S1",
        xlabel = "Time",
        ylabel = "x",
        title = "Model"                                  
    )
    # plot
    p.plotSurface()

.. image:: _notebooks/core/parameter_scan_files/parameter_scan_3_0.png


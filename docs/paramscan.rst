==============
Parameter Scan
==============

teParameterScan is a package for Tellurium that provides a different way to run simulations and plot graphs than given in the standard Tellurium library. While the standard syntax in Tellurium asks you to put parameters, such as the amount of time for the simulation to run, as arguments in the simulation function, teParameterScan allows you to set these values before calling the function. This is especially useful for more complicated 3D plots that often take many arguments to customize. Therefore, teParameterScan also provides several plotting options that would be cumbersome to handle using the traditional approach. This tutorial will go over how to use all of teParameterScan’s functionality. Additionally, there are examples which you can run and edit in Tellurium. They can be found in `examples/tellurium-files/parameterScan <https://github.com/sys-bio/tellurium/tree/master/examples/tellurium-files/parameterscan>`_.

Loading a Model
===============

To use teParameterScan you will need to import it. The easiest way to do this is the command ‘from tellurium import ParameterScan’ after the standard ‘import tellurium as te’.

.. code-block:: python

    import tellurium as te
    from tellurium import ParameterScan as ps

    cell = '''
        $Xo -> S1; vo;
        S1 -> S2; k1*S1 - k2*S2;
        S2 -> $X1; k3*S2;

        vo = 1
        k1 = 2; k2 = 0; k3 = 3;
    '''

    rr = te.loadAntimonyModel(cell)
    p = ps.ParameterScan(rr)

    p.startTime = 0
    p.endTime = 20
    p.numberOfPoints = 50
    p.width = 2
    p.xlabel = 'Time'
    p.ylabel = 'Concentration'
    p.title = 'Cell'

    p.plotArray()

After you load the model, you can use it to create an object of ParameterScan. This allows you to set many different parameters and easily change them.

Methods
=======

``plotArray()``

The plotArray() method works much the same as te.plotArray(), but with some increased functionality. It automatically runs a simulation based on the given parameters, and plots a graph of the results. Accepted parameters are startTime, endTime, numberOfPoints, width, color, xlabel, ylabel, title, integrator, and selection.

``plotGraduatedArray()``

This method runs several simulations, each one with a slightly higher starting concentration of a chosen species than the last. It then plots the results. Accepted parameters are startTime, endTime, value, startValue, endValue, numberOfPoints, width, color, xlabel, ylabel, title, integrator, and polyNumber.

``plotPolyArray()``

This method runs the same simulation as plotGraduatedArray(), but plots each graph as a polygon in 3D space. Accepted parameters are startTime, endTime, value, startValue, endValue, numberOfPoints, color, alpha, xlabel, ylabel, title, integrator, and polyNumber.

``plotMultiArray(param1, param1Range, param2, param2Range)``

This method plots a grid of arrays with different starting conditions. It is the only method in teParameterScan that takes arguments when it is called. The two param arguments specify the species or constant that should be set, and the range arguments give the different values that should be simulated with. The resulting grid is an array for each possible combination of the two ranges. For instance, plotMultiArray(‘k1’, [1, 2], ‘k2’, [1, 2, 3]) would result in a grid of six arrays, one with k1 = 1 and k2 = 1, the next with k1 = 1 and k2 = 2, and so on. The advantage of this method is that you can plot multiple species in each array. Accepted parameters are startTime, endTime, numberOfPoints, width, title, and integrator.

``plotSurface()``

This method produces a color-coded 3D surface based on the concentration of one species and the variation of two factors (usually time and an equilibrium constant). Accepted parameters are startTime, endTime, numberOfPoints, startValue, endValue, independent, dependent, color, xlabel, ylabel, title, integrator, colormap, colorbar, and antialias.

``createColormap(color1, color2)``

This method allows you to create a custom colormap for plotSurface(). It returns a colormap that stretches between color1 and color2. Colors can be input as RGB tuplet lists (i.e. [0.5, 0, 1]), or as strings with either a standard color name or a hex value. The first color becomes bottom of the colormap (i.e. lowest values in plotArray()) and the second becomes the top.

``createColorPoints()``

This method creates a color list (i.e. sets ‘color’) spanning the range of a colormap. The colormap can either be predefined or user-defined with createColorMap(). This set of colors will then be applied to arrays, including plotArray(), plotPolyArray(), and plotGraduatedArray(). Note: This method gets the number of colors to generate from the polyNumber parameter. If using it with plotArray() or plotGraduatedArray(), setting this parameter to the number of graphs you are expecting will obtain better results.

Example
=======

TODO: use notebook

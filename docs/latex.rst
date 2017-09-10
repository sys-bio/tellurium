======================
LaTeX Export
======================

This functionality allows you to export your results and graph to LaTex sources. An example script can be found in `examples/tellurium-files/export/latex_export.py <https://github.com/sys-bio/tellurium/tree/master/examples/tellurium-files/export>`_.

You will need to import LatexExport first, by typing ‘from tellurium import LatexExport’. To use LatexExport, you need to already have a model and simulation results.

.. code-block:: python

    import tellurium as te
    from tellurium import LatexExport

    cell = '''
        $Xo -> S1; vo;
        S1 -> S2; k1*S1 - k2*S2;
        S2 -> $X1; k3*S2;

        vo = 1
        k1 = 2; k2 = 0; k3 = 3;
    '''

    rr = te.loadAntimonyModel(cell)
    result = rr.simulate(0, 6, 100, ['Time', 'S1', 'S2'])
    rr.plot(result)

    p = LatexExport(rr)
    p.color = ['blue', 'green']
    p.legend = ['S1', 'S2']
    p.xlabel = 'Time'
    p.ylabel = 'Concentration'
    p.exportComplete = True
    p.exportClipboard = True
    p.saveto = 'C:\\Users\\user\\Documents\\LaTeXdocs'
    p.saveToFile(result)

Methods
-------

``saveToFile(result)``

Creates a minimum of two .txt files: one contains code to be pasted into a LaTeX document, and the other has the actual coordinates for the simulation results. If more than one graph is plotted, there will be an additional ‘data’ file for every extra graph. For instance, a model with two species in the results will produce three different .txt files, and save them to the location specified in ‘location’. The filenames are ‘filename’ with _code, _data1, _data2, etc. and .txt appended. Note: LaTeX will only be able to import the data files if they are located in the library with the LaTeX project.

``saveToOneFile(result)``

Creates one .txt file that contains the data nested within the LaTeX model. Note that this can get pretty lengthy, especially if you specify a large number of points and/or multiple graphs. Nothing will be appended to the file name.

Parameters
----------

``color``: Use a list of legal HTML color names. Pyplot line styles are not accepted. If there are more graphs than colors provided, the exporter will loop back to the beginning.

``coorPerRow``: For saveToOneFile(), this determines the number of coordinate pairs printed in each line of code. A larger number means less lines of code but could become awkwardly wide. Default is 6.

``exportComplete``: If set to True, this will add all the code necessary to make a complete LaTeX document. This should be used if you want to print out the graph right away, or are starting with a blank document. Default is False.

``exportType``: A placeholder for when additional functionality is added.

``legend``: A list of species to be included in the graph’s legend. Default is no legend.

``saveto``: Set to a string with the location of where you want the .txt files with code and/or data to be saved. Default is wherever Python thinks they should be.

``xlabel``: The title for the x-axis. Should be a string. Default is ‘x’.

``ylabel``: The title for the y-axis. Should be a string. Default is ‘y’.

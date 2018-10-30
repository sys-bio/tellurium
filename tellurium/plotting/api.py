from __future__ import print_function, division, absolute_import

# _plot_index = 0
def plot(x, y, show=True, **kwargs):
    """ Create a 2D scatter plot.

    :param x: A numpy array describing the X datapoints. Should have the same number of rows as y.
    :param y: A numpy array describing the Y datapoints. Should have the same number of rows as x.
    :param tag: A tag so that all traces of the same type are plotted using same color/label (for e.g. multiple stochastic traces).
    :param tags: Like tag, but for multiple traces.
    :param name: The name of the trace.
    :param label: The name of the trace.
    :param names: Like name, but for multiple traces to appear in the legend.
    :param labels: The name of the trace.
    :param alpha: Floating point representing the opacity ranging from 0 (transparent) to 1 (opaque).
    :param show: show=True (default) shows the plot, use show=False to plot multiple simulations in one plot
    :param showlegend: Whether to show the legend or not.
    :param mode: Can be set to 'markers' to generate scatter plots, or 'dash' for dashed lines.
    ::

        import numpy as np, tellurium as te
        result = np.array([[1,2,3,4], [7.2,6.5,8.8,10.5], [9.8, 6.5, 4.3,3.0]])
        te.plot(result[:,0], result[:,1], name='Second column', show=False)
        te.plot(result[:,0], result[:,2], name='Third column', show=False)
        te.show(reset=False) # does not reset the plot after showing plot
        te.plot(result[:,0], result[:,3], name='Fourth column', show=False)
        te.show()
    """
    from .. import getPlottingEngine
    # global _plot_index
    return getPlottingEngine().plot(x, y, show=show, **kwargs)

def plot_text(x, y, text, show=True, **kwargs):
    from .. import getPlottingEngine
    from numpy import array
    if len(x.shape) < 1:
        x = array([x])
    if len(y.shape) < 1:
        y = array([y])
    if not isinstance(text, list):
        text = [text]
    return getPlottingEngine().plot_text(x, y, text=text, show=show, **kwargs)

def show(reset=True):
    from .. import getPlottingEngine
    return getPlottingEngine().show(reset=reset)

def nextFigure(*args, **kwargs):
    from .. import getPlottingEngine
    if nextFigure.tiledFigure is not None:
        fig = nextFigure.tiledFigure.nextFigure(*args, **kwargs)
        #if nextFigure.tiledFigure.isExhausted():
            #nextFigure.tiledFigure = None
        return fig
    else:
        return getPlottingEngine().newFigure(*args, **kwargs)
nextFigure.tiledFigure = None

def newTiledFigure(*args, **kwargs):
    from .. import getPlottingEngine
    nextFigure.tiledFigure = getPlottingEngine().newTiledFigure(*args, **kwargs)
    return nextFigure.tiledFigure

def newLowerTriFigure(*args, **kwargs):
    from .. import getPlottingEngine
    nextFigure.tiledFigure = getPlottingEngine().newLowerTriFigure(*args, **kwargs)
    return nextFigure.tiledFigure

def tiledFigure():
    return nextFigure.tiledFigure

def clearTiledFigure():
    nextFigure.tiledFigure = None
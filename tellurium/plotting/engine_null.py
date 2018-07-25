"""
Plotly implementation of the plotting engine.
"""
from __future__ import print_function, absolute_import

from .engine import PlottingEngine, PlottingFigure, PlottingLayout, filterWithSelections, TiledFigure, LowerTriFigure


class NullEngine(PlottingEngine):
    """ PlottingEngine using plotly. """

    def __init__(self):
        PlottingEngine.__init__(self)

    def __str__(self):
        return "<NullEngine>"

    def newFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout(), xtitle=None, ytitle=None):
        """ Returns a figure object."""
        return NullFigure(title=title, layout=layout, xtitle=xtitle, ytitle=ytitle)

    def newTiledFigure(self, title=None, rows=None, cols=None):
        return NullTiledFigure(engine=self, rows=rows, cols=cols)

    def newLowerTriFigure(self, title=None, rows=None, cols=None):
        return NullLowerTriFigure(engine=self, rows=rows, cols=cols)


class NullFigure(PlottingFigure):
    """ PlotlyFigure. """

    def __init__(self, title=None, layout=PlottingLayout(), logx=False, logy=False, save_to_pdf=False, xtitle=None, ytitle=None):
        super(NullFigure, self).__init__(title=title, layout=layout, logx=logx, xtitle=xtitle, logy=logy, ytitle=ytitle)

    def render(self):
        pass

    def save(self, filename, format):
        # FIXME: implement
        raise NotImplementedError



class PlotlyTiledFigure(TiledFigure):
    def __init__(self, engine, rows, cols):
        pass

    def nextFigure(self, *args, **kwargs):
        pass

    def renderIfExhausted(self):
        pass

class PlotlyLowerTriFigure(PlotlyTiledFigure,LowerTriFigure):
    def makeTitles(self):
        pass

    def renderIfExhausted(self):
        pass

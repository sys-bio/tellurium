"""
Plotly implementation of the plotting engine.
"""
from __future__ import print_function, absolute_import

from .engine import PlottingEngine, PlottingFigure, PlottingLayout, filterWithSelections, TiledFigure, LowerTriFigure
import numpy as np
import plotly
from plotly.graph_objs import Scatter, Scatter3d, Layout, Data
from plotly import tools


class PlotlyEngine(PlottingEngine):
    """ PlottingEngine using plotly. """

    def __init__(self):
        PlottingEngine.__init__(self)

    def __str__(self):
        return "<PlotlyEngine>"

    def newFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout(), xtitle=None, ytitle=None):
        """ Returns a figure object."""
        return PlotlyFigure(title=title, layout=layout, xtitle=xtitle, ytitle=ytitle)

    def newStackedFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout()):
        """ Returns a figure object."""
        return PlotlyStackedFigure(title=title, layout=layout)

    def newTiledFigure(self, title=None, rows=None, cols=None):
        return PlotlyTiledFigure(engine=self, rows=rows, cols=cols)

    def newLowerTriFigure(self, title=None, rows=None, cols=None):
        return PlotlyLowerTriFigure(engine=self, rows=rows, cols=cols)


class PlotlyFigure(PlottingFigure):
    """ PlotlyFigure. """

    def __init__(self, title=None, layout=PlottingLayout(), logx=False, logy=False, save_to_pdf=False, xtitle=None, ytitle=None):
        super(PlotlyFigure, self).__init__(title=title, layout=layout, logx=logx, xtitle=xtitle, logy=logy, ytitle=ytitle)

    def getArgsForDataset(self, dataset):
        kwargs = {}
        if 'name' in dataset and dataset['name'] is not None:
            kwargs['name'] = dataset['name']
        else:
            kwargs['showlegend'] = False
        if 'alpha' in dataset and dataset['alpha'] is not None:
            kwargs['opacity'] = dataset['alpha']
        # lines/markers (lines by default)
        if 'mode' in dataset and dataset['mode'] is not None:
            kwargs['mode'] = dataset['mode']
        else:
            kwargs['mode'] = 'lines'
        return kwargs

    def getScatterGOs(self):
        for dataset in self.getDatasets():
            yield Scatter(
                x = dataset['x'],
                y = dataset['y'],
                **self.getArgsForDataset(dataset)
            )


    def render(self):
        """ Plot the figure. Call this last."""
        traces = list(self.getScatterGOs())

        data = Data(traces)
        plotly.offline.iplot({
            'data': data,
            'layout': self.makeLayout()
        })

    def save(self, filename, format):
        # FIXME: implement
        raise NotImplementedError

    def makeLayout(self):
        kwargs = {}
        if self.title is not None:
            kwargs['title'] = self.title
        if self.logx:
            kwargs['xaxis'] = {
                'type': 'log',
                'autorange': True,
            }
        if self.xtitle:
            if not 'xaxis' in kwargs:
                kwargs['xaxis'] = {}
            kwargs['xaxis']['title'] = self.xtitle
        if self.logy:
            kwargs['yaxis'] = {
                'type': 'log',
                'autorange': True,
            }
        if self.ytitle:
            if not 'yaxis' in kwargs:
                kwargs['yaxis'] = {}
            kwargs['yaxis']['title'] = self.ytitle
        if not self.grid_enabled:
            kwargs['xaxis']['showgrid'] = False
            kwargs['xaxis']['showline'] = False
            kwargs['yaxis']['showgrid'] = False
            kwargs['yaxis']['showline'] = False
        return Layout(**kwargs)


class PlotlyStackedFigure(PlotlyFigure):
    """ Stacked figure."""
    def __init__(self, title=None, layout=PlottingLayout(), logx=False, logy=False):
        super(PlotlyStackedFigure, self).__init__(title=title, layout=layout, logx=logx, logy=logy)
        self.zindex = 0

    def render(self):
        """ Plot the figure. Call this last."""
        traces = []
        for dataset in self.xy_datasets:
            kwargs = {}
            if 'name' in dataset and dataset['name'] is not None:
                kwargs['name'] = dataset['name']
                self.zindex = kwargs['name']
            else:
                kwargs['showlegend'] = False
            zvals = np.full(np.size(dataset['x']), self.zindex)
            traces.append(Scatter3d(
                x = dataset['x'],
                z = dataset['y'],
                y = zvals,
                mode = 'lines',
                **kwargs
            ))
            if not isinstance(self.zindex, str):
                self.zindex += 1

        data = Data(traces)
        plotly.offline.iplot({
            'data': data,
            'layout': self.makeLayout()
        })



class PlotlyTiledFigure(TiledFigure):
    def __init__(self, engine, rows, cols):
        self.rows = rows
        self.rowmarker = 0
        self.cols = cols
        self.colmarker = 0
        self.engine = engine
        #self.fig = None
        self.figures = []

    def nextFigure(self, *args, **kwargs):
        self.cycleMarker()
        fig = self.engine.newFigure(*args, **kwargs)
        self.figures.append(fig)
        return fig

    def renderIfExhausted(self):
        if not self.isExhausted():
            return
        fig = tools.make_subplots(self.rows, self.cols, subplot_titles=tuple(f.title for f in self.figures), print_grid=False)
        row = 1
        col = 1
        n = 1
        for f in self.figures:
            for trace in f.getScatterGOs():
                fig.append_trace(trace, row, col)
            if f.logx:
                fig['layout']['xaxis'+str(n)]['type'] = 'log'
                fig['layout']['xaxis'+str(n)]['autorange'] = True
            if f.logy:
                fig['layout']['yaxis'+str(n)]['type'] = 'log'
                fig['layout']['yaxis'+str(n)]['autorange'] = True
            col += 1
            n += 1
            if col > self.cols:
                col = 1
                row += 1
                if row > self.rows:
                    row = self.rows
        plotly.offline.iplot(fig)

class PlotlyLowerTriFigure(PlotlyTiledFigure,LowerTriFigure):
    def makeTitles(self):
        row = 1
        col = 1
        for f in self.figures:
            yield f.title
            col += 1
            if col > row:
                while col <= self.cols:
                    col += 1
                    yield ''
                col = 1
                row += 1
                if row > self.rows:
                    return;

    def renderIfExhausted(self):
        if not self.isExhausted():
            return
        fig = tools.make_subplots(self.rows, self.cols, subplot_titles=tuple(self.makeTitles()), print_grid=False)
        row = 1
        col = 1
        n = 1
        for f in self.figures:
            for trace in f.getScatterGOs():
                fig.append_trace(trace, row, col)
            col += 1
            n += 1
            if col > row:
                while col <= self.cols:
                    for key in ('xaxis'+str(n), 'yaxis'+str(n)):
                        fig['layout'][key]['showgrid'] = False
                        fig['layout'][key]['showline'] = False
                        fig['layout'][key]['showticklabels'] = False
                        fig['layout'][key]['ticks'] = ''
                        fig['layout'][key]['zeroline'] = False
                    n+=1
                    col+=1
                col = 1
                row += 1
                if row > self.rows:
                    row = self.rows
        plotly.offline.iplot(fig)

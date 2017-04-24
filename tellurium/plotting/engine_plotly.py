from .engine import PlottingEngine, PlottingFigure, PlottingLayout
import plotly
from plotly.graph_objs import Scatter, Scatter3d, Layout, Data
import numpy as np

class PlotlyFigure(PlottingFigure):
    def __init__(self, title=None, layout=PlottingLayout(), logx=False, logy=False, save_to_pdf=False):
        self.initialize(title=title, layout=layout, logx=logx, logy=logy)

    def makeLayout(self):
        kwargs = {}
        if self.title is not None:
            kwargs['title'] = self.title
        if self.logx:
            kwargs['xaxis'] = {
                type: 'log',
                autorange: True,
            }
        if self.logy:
            kwargs['yaxis'] = {
                type: 'log',
                autorange: True,
            }
        return Layout(**kwargs)

    def plot(self):
        """ Plot the figure. Call this last."""
        traces = []
        for dataset in self.xy_datasets:
            kwargs = {}
            if 'name' in dataset and dataset['name'] is not None:
                kwargs['name'] = dataset['name']
            else:
                kwargs['showlegend'] = False
            traces.append(Scatter(
                x = dataset['x'],
                y = dataset['y'],
                mode = 'lines',
                **kwargs
            ))

        data = Data(traces)
        plotly.offline.iplot({
            'data': data,
            'layout': self.makeLayout()
        })

class PlotlyStackedFigure(PlotlyFigure):
    def __init__(self, title=None, layout=PlottingLayout(), logx=False, logy=False):
        self.initialize(title=title, layout=layout, logx=logx, logy=logy)
        self.zindex = 0

    def plot(self):
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

class PlotlyPlottingEngine(PlottingEngine):
    def __init__(self, save_to_pdf=False):
        pass

    def newFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout()):
        """ Returns a figure object."""
        return PlotlyFigure(title=title, layout=layout)

    def newStackedFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout()):
        """ Returns a figure object."""
        return PlotlyStackedFigure(title=title, layout=layout)

    def figureFromTimecourse(self, m, title=None, ordinates=None):
        """ Generate a new figure from a timecourse simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.newFigure()
        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in filter(lambda k: self.filterWithSelections(m.colnames[k], ordinates), range(1,m.shape[1])):
            fig.addXYDataset(m[:,0], m[:,k], name=m.colnames[k])

        return fig

    def plotTimecourse(self, m, title=None, ordinates=None):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.figureFromTimecourse(m, title=title, ordinates=ordinates)
        fig.plot()

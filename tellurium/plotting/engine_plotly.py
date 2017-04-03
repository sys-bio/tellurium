from .engine import PlottingEngine, PlottingFigure, PlottingLayout
import plotly
from plotly.graph_objs import Scatter, Layout, Data

class PlotlyFigure(PlottingFigure):
    def __init__(self, title=None, layout=PlottingLayout()):
        self.initialize(title=title, layout=layout)

    def makeLayout(self):
        kwargs = {}
        if self.title is not None:
            kwargs['title'] = self.title
        return Layout(**kwargs)

    def plot(self):
        """ Plot the figure. Call this last."""
        traces = []
        for dataset in self.xy_datasets:
            kwargs = {}
            if 'name' in dataset:
                kwargs['name'] = dataset['name']
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

class PlotlyPlottingEngine(PlottingEngine):
    def newFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout()):
        """ Returns a figure object."""
        return PlotlyFigure(title=title, layout=layout)

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

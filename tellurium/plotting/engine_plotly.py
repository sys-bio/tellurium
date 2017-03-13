from .engine import PlottingEngine, PlottingFigure, PlottingLayout
import plotly
from plotly.graph_objs import Scatter, Layout, Data

plotly.offline.init_notebook_mode(connected=True)

plotly.offline.iplot({
    "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1], mode = 'lines')],
    "layout": Layout(title="hello world")
})

class PlotlyFigure(PlottingFigure):
    def __init__(self, layout=PlottingLayout()):
        self.xy_datasets = []

    def addXYDataset(self, x_arr, y_arr):
        """ Adds an X/Y dataset to the plot.

        :param x_arr: A numpy array describing the X datapoints. Should have the same size as y_arr.
        :param y_arr: A numpy array describing the Y datapoints. Should have the same size as x_arr.
        """
        self.xy_datasets.append((x_arr, y_arr))

    def makeLayout(self):
        return Layout(title="Figure")

    def plot(self):
        traces = []
        for dataset in self.xy_datasets:
            traces.append(Scatter(
                x = dataset[0],
                y = dataset[1],
            ))

        data = Data(traces)
        plotly.offline.iplot({
            'data': data,
            'layout': self.makeLayout()
        })

class PlotlyPlottingEngine(PlottingEngine):
    def newFigure(self, layout=PlottingLayout()):
        """ Returns a figure object."""
        return PlotlyFigure(layout)

    def figureFromTimecourse(self, m):
        """ Generate a new figure from a timecourse simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.newFigure()
        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in range(1,m.shape[1]):
            fig.addXYDataset(m[:,0], m[:,k])

        return fig

    def plotTimecourse(self, m):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.figureFromTimecourse(m)
        fig.plot()

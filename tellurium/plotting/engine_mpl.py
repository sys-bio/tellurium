from .engine import PlottingEngine, PlottingFigure, PlottingLayout

import matplotlib.pyplot as plt
from matplotlib import gridspec

class MatplotlibFigure(PlottingFigure):
    def __init__(self, title=None, layout=PlottingLayout):
        self.initialize(title=title, layout=layout)

    def plot(self):
        """ Plot the figure. Call this last."""
        __gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        fig = plt.figure(num=None, figsize=(9,5), dpi=80, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(__gs[0])
        for dataset in self.xy_datasets:
            ax.plot(dataset['x'], dataset['y'], marker='')
        # fig.show()

class MatplotlibPlottingEngine(PlottingEngine):
    def newFigure(self, title=None, layout=PlottingLayout()):
        """ Returns a figure object."""
        return MatplotlibFigure(title=title, layout=layout)

    def figureFromTimecourse(self, m, title=None):
        """ Generate a new figure from a timecourse simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.newFigure()
        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in range(1,m.shape[1]):
            fig.addXYDataset(m[:,0], m[:,k], name=m.colnames[k])

        return fig

    def plotTimecourse(self, m, title=None):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.figureFromTimecourse(m, title=title)
        fig.plot()

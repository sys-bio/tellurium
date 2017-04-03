from .engine import PlottingEngine, PlottingFigure, PlottingLayout

import matplotlib.pyplot as plt
from matplotlib import gridspec

class MatplotlibFigure(PlottingFigure):
    def __init__(self, title=None, layout=PlottingLayout, use_legend=True, figsize=(9,5)):
        self.initialize(title=title, layout=layout)
        self.use_legend = use_legend
        self.figsize = figsize

    def plot(self):
        """ Plot the figure. Call this last."""
        fig = plt.figure(num=None, figsize=self.figsize, dpi=80, facecolor='w', edgecolor='k')
        __gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        plt.subplot(__gs[0])

        have_labels = False
        for dataset in self.xy_datasets:
            kwargs = {}
            if 'name' in dataset:
                kwargs['label'] = dataset['name']
                have_labels = True
            plt.plot(dataset['x'], dataset['y'], marker='', **kwargs)
        # title
        if self.title:
            plt.title(self.title, fontweight='bold')
        # legend
        if self.use_legend and have_labels:
            legend = plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=5.)
            legend.draw_frame(False)
        plt.savefig('/Users/phantom/plot.pdf', format='pdf')

        return fig

    def save(self, filename, format):
        fig = self.plot()
        fig.savefig(filename, format=format)

class MatplotlibPlottingEngine(PlottingEngine):
    def newFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout()):
        """ Returns a figure object."""
        return MatplotlibFigure(title=title, layout=layout)

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

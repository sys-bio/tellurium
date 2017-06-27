from __future__ import print_function, absolute_import

from .engine import PlottingEngine, PlottingFigure, PlottingLayout, filterWithSelections

import matplotlib.pyplot as plt
from matplotlib import gridspec
from tempfile import mkstemp

class MatplotlibFigure(PlottingFigure):
    def __init__(self, title=None, layout=PlottingLayout, use_legend=True, figsize=(9,5), save_to_pdf=False):
        self.initialize(title=title, layout=layout)
        self.use_legend = use_legend
        self.figsize = figsize
        self.save_to_pdf = save_to_pdf

    def plot(self):
        """ Plot the figure. Call this last."""
        fig = plt.figure(num=None, figsize=self.figsize, dpi=80, facecolor='w', edgecolor='k')
        __gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        plt.subplot(__gs[0])

        have_labels = False
        for dataset in self.getDatasets():
            kwargs = {}
            if 'name' in dataset:
                kwargs['label'] = dataset['name']
                have_labels = True
            if 'color' in dataset:
                kwargs['color'] = dataset['color']
            if 'alpha' in dataset and dataset['alpha'] is not None:
                kwargs['alpha'] = dataset['alpha']
            plt.plot(dataset['x'], dataset['y'], marker='', **kwargs)
        # title
        if self.title:
            plt.title(self.title, fontweight='bold')
        # legend
        if self.use_legend and have_labels:
            legend = plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=5.)
            legend.draw_frame(False)

        if self.save_to_pdf:
            (dummy,filename) = mkstemp(suffix='.pdf')
            plt.savefig(filename, format='pdf')
            print('saved plot to {}'.format(filename))

        return fig

    def save(self, filename, format):
        fig = self.plot()
        fig.savefig(filename, format=format)

class MatplotlibPlottingEngine(PlottingEngine):
    def __init__(self, save_to_pdf=False):
        PlottingEngine.__init__(self)
        self.save_to_pdf = save_to_pdf

    def newFigure(self, title=None, logX=False, logY=False, layout=PlottingLayout()):
        """ Returns a figure object."""
        return MatplotlibFigure(title=title, layout=layout, save_to_pdf=self.save_to_pdf)

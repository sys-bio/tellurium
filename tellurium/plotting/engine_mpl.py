"""
Matplotlib implementation of the plotting engine.
"""
from __future__ import print_function, division, absolute_import


from .engine import PlottingEngine, PlottingFigure, PlottingLayout, filterWithSelections

import os
import matplotlib.pyplot as plt
from matplotlib import gridspec
from tempfile import mkstemp

if any('SPYDER' in name for name in os.environ):
    SPYDER = True
else:        
    SPYDER = False
    

class MatplotlibFigure(PlottingFigure):
    """ MatplotlibFigure. """
    def __init__(self, title=None, layout=PlottingLayout, use_legend=True, figsize=(9,5), save_to_pdf=False):
        self.initialize(title=title, layout=layout)
        self.use_legend = use_legend
        if not SPYDER:
            self.figsize = figsize
        self.save_to_pdf = save_to_pdf

    def render(self):
        """ Plot the figure. Call this last."""
        if SPYDER:
            fig = plt.figure(num=None, facecolor='w', edgecolor='k')
        else:        
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
            scatter = False
            if 'mode' in dataset and dataset['mode'] is not None and dataset['mode'] == 'markers':
                scatter = True
            if not scatter:
                plt.plot(dataset['x'], dataset['y'], marker='', **kwargs)
            else:
                plt.scatter(dataset['x'], dataset['y'], **kwargs)
        # title
        if self.title:
            plt.title(self.title, fontweight='bold')
        # xtitle
        if self.xtitle:
            plt.xlabel(self.xtitle)
        # ytitle
        if self.ytitle:
            plt.ylabel(self.ytitle)
        # xlim
        if self.xlim:
            plt.xlim(self.xlim)
        # ylim
        if self.ylim:
            plt.ylim(self.ylim)
        # logx
        if self.logx:
            plt.xscale('log')
        # logy
        if self.logy:
            plt.yscale('log')
        # legend
        if self.use_legend and have_labels:
            if SPYDER:
                legend = plt.legend()
            else:
                legend = plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=5.)
            legend.draw_frame(False)

        if self.save_to_pdf:
            (dummy,filename) = mkstemp(suffix='.pdf')
            plt.savefig(filename, format='pdf')
            print('saved plot to {}'.format(filename))
        
        plt.show()

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

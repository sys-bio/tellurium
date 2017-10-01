"""
Matplotlib implementation of the plotting engine.
"""
from __future__ import absolute_import, print_function, division


from .engine import PlottingEngine, PlottingFigure, PlottingLayout

import os
import matplotlib.pyplot as plt
from matplotlib import gridspec
from tempfile import mkstemp

# Check if in spyder environment
SPYDER = False
if any('SPYDER' in name for name in os.environ):
    SPYDER = True


class MatplotlibEngine(PlottingEngine):
    """ Matplotlib engine."""

    def __init__(self):
        super(MatplotlibEngine, self).__init__()

    def __str__(self):
        return "<MatplotlibEngine>"

    @classmethod
    def newFigure(cls, title=None, logX=False, logY=False, layout=None, xtitle=None, ytitle=None):
        """ Returns a figure object."""
        if layout is None:
            layout = PlottingLayout()

        fig = MatplotlibFigure(title=title, layout=layout, xtitle=xtitle, ytitle=ytitle, logx=logX, logy=logY)
        return fig


class MatplotlibFigure(PlottingFigure):
    """ MatplotlibFigure. """

    def __init__(self, title=None, layout=PlottingLayout(), use_legend=True, xtitle=None, ytitle=None,
                 logx=None, logy=None,
                 figsize=(9, 5), save_to_pdf=False):
        super(MatplotlibFigure, self).__init__(title=title, layout=layout,
                                               xtitle=xtitle, ytitle=ytitle, logx=logx, logy=logy)
        self.use_legend = use_legend

        # FIXME: ? why this check here?
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
                legend = plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=1.)
            legend.draw_frame(False)

        if self.save_to_pdf:
            (dummy, filename) = mkstemp(suffix='.pdf')
            plt.savefig(filename, format='pdf')
            print('saved plot to {}'.format(filename))
        
        plt.show()

        return fig

    def save(self, filename, format):
        fig = self.render()
        fig.savefig(filename, format=format)

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
                 figsize=(9, 6), save_to_pdf=False):
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
            fig, ax = plt.subplots(num=None, facecolor='w', edgecolor='k')
        else:        
            # fig = plt.figure(num=None, figsize=self.figsize, dpi=80, facecolor='w', edgecolor='k')
            # __gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
            # plt.subplot(__gs[0])
            fig, ax = plt.subplots(num=None, figsize=self.figsize, dpi=80, facecolor='w', edgecolor='k')
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

        # TODO: data as points

        # title & axes labels
        if self.title:
            ax.set_title(self.title, fontweight='bold')
        if self.xtitle:
            ax.set_xlabel(self.xtitle, fontweight='bold')
        if self.ytitle:
            ax.set_ylabel(self.ytitle, fontweight="bold")

        # axes limits
        if self.xlim:
            ax.set_xlim(self.xlim)
        if self.ylim:
            ax.set_ylim(self.ylim)

        # logarithmic axes
        if self.logx:
            ax.set_xscale('log')
        if self.logy:
            ax.set_yscale('log')

        # legend
        if self.use_legend and have_labels:
            if SPYDER:
                legend = plt.legend()
            else:
                # legend = plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=1.)
                # legend = plt.legend(bbox_to_anchor=(0.0, 1.02, 1., .102), ncol=2, loc='best', borderaxespad=0.)
                legend = plt.legend(ncol=1, loc='best', borderaxespad=0.)
            # legend.draw_frame(False)
            legend.draw_frame(True)

        # grid
        ax.grid(linestyle='dotted', alpha=0.8)

        if self.save_to_pdf:
            (dummy, filename) = mkstemp(suffix='.pdf')
            plt.savefig(filename, format='pdf')
            print('saved plot to {}'.format(filename))
        
        plt.show()

        return fig

    def save(self, filename, format):
        fig = self.render()
        fig.savefig(filename, format=format)


# FIXME: integrate old code
# Old code:
# if loc is False:
#     loc = None
#
# if 'linewidth' not in kwargs:
#     kwargs['linewidth'] = 2.0
#
# # get the names
# names = result.dtype.names
# if names is None:
#     names = self.selections
#
# # check if set_prop_cycle is supported
# if hasattr(plt.gca(), 'set_prop_cycle'):
#     # reset color cycle (repeated simulations have the same colors)
#     plt.gca().set_prop_cycle(None)
#
# # make plot
# Ncol = result.shape[1]
# if len(names) != Ncol:
#     raise Exception('Legend names must match result array')
# for k in range(1, Ncol):
#     if loc is None:
#         # no labels if no legend
#         plt.plot(result[:, 0], result[:, k], **kwargs)
#     else:
#         plt.plot(result[:, 0], result[:, k], label=names[k], **kwargs)
#
#     cmap = plt.get_cmap('Blues')
#
# # labels
# if xlabel is None:
#     xlabel = names[0]
# plt.xlabel(xlabel)
# if ylabel is not None:
#     plt.ylabel(ylabel)
# if title is not None:
#     plt.title(title)
# if xlim is not None:
#     plt.xlim(xlim)
# if ylim is not None:
#     plt.ylim(ylim)
# # axis and grids
# plt.xscale(xscale)
# plt.yscale(yscale)
# plt.grid(grid)
#
# # show legend
# if loc is not None:
#     plt.legend(loc=loc)
# # show plot
# if show:
#     plt.show()
# return plt

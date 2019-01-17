"""
Matplotlib implementation of the plotting engine.
"""
from __future__ import absolute_import, print_function, division


from .engine import PlottingEngine, PlottingFigure, PlottingLayout

import os
import matplotlib.pyplot as plt
from matplotlib import gridspec
from tempfile import mkstemp

# enable fixes for non-IPython environment
IPYTHON = False
if any('IPYTHONDIR' in name for name in os.environ):
    IPYTHON = True


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

    def __init__(self, layout=PlottingLayout(), use_legend=True, xtitle=None, ytitle=None, title=None, 
                 linewidth=None, xlim=None, ylim=None, logx=None, logy=None, xscale=None, yscale=None, 
                 grid=None, ordinates=None, tag=None, labels=None, figsize=(9,6), savefig=None, dpi=None):
        super(MatplotlibFigure, self).__init__(title=title, layout=layout,
                                               xtitle=xtitle, ytitle=ytitle, logx=logx, logy=logy)
        self.use_legend = use_legend
        self.linewidth = linewidth
        self.xscale = xscale
        self.yscale = yscale
        self.grid = grid
        self.ordinates = ordinates
        self.tag = tag
        self.labels = labels
        self.figsize = figsize
        self.savefig = savefig
        self.dpi = dpi

    def render(self):
        """ Plot the figure. Call this last."""
        fig, ax = plt.subplots(num=None, figsize=self.figsize, facecolor='w', edgecolor='k')
        have_labels = False
        show_legend = False # override self.use_legend if user called plot with showlegend=True
        for dataset in self.getDatasets():
            kwargs = {}
            if 'name' in dataset:
                kwargs['label'] = dataset['name']
                have_labels = True
            if 'color' in dataset:
                kwargs['color'] = dataset['color']
            if 'alpha' in dataset and dataset['alpha'] is not None:
                kwargs['alpha'] = dataset['alpha']
            if 'showlegend' in dataset and dataset['showlegend'] is not None:
                show_legend = dataset['showlegend']
            if 'color' in dataset and dataset['color'] is not None:
                kwargs['color'] = dataset['color']
            scatter = False
            marker = ''
            if 'mode' in dataset and dataset['mode'] is not None:
                if dataset['mode'] == 'markers':
                    scatter = True
                    marker = ''
            if 'dash' in dataset and dataset['dash'] is not None:
                kwargs['dashes'] = [4,2]
            if  'text' in dataset and dataset['text'] is not None:
                for x,y,t in zip(dataset['x'], dataset['y'], dataset['text']):
                    plt.text(x, y, t, bbox=dict(facecolor='white', alpha=1))
            elif not scatter:
                plt.plot(dataset['x'], dataset['y'], marker=marker, linewidth=self.linewidth, **kwargs)
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

        # axes type
        if self.logx or self.xscale == 'log':
            ax.set_xscale('log')
        elif self.xscale != None:
            ax.set_xscale(self.xscale)
        if self.logy or self.yscale == 'log':
            ax.set_yscale('log')
        elif self.yscale != None:
            ax.set_yscale(self.yscale)
            
        # grid
        if self.grid:
            ax.grid(linestyle='dotted', alpha=0.8)
            
        # TODO: implement ordinates, tags & labels

        # legend
        if (self.use_legend and have_labels) or show_legend:
            if not IPYTHON:
                legend = plt.legend()
            else:
                # legend = plt.legend(bbox_to_anchor=(1.0, 0.5), loc='center left', borderaxespad=1.)
                # legend = plt.legend(bbox_to_anchor=(0.0, 1.02, 1., .102), ncol=2, loc='best', borderaxespad=0.)
                legend = plt.legend(ncol=1, loc='best', borderaxespad=0.)
            # legend.draw_frame(False)
            legend.draw_frame(True)

        # save figure
        if self.savefig:
            plt.savefig(self.savefig, dpi=self.dpi, bbox_inches='tight')
            print('saved plot to {}'.format(self.savefig))

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

from __future__ import print_function, division, absolute_import


from collections import defaultdict
import itertools
import numpy as np
from functools import reduce


def filterWithSelections(self, name, selections):
    """ This function is intended to be used as an argument to the filter built-in.
    It filters out unwanted traces (only those variables specified in selections
    will be passed through).

    :param name: The symbol we want to potentially filter
    :param selections: The list of selections we want to plot
    """
    if selections is not None:
        augmented_sel = selections + list('[{}]'.format(name) for name in selections if not name.startswith('['))
        return name in augmented_sel
    else:
        return True

class PlottingLayout:
    pass

class PlottingFigure(object):
    def initialize(self, title=None, layout=PlottingLayout(), logx=False, xtitle=None, logy=False, ytitle=None, selections=None):
        """ Initialize the figure.

        :param title: The title of the plot.
        :param layout: Plotting layout information.
        :param logx: Use log scale in x.
        :param logy: Use log scale in y.
        :param selections: Filter plotted traces based on passed name.
        """
        self.title = title
        self.xy_datasets = []
        self.tagged_data = defaultdict(list)
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.logx = logx
        self.logy = logy
        self.selections=selections
        self.xlim = None
        self.ylim = None

    def addXYDataset(self, x_arr, y_arr, color=None, tag=None, name=None, filter=True, alpha=None, mode=None):
        """ Adds an X/Y dataset to the plot.

        :param x_arr: A numpy array describing the X datapoints. Should have the same size as y_arr.
        :param y_arr: A numpy array describing the Y datapoints. Should have the same size as x_arr.
        :param color: The color to use (not supported by all backends).
        :param tag: A tag so that all traces of the same type are plotted consistently (for e.g. multiple stochastic traces).
        :param name: The name of the trace.
        :param filter: Apply the self.selections filter?
        :param alpha: Floating point representing the opacity.
        :param mode: Either 'lines' or 'markers' (defaults to 'lines').
        """
        if filter and name is not None and self.selections is not None:
            # if this name is filtered out, return
            if filterWithSelections(name, self.selections):
                return

        dataset = {'x': x_arr, 'y': y_arr}
        if name is not None:
            dataset['name'] = name
        if color is not None:
            dataset['color'] = color
        if tag is not None:
            dataset['tag'] = tag
            self.tagged_data[tag].append(dataset)
        if alpha is not None:
            dataset['alpha'] = alpha
        if mode is not None:
            dataset['mode'] = mode
        self.xy_datasets.append(dataset)

    def getMergedTaggedDatasets(self):
        for datasets_for_tag in self.tagged_data.values():
            x = reduce(lambda u,v: np.concatenate((u,[np.nan],v)), (dataset['x'] for dataset in datasets_for_tag))
            y = reduce(lambda u,v: np.concatenate((u,[np.nan],v)), (dataset['y'] for dataset in datasets_for_tag))
            # merge all datasets
            result_dataset = datasets_for_tag[0] if datasets_for_tag else None
            for dataset in datasets_for_tag:
                result_dataset.update(dataset)
            # use the concatenated values for x and y
            result_dataset['x'] = x
            result_dataset['y'] = y
            if result_dataset is not None:
                yield result_dataset

    def getDatasets(self):
        """ Get an iterable of all datasets."""
        return itertools.chain(
            self.getMergedTaggedDatasets(),
            (dataset for dataset in self.xy_datasets if not 'tag' in dataset))

    # TODO: don't need name/names and tag/tags redundancy
    def plot(self, x, y, colnames=None, title=None, xtitle=None, logy=False, ytitle=None, alpha=None, name=None, names=None, tag=None, tags=None):
        """ Plot x & y data.
        """
        if xtitle:
            self.xtitle = xtitle
        if ytitle:
            self.ytitle = ytitle
        kws = {'alpha': alpha}
        if colnames is None and hasattr(y,'colnames'):
            colnames = y.colnames

        # TODOL if y is 2d array with 1 column, convert to 1d array
        if len(y.shape) > 1:
            # it's a 2d array
            for k in range(0,y.shape[1]):
                if len(x) != len(y[:,k]):
                    raise RuntimeError('x data has length {} but y data has length {}'.format(len(x), len(y)))
                if names is not None:
                    kws['name'] = names[k]
                if tags is not None:
                    kws['tag'] = tags[k]
                if colnames is not None:
                    kws['name'] = colnames[k]
                self.addXYDataset(x, y[:,k], **kws)
        elif len(y.shape) == 1:
            # it's a 1d array
            if len(x) != len(y):
                raise RuntimeError('x data has length {} but y data has length {}'.format(len(x), len(y)))
            if name is not None:
                kws['name'] = name
            if tag is not None:
                kws['tag'] = name
            elif colnames is not None:
                kws['name'] = colnames[0]
            self.addXYDataset(x, y, **kws)
        else:
            raise RuntimeError('Could not plot y data with {} dimensions'.format(len(y.shape)))
        return self

    def setXLim(self, xlim):
        """Set the min/max x limits of the figure.
        :param xlim: tuple of min/max values
        """
        self.xlim = xlim

    def setYLim(self, ylim):
        """Set the min/max y limits of the figure.
        :param ylim: tuple of min/max values
        """
        self.ylim = ylim


class PlottingEngine(object):
    def __init__(self):
        self.fig = None


    def figureFromXY(self, x, y, **kwargs):
        """ Generate a new figure from x/y data.

        :param x: A column representing x data.
        :param y: Y data (may be multiple columns).
        """
        return self.newFigure().plot(x,y,**kwargs)

    def figureFromTimecourse(self, m, ordinates=None, tag=None, alpha=None, title=None, xlim=None, ylim=None):
        """ Generate a new figure from a timecourse simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.newFigure()
        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in range(1,m.shape[1]):
            fig.addXYDataset(m[:,0], m[:,k], name=m.colnames[k], tag=tag, alpha=alpha)

        return fig


    def plot(self, x, y, show=True, **kwargs):
        """ Plot x & y data.

        :param x: x data.
        :param y: y data (can be multiple columns).
        """
        if self.fig:
            fig = self.fig
            fig.plot(x, y, **kwargs)
        else:
            fig = self.figureFromXY(x, y, **kwargs)
        if show:
            fig.render()
            self.fig = None
        else:
            self.fig = fig
        return fig

    def plotTimecourse(self, m, title=None, ordinates=None, tag=None, xtitle=None, logx=False, logy=False, ytitle=None, alpha=None, xlim=None, ylim=None, **kwargs):

        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.figureFromTimecourse(m, title=title, ordinates=ordinates, tag=tag, alpha=alpha, xlim=xlim, ylim=ylim)
        if title:
            fig.title = title
        if xtitle:
            fig.xtitle = xtitle
        if ytitle:
            fig.ytitle = ytitle
        if xlim:
            fig.setXLim(xlim)
        if ylim:
            fig.setYLim(ylim)
        if logx:
            fig.logx = logx
        if logy:
            fig.logy = logy
        fig.render()

    def accumulateTimecourse(self, m, title=None, ordinates=None, tag=None, xtitle=None, logx=False, logy=False, ytitle=None, alpha=None, xlim=None, ylim=None, **kwargs):
        """ Accumulates the traces instead of plotting (like matplotlib with show=False).
        Call show() to show the plot.

        :param m: An array returned by RoadRunner.simulate.
        """
        if not self.fig:
            self.fig = self.newFigure()

        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in range(1,m.shape[1]):
            t = tag if tag else m.colnames[k]
            self.fig.addXYDataset(m[:,0], m[:, k], name=m.colnames[k], tag=t, alpha=alpha)

        if title:
            self.fig.title = title
        if xtitle:
            self.fig.xtitle = xtitle
        if ytitle:
            self.fig.ytitle = ytitle
        if xlim:
            self.fig.setXLim(xlim)
        if ylim:
            self.fig.setYLim(ylim)
        if logx:
            self.fig.logx = logx
        if logy:
            self.fig.logy = logy

    def show(self, reset=True):
        """ Shows the traces accummulated from accumulateTimecourse.

        :param reset: Reset the traces so the next plot will start out empty?
        """
        if self.fig:
            self.fig.render()
        fig = self.fig
        if reset:
            self.fig = None
        return self.fig

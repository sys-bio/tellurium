from collections import defaultdict
import itertools, numpy as np
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
    def initialize(self, title=None, layout=PlottingLayout(), logx=False, logy=False, selections=None):
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
        self.logx = logx
        self.logy = logy
        self.selections=selections

    def addXYDataset(self, x_arr, y_arr, color=None, tag=None, name=None, filter=True):
        """ Adds an X/Y dataset to the plot.

        :param x_arr: A numpy array describing the X datapoints. Should have the same size as y_arr.
        :param y_arr: A numpy array describing the Y datapoints. Should have the same size as x_arr.
        :param color: The color to use (not supported by all backends).
        :param tag: A tag so that all traces of the same type are plotted consistently (for e.g. multiple stochastic traces).
        :param name: The name of the trace.
        :param filter: Apply the self.selections filter?
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


class PlottingEngine(object):
    def __init__(self):
        self.fig = None

    def plotTimecourse(self, m):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        raise NotImplementedError('Abstract method')

    def figureFromTimecourse(self, m, title=None, ordinates=None, tag=None):
        """ Generate a new figure from a timecourse simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.newFigure()
        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in range(1,m.shape[1]):
            fig.addXYDataset(m[:,0], m[:,k], name=m.colnames[k], tag=tag)

        return fig

    def plotTimecourse(self, m, title=None, ordinates=None, tag=None):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.figureFromTimecourse(m, title=title, ordinates=ordinates, tag=tag)
        fig.plot()

    def accumulateTimecourse(self, m, title=None, ordinates=None, tag=None):
        """ Accumulates the traces instead of plotting (like matplotlib with show=False).
        Call show() to show the plot.

        :param m: An array returned by RoadRunner.simulate.
        """
        if not self.fig:
            self.fig = self.newFigure()

        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in range(1,m.shape[1]):
            self.fig.addXYDataset(m[:,0], m[:,k], name=m.colnames[k], tag=tag)

    def show(self, reset=True):
        """ Shows the traces accummulated from accumulateTimecourse.

        :param reset: Reset the traces so the next plot will start out empty?
        """
        if self.fig:
            self.fig.plot()
        fig = self.fig
        if reset:
            self.fig = None
        return self.fig

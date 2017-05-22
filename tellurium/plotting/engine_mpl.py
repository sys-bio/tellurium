from .engine import PlottingEngine, PlottingFigure, PlottingLayout, filterWithSelections

import matplotlib.pyplot as plt
from matplotlib import gridspec
from tempfile import mkstemp
import itertools, numpy as np
from functools import reduce

class MatplotlibFigure(PlottingFigure):
    def __init__(self, title=None, layout=PlottingLayout, use_legend=True, figsize=(9,5), save_to_pdf=False):
        self.initialize(title=title, layout=layout)
        self.use_legend = use_legend
        self.figsize = figsize
        self.save_to_pdf = save_to_pdf

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

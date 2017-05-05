from collections import defaultdict

class PlottingLayout:
    pass

class PlottingFigure(object):
    def initialize(self, title=None, layout=PlottingLayout(), logx=False, logy=False):
        self.title = title
        self.xy_datasets = []
        self.tagged_data = defaultdict(list)
        self.logx = logx
        self.logy = logy

    def addXYDataset(self, x_arr, y_arr, color=None, tag=None, name=None):
        """ Adds an X/Y dataset to the plot.

        :param x_arr: A numpy array describing the X datapoints. Should have the same size as y_arr.
        :param y_arr: A numpy array describing the Y datapoints. Should have the same size as x_arr.
        """
        dataset = {'x': x_arr, 'y': y_arr}
        if name is not None:
            dataset['name'] = name
        if color is not None:
            dataset['color'] = color
        if tag is not None:
            dataset['tag'] = tag
            self.tagged_data[tag].append(dataset)
        self.xy_datasets.append(dataset)

class PlottingEngine(object):
    def plotTimecourse(self, m):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        raise NotImplementedError('Abstract method')

    def filterWithSelections(self, name, selections):
        if selections is not None:
            augmented_sel = selections + list('[{}]'.format(name) for name in selections if not name.startswith('['))
            return name in augmented_sel #or '[{}]'.format(name) in selections
        else:
            return True

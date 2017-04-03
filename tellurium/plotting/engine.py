
class PlottingLayout:
    pass

class PlottingFigure:
    def initialize(self, title=None, layout=PlottingLayout()):
        self.title = title
        self.xy_datasets = []

    def addXYDataset(self, x_arr, y_arr, name=None):
        """ Adds an X/Y dataset to the plot.

        :param x_arr: A numpy array describing the X datapoints. Should have the same size as y_arr.
        :param y_arr: A numpy array describing the Y datapoints. Should have the same size as x_arr.
        """
        dataset = {'x': x_arr, 'y': y_arr}
        if name is not None:
            dataset['name'] = name
        self.xy_datasets.append(dataset)

class PlottingEngine:
    def plotTimecourse(self, m):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        raise NotImplementedError('Abstract method')

    def filterWithSelections(self, name, selections):
        augmented_sel = selections + list('[{}]'.format(name) for name in selections if not name.startswith('['))
        if selections is not None:
            return name in augmented_sel #or '[{}]'.format(name) in selections
        else:
            return True

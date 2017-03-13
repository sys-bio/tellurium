
class PlottingLayout:
    pass

class PlottingFigure:
    pass

class PlottingEngine:
    def plotTimecourse(self, m):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        raise NotImplementedError('Abstract method')

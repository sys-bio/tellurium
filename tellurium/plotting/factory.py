"""
Factory for the engines.
"""

from __future__ import absolute_import, print_function

from .engine_null import NullEngine
__engines = {'null': NullEngine}

from .engine_mpl import MatplotlibEngine
__engines['matplotlib'] = MatplotlibEngine

try:
    from .engine_plotly import PlotlyEngine
    __engines['plotly'] = PlotlyEngine
except ImportError:
    pass

def getEngines():
    global __engines
    return __engines


class PlottingEngineFactory:
    def __init__(self, engine):
        self.engine = engine
        self.save_plots_to_pdf = False
        self.engines = getEngines()

    def __call__(self):
        """ Creates a plotting engine based on passed argument.

        :param engine: A string specifying which engine to create. Valid values are 'matplotlib' and 'plotly'.
        :type engine:  String
        """
        possible_keys = [
            'matplotlib',
            'plotly',
            'null'
        ]
        try:
            return self.engines[self.engine]()
        except KeyError:
            if not self.engine in possible_keys:
                raise RuntimeError('No such plotting engine "{}". Possible values are {}.'.format(self.engine, ', '.join(possible_keys)))
            raise RuntimeError('Could not create plotting engine because {} is not available.'.format(self.engine))

factories = {}
def getPlottingEngineFactory(engine):
    global factories
    if not engine in factories:
        factories[engine] = PlottingEngineFactory(engine)
    return factories[engine]


__engines = {}

from .engine_mpl import MatplotlibPlottingEngine
__engines['matplotlib'] = MatplotlibPlottingEngine

try:
    from .engine_plotly import PlotlyPlottingEngine
    __engines['plotly'] = PlotlyPlottingEngine
except ImportError:
    pass

def getPlottingEngine(engine):
    """ Creates a plotting engine based on passed argument.

    :param engine: A string specifying which engine to create. Valid values are 'matplotlib' and 'plotly'.
    :type engine:  String
    """
    possible_keys = [
        'matplotlib',
        'plotly',
    ]
    try:
        return __engines[engine]()
    except KeyError:
        if not engine in possible_keys:
            raise RuntimeError('No such plotting engine "{}". Possible values are {}.'.format(engine, ', '.join(possible_keys)))
        raise RuntimeError('Could not create plotting engine because {} is not available.'.format(engine))

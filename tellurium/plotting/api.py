from __future__ import print_function, division, absolute_import

# _plot_index = 0
def plot(x, y, show=True, **kwargs):
    from .. import getPlottingEngine
    # global _plot_index
    return getPlottingEngine().plot(x, y, show=show, **kwargs)

def show(reset=True):
    from .. import getPlottingEngine
    return getPlottingEngine().show(reset=reset)
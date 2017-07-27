from __future__ import print_function, division, absolute_import

# _plot_index = 0
def plot(x, y, hold=False, **kwargs):
    from .. import getPlottingEngine
    # global _plot_index
    return getPlottingEngine().plot(x, y, hold=hold, **kwargs)

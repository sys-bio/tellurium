"""
Parameter scan utilities.
"""

from __future__ import print_function, division
import matplotlib.pyplot as plt


def plot2DParameterScan(r, p1, p1Range, p2, p2Range, start=0, end=100, points=101):
    """ Create a 2D Parameter scan and plot the results.

    :param r: RoadRunner instance
    :param p1: id of first parameter
    :param p1Range: range of first parameter
    :param p2: id of second parameter
    :param p2Range: range of second parameter
    """

    # FIXME: refactor in plotting function & and parameter scan function. I.e.
    # one function for performing simulations, the other only plots the results.
    # FIXME: return the plot object to create figure

    f, axarr = plt.subplots(
        len(p1Range),
        len(p2Range),
        sharex='col',
        sharey='row')

    for i, k1 in enumerate(p1Range):
        for j, k2 in enumerate(p2Range):
            r.reset()
            r[p1], r[p2] = k1, k2
            result = r.simulate(start, end, points)
            columns = result.shape[1]
            legendItems = r.selections[1:]
            if columns-1 != len(legendItems):
                raise Exception('Legend list must match result array')
            for c in range(columns-1):
                axarr[i, j].plot(
                    result[:, 0],
                    result[:, c+1],
                    linewidth=2,
                    label=legendItems[c])

            if (i == len(p1Range) - 1):
                axarr[i, j].set_xlabel('%s = %.2f' % (p2, k2))
            if (j is 0):
                axarr[i, j].set_ylabel('%s = %.2f' % (p1, k1))

    f.show()
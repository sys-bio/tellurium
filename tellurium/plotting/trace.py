"""
Function for manipulation of traces.

This are currently not used.
"""


def process_trace(trace):
    """ If each entry in the task consists of a single point
    (e.g. steady state scan), concatenate the points.
    Otherwise, plot as separate curves."""
    warnings.warn("don't use this", DeprecationWarning)
    # print('trace.size = {}'.format(trace.size))
    # print('len(trace.shape) = {}'.format(len(trace.shape)))
    if trace.size > 1:
        # FIXME: this adds a nan at the end of the data. This is a bug.
        if len(trace.shape) == 1:
            # return np.concatenate((np.atleast_1d(trace), np.atleast_1d(np.nan)))
            return np.atleast_1d(trace)

        elif len(trace.shape) == 2:
            #print('2d trace')
            # print(trace.shape)
            # FIXME: this adds a nan at the end of the data. This is a bug.
            # result = np.vstack((np.atleast_1d(trace), np.full((1,trace.shape[-1]),np.nan)))
            result = np.vstack((np.atleast_1d(trace), np.full((1, trace.shape[-1]))))
            return result
    else:
        return np.atleast_1d(trace)


def terminate_trace(trace):
    """ If each entry in the task consists of a single point
    (e.g. steady state scan), concatenate the points.
    Otherwise, plot as separate curves."""
    warnings.warn("don't use this", DeprecationWarning)

    if isinstance(trace, list):
        if len(trace) > 0 and not isinstance(trace[-1], list) and not isinstance(trace[-1], dict):
            # if len(trace) > 2 and isinstance(trace[-1], dict):
            # e = np.array(trace[-1], copy=True)
            e = {}
            for name in trace[-1].colnames:
                e[name] = np.atleast_1d(np.nan)
            # print('e:')
            # print(e)
            return trace + [e]
    return trace


def fix_endpoints(x, y, color, tag, fig):
    """ Adds endpoint markers wherever there is a discontinuity in the data."""
    warnings.warn("don't use this", DeprecationWarning)
    # expect x and y to be 1d
    if len(x.shape) > 1:
        raise RuntimeError('Expected x to be 1d')
    if len(y.shape) > 1:
        raise RuntimeError('Expected y to be 1d')
    x_aug = np.concatenate((np.atleast_1d(np.nan), np.atleast_1d(x), np.atleast_1d(np.nan)))
    y_aug = np.concatenate((np.atleast_1d(np.nan), np.atleast_1d(y), np.atleast_1d(np.nan)))
    w = np.argwhere(np.isnan(x_aug))

    endpoints_x = []
    endpoints_y = []

    for begin, end in ( (int(w[k]+1), int(w[k+1])) for k in range(w.shape[0]-1) ):
        if begin != end:
            #print('begin {}, end {}'.format(begin, end))
            x_values = x_aug[begin:end]
            x_identical = np.all(x_values == x_values[0])
            y_values = y_aug[begin:end]
            y_identical = np.all(y_values == y_values[0])
            #print('x_values')
            #print(x_values)
            #print('x identical? {}'.format(x_identical))
            #print('y_values')
            #print(y_values)
            #print('y identical? {}'.format(y_identical))

            if x_identical and y_identical:
                # get the coords for the new markers
                x_begin = x_values[0]
                x_end   = x_values[-1]
                y_begin = y_values[0]
                y_end   = y_values[-1]

                # append to the lists
                endpoints_x += [x_begin, x_end]
                endpoints_y += [y_begin, y_end]

        if endpoints_x:
            fig.addXYDataset(np.array(endpoints_x), np.array(endpoints_y), color=color, tag=tag, mode='markers')
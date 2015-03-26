def plot2DParameterScan(
    r, param1, param1Range, param2, param2Range, start=0, end=100, steps=100
):
    import matplotlib.pyplot as p
    f, axarr = p.subplots(
        len(param1Range),
        len(param2Range),
        sharex='col',
        sharey='row')

    for i, k1 in enumerate(param1Range):
        for j, k2 in enumerate(param2Range):
            r.reset()
            r[param1], r[param2] = k1, k2
            result = r.simulate(start, end, steps)
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

            if (i == len(param1Range) - 1):
                axarr[i, j].set_xlabel('%s = %.2f' % (param2, k2))
            if (j is 0):
                axarr[i, j].set_ylabel('%s = %.2f' % (param1, k1))

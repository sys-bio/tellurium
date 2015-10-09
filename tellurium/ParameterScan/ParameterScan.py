import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib

class ParameterScan (object):
    def __init__(self, rr):
        self.startTime = 0
        self.endTime = 20
        self.numberOfPoints = 50
        self.polyNumber = 10
        self.startValue = None
        self.endValue = None
        self.value = None
        self.independent = None
        self.selection = None
        self.dependent = None
        self.integrator = "cvode"
        self.rr = rr
        self.color = None
        self.width = 2.5
        self.alpha = 0.7
        self.title = None
        self.xlabel = 'toSet'
        self.ylabel = 'toSet'
        self.zlabel = 'toSet'
        self.colormap = "seismic"
        self.colorbar = True
        self.antialias = True
        self.sameColor = False
        self.legend = True

    
    def sim(self):
        """Runs a simulation and returns the result for a plotting function. Not intended to
        be called by user."""
        mdl = self.rr.model
        if self.selection is None:
            result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, integrator = self.integrator)
        else:
            if not isinstance(self.selection, list):
                self.selection = [self.selection]
            if 'time' not in [item.lower() for item in self.selection]:
                self.selection = ['time'] + self.selection
            for item in self.selection:
                if item not in mdl.getFloatingSpeciesIds() and item not in mdl.getBoundarySpeciesIds():
                    if item.lower() != 'time':
                        raise ValueError('"{0}" is not a valid species in loaded model'.format(item))
            result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints,
                                      self.selection, integrator = self.integrator)
        return result

    def plotArray(self):
        """Plots result of simulation with options for linewdith and line color.

        p.plotArray()"""
        result = self.sim()
        if self.color is None:
            for species in self.rr.timeCourseSelections[1:]:
                plt.plot(result[:,0], result[species], linewidth = self.width, label = species)
        else:
            if len(self.color) != result.shape[1]:
                self.color = self.colorCycle()
            for i in range(result.shape[1] - 1):
                plt.plot(result[:,0], result[:,i+1], color = self.color[i], 
                        linewidth = self.width, label = self.rr.timeCourseSelections[i+1])
            
        if self.xlabel == 'toSet':
            plt.xlabel('time')
        elif self.xlabel:
            plt.xlabel(self.xlabel)
        if self.ylabel == 'toSet':
            plt.ylabel('concentration')
        elif self.ylabel:
            plt.ylabel(self.ylabel)
        if self.title is not None:
            plt.suptitle(self.title)
        if self.legend:
            plt.legend()
        plt.show()

    def graduatedSim(self):
        """Runs successive simulations with incremental changes in one species, and returns
        results for a plotting function. Not intended to be called by user."""
        mdl = self.rr.model
        if self.value is None:
            self.value = mdl.getFloatingSpeciesIds()[0]
            print 'Warning: self.value not set. Using self.value = {0}'.format(self.value)
        elif not isinstance(self.value, str):
            raise ValueError('self.value must be a string')
        elif self.value not in mdl.getFloatingSpeciesIds() and self.value not in mdl.getBoundarySpeciesIds():
            if self.value not in mdl.getGlobalParameterIds():
                raise ValueError('self.value "{0}" cannot be found in loaded model'.format(self.value))
        if self.startValue is None:
            self.startValue = mdl[self.value]
        else:
            self.startValue = float(self.startValue)
        if self.endValue is None:
            self.endValue = self.startValue + 5
        else:
            self.endValue = float(self.endValue)
        if self.selection is None:
            self.selection = [mdl.getFloatingSpeciesIds()[0]]
        else:
            if not isinstance(self.selection, list):
                self.selection = [self.selection]
            for item in self.selection:
                if item.lower() == 'time':
                    self.selection.remove(item)
                if not isinstance(item, str) or (item not in mdl.getFloatingSpeciesIds() and item not in mdl.getBoundarySpeciesIds()):
                    if item.lower() != 'time':
                        raise ValueError('{0} cannot be found in loaded model'.format(item))
        self.selection = ['time'] + self.selection            
        polyNumber = float(self.polyNumber)
        mdl[self.value] = self.startValue
        m = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints,
                             self.selection, integrator = self.integrator)
        interval = ((self.endValue - self.startValue) / (polyNumber - 1))
        start = self.startValue
        while start < self.endValue - .00001:
            self.rr.reset()
            start += interval
            mdl[self.value] = start
            m1 = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints,
                                  self.selection, integrator = self.integrator)
            m1 = np.delete(m1, 0, 1)
            m = np.hstack((m, m1))

        return m

    def plotGraduatedArray(self):
        """Plots array with either default multiple colors or user sepcified colors using
        results from graduatedSim().

        p.plotGraduatedArray()"""
        result = self.graduatedSim()
        interval = ((self.endValue - self.startValue) / (self.polyNumber - 1))
        numSp = len(self.selection) - 1
        if self.color is None and self.sameColor is True:
            count = 1
            for species in self.selection[1:]:
                for i in range(self.polyNumber):
                    if numSp > 1:
                        lbl = "{0}, {1} = {2}".format(species, self.value, round((self.startValue + (interval * i)), 2))
                    else:
                        lbl = "{0} = {1}".format(self.value, round((self.startValue + (interval * i)), 2))
                    plt.plot(result[:,0], result[:,numSp*i+count], linewidth = self.width, color = 'b', label = lbl)
                count += 1
                    
        elif self.color is None:
            count = 1
            for species in self.selection[1:]:
                for i in range(self.polyNumber):
                    if numSp > 1:
                        lbl = "{0}, {1} = {2}".format(species, self.value, round((self.startValue + (interval * i)), 2))
                    else:
                        lbl = "{0} = {1}".format(self.value, round((self.startValue + (interval * i)), 2))
                    plt.plot(result[:,0], result[:,numSp*i+count], linewidth = self.width, label = lbl)
                count += 1
                    
        else:
            if len(self.color) != self.polyNumber:
                self.color = self.colorCycle()
            count = 1
            for species in self.selection[1:]:
                for i in range(self.polyNumber):
                    if numSp > 1:
                        lbl = "{0}, {1} = {2}".format(species, self.value, round((self.startValue + (interval * i)), 2))
                    else:
                        lbl = "{0} = {1}".format(self.value, round((self.startValue + (interval * i)), 2))
                    plt.plot(result[:,0], result[:,numSp*i+count], color = self.color[i],
                                 linewidth = self.width, label = lbl)
                count += 1
                         
        if self.title is not None:
            plt.suptitle(self.title)
        if self.xlabel == 'toSet':
            plt.xlabel('time')
        elif self.xlabel:
            plt.xlabel(self.xlabel)
        if self.ylabel == 'toSet':
            plt.ylabel('concentration')
        elif self.ylabel:
            plt.ylabel(self.ylabel)
        if self.legend:
            plt.legend()
        plt.show()

    def plotPolyArray(self):
        """Plots results as individual graphs parallel to each other in 3D space using results
        from graduatedSim().

        p.plotPolyArray()"""
        result = self.graduatedSim()
        interval = ((self.endValue - self.startValue) / (self.polyNumber - 1))
        self.rr.reset()
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        if self.startValue is None:
            self.startValue = self.rr.model[self.value]
        columnNumber = self.polyNumber + 1
        lastPoint = [self.endTime]
        firstPoint = [self.startTime]
        for i in range(int(columnNumber) - 1):
            lastPoint.append(0)
            firstPoint.append(0)
        lastPoint = np.array(lastPoint)
        firstPoint = np.array(firstPoint)
        zresult = np.vstack((result, lastPoint))
        zresult = np.vstack((firstPoint, zresult))
        zs = []
        result = []
        for i in range(int(columnNumber)-1):
            zs.append(i)
            result.append(zip(zresult[:,0], zresult[:,(i+1)]))   
        if self.color is None:
            poly = PolyCollection(result)
        else:
            if len(self.color) != self.polyNumber:
                self.color = self.colorCycle()
            poly = PolyCollection(result, facecolors = self.color, closed = False)

        poly.set_alpha(self.alpha)
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlim3d(0, self.endTime)
        ax.set_ylim3d(0, (columnNumber - 1))
        ax.set_zlim3d(0, (self.endValue + interval))
        if self.xlabel == 'toSet':
            ax.set_xlabel('Time')
        elif self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel == 'toSet':
            ax.set_ylabel('Trial Number')
        elif self.ylabel:
            ax.set_ylabel(self.ylabel)
        if self.zlabel == 'toSet':
            ax.set_zlabel(self.value)
        elif self.zlabel:
            ax.set_zlabel(self.zlabel)
#        ax.set_xlabel('Time') if self.xlabel is None else ax.set_xlabel(self.xlabel)
#        ax.set_ylabel('Trial Number') if self.ylabel is None else ax.set_ylabel(self.ylabel)
#        ax.set_zlabel(self.value) if self.zlabel is None else ax.set_zlabel(self.zlabel)
        if self.title is not None:
            ax.set_title(self.title)
        plt.show()

    def plotSurface(self):
        """ Plots results of simulation as a colored surface. Takes three variables, two
        independent and one dependent. Legal colormap names can be found at
        http://matplotlib.org/examples/color/colormaps_reference.html.

        p.plotSurface()"""
        try:
#            if self.independent is None and self.dependent is None:
#                self.independent = ['Time']
#                defaultParameter = self.rr.model.getGlobalParameterIds()[0]
#                self.independent.append(defaultParameter)
#                defaultSpecies = self.rr.model.getFloatingSpeciesIds()[0]
#                self.dependent = [defaultSpecies]
#                print 'Warning: self.independent and self.dependent not set. Using' \
#                ' self.independent = %s and self.dependent = %s' % (self.independent, self.dependent)
            if self.independent is None:
                self.independent = ['Time']
                defaultParameter = self.rr.model.getGlobalParameterIds()[0]
                self.independent.append(defaultParameter)
                print 'Warning: self.independent not set. Using: {0}'.format(self.independent)
            if self.dependent is None:
                defaultSpecies = self.rr.model.getFloatingSpeciesIds()[0]
                self.dependent = defaultSpecies
                print 'Warning: self.dependent not set. Using: {0}'.format(self.dependent)
                
            if len(self.independent) < 2:
                raise ValueError('self.independent must contain two independent variables')
            
            if not isinstance(self.independent, list):
                raise ValueError('self.independent must be a list of strings')
            if not isinstance(self.dependent, str):
                raise ValueError('self.dependent must be a string')
            if self.startValue is None:
                if self.independent[0].lower() != 'time':
                    self.startValue = self.rr.model[self.independent[0]]
                else:
                    self.startValue = self.rr.model[self.independent[1]]
            if self.endValue is None:
                self.endValue = self.startValue + 5
    
    
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            interval = (self.endTime - self.startTime) / float(self.numberOfPoints - 1)
            X = np.arange(self.startTime, (self.endTime + (interval - 0.001)), interval)
            interval = (self.endValue - self.startValue) / float(self.numberOfPoints - 1)
            Y = np.arange(self.startValue, (self.endValue + (interval - 0.001)), interval)
            X, Y = np.meshgrid(X, Y)
            self.rr.reset()
            self.rr.model[self.independent[1]] = self.startValue
            Z = self.rr.simulate(self.startTime, self.endTime, (self.numberOfPoints),
                                 [self.dependent], integrator = self.integrator)
            Z = Z.T
            for i in range(self.numberOfPoints - 1):
                self.rr.reset()
                self.rr.model[self.independent[1]] = self.startValue + ((i + 1) * interval)
                Z1 = self.rr.simulate(self.startTime, self.endTime, (self.numberOfPoints),
                                     [self.dependent], integrator = self.integrator)
                Z1 = Z1.T
                Z = np.concatenate ((Z, Z1))
    
            if self.antialias is False:
                surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap = self.colormap,
                                       antialiased = False, linewidth=0)
            else:
                surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap = self.colormap,
                                       linewidth=0)
    
            ax.yaxis.set_major_locator(LinearLocator((6)))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            if self.xlabel == 'toSet':
                ax.set_xlabel(self.independent[0])
            elif self.xlabel:
                ax.set_xlabel(self.xlabel)
            if self.ylabel == 'toSet':
                ax.set_ylabel(self.independent[1])
            elif self.ylabel:
                ax.set_ylabel(self.ylabel)
            if self.zlabel == 'toSet':
                ax.set_zlabel(self.dependent)
            elif self.zlabel:
                ax.set_zlabel(self.zlabel)
            if self.title is not None:
                ax.set_title(self.title)
    
            if self.colorbar:
                fig.colorbar(surf, shrink=0.5, aspect=4)
    
            plt.show()
        
        except Exception as e:
            print 'error: {0}'.format(e.message)

    def plotMultiArray(self, param1, param1Range, param2, param2Range):
        """Plots separate arrays for each possible combination of the contents of param1range and
        param2range as an array of subplots. The ranges are lists of values that determine the
        initial conditions of each simulation.

        p.multiArrayPlot('S1', [1, 2, 3], 'S2', [1, 2])"""
        mdl = self.rr.model        
        
        f, axarr = plt.subplots(
            len(param1Range),
            len(param2Range),
            sharex='col',
            sharey='row')

        if self.color is None:
            self.color = ['b', 'g', 'r', 'k']

        for i, k1 in enumerate(param1Range):
            for j, k2 in enumerate(param2Range):
                self.rr.reset()
                mdl[param1], mdl[param2] = k1, k2
                if self.selection is None:
                    result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints,
                                                integrator = self.integrator) 
                else:
                    if 'time' not in [item.lower() for item in self.selection]:
                        self.selection = ['time'] + self.selection                    
                    for item in self.selection:
                        if item not in mdl.getFloatingSpeciesIds() and item not in mdl.getBoundarySpeciesIds():
                            if item.lower() != 'time':
                                raise ValueError('"{0}" is not a valid species in loaded model'.format(item))
                    result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints,
                                                  self.selection, integrator = self.integrator)
                columns = result.shape[1]
                legendItems = self.rr.timeCourseSelections[1:]
                if columns-1 != len(legendItems):
                    raise Exception('Legend list must match result array')
                for c in range(columns-1):
                    axarr[i, j].plot(
                        result[:, 0],
                        result[:, c+1],
                        linewidth = self.width,
                        label = legendItems[c])
                if (self.legend):
                    plt.legend(loc= 3, bbox_to_anchor=(0.5, 0.5))

                if (i == (len(param1Range) - 1)):
                    axarr[i, j].set_xlabel('%s = %.2f' % (param2, k2))
                if (j == 0):
                    axarr[i, j].set_ylabel('%s = %.2f' % (param1, k1))
                if self.title is not None:
                    plt.suptitle(self.title)


    def createColormap(self, color1, color2):
        """Creates a color map for plotSurface using two colors as RGB tuplets, standard color
        names, e.g. 'aqua'; or hex strings.

        p.colormap = p.createColorMap([0,0,0], [1,1,1])"""

        if isinstance(color1, str) is True:
            try:
                color1 = matplotlib.colors.colorConverter.to_rgb('%s' % color1)
            except ValueError:
                print '"{0}" is not a valid color name, using default "blue" instead'.format(color1)
                color1 = matplotlib.colors.colorConverter.to_rgb('blue')
        if isinstance(color2, str) is True:
            try:
                color2 = matplotlib.colors.colorConverter.to_rgb('%s' % color2)
            except ValueError:
                print '"{0}" is not a valid color name, using default "blue" instead'.format(color2)
                color2 = matplotlib.colors.colorConverter.to_rgb('blue')

        cdict = {'red': ((0., 0., color1[0]),
                         (1., color2[0], 0.)),

                 'green': ((0., 0., color1[1]),
                           (1., color2[1], 0.)),

                 'blue': ((0., 0., color1[2]),
                          (1., color2[2], 0.))}
        my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        return my_cmap


    def colorCycle(self):
        """Adjusts contents of self.color as needed for plotting methods."""
        if len(self.color) < self.polyNumber:
            for i in range(self.polyNumber - len(self.color)):
                self.color.append(self.color[i])
        else:
            for i in range(len(self.color) - self.polyNumber):
                del self.color[-(i+1)]
        return self.color

    def createColorPoints(self):
        """Sets self.color to a set of values that allow plotPolyArray, plotArray,
        or plotGraduatedArray to take on colors from a colormap. The colormap can either
        be user-defined using createColormap or one of the standard colormaps.

        p.createColorPoints() """
        color = []
        interval = 1.0 / self.polyNumber
        count = 0
        if isinstance(self.colormap, str) is True:
            for i in range(self.polyNumber):
                color.append(eval('matplotlib.pylab.cm.%s(%s)' % (self.colormap, count)))
                count += interval
        else:
            for i in range(self.polyNumber):
                color.append(self.colormap(count))
                count += interval
        self.color = color
        


class SteadyStateScan (object):
    def __init__(self, rr):
        self.startTime = 0
        self.endTime = 20
        self.numberOfPoints = 50
        self.polyNumber = 10
        self.startValue = None
        self.endValue = None
        self.value = None
        self.independent = None
        self.selection = None
        self.dependent = None
        self.integrator = "cvode"
        self.rr = rr
        self.color = None
        self.width = 2.5
        self.alpha = 0.7
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        self.colormap = "seismic"
        self.colorbar = True
        self.antialias = True
        self.sameColor = False

    def steadyStateSim(self):
        if self.value is None:
            self.value = self.rr.model.getFloatingSpeciesIds()[0]
            print 'Warning: self.value not set. Using self.value = %s' % self.value
        if self.startValue is None:
            self.startValue = self.rr.model[self.value]
        if self.endValue is None:
            self.endValue = self.startValue + 5
        interval = (float(self.endValue - self.startValue) / float(self.numberOfPoints - 1))
        a = []
        for i in range(len(self.selection) + 1):
            a.append(0.)
        result = np.array(a)
        start = self.startValue
        for i in range(self.numberOfPoints):
            self.rr.reset()
            start += interval
            self.rr.model[self.value] = start
            self.rr.steadyState()
            b = [self.rr.model[self.value]]
            for i in range(len(self.selection)):
                b.append(self.rr.model[self.selection[i]])
            result = np.vstack((result, b))
        result = np.delete(result, 0, 0)
        return result

    def plotArray(self):
        result = self.steadyStateSim()
        print result
        if self.color is None:
            plt.plot(result[:,0], result[:,1:], linewidth = self.width)
        else:
            if len(self.color) != result.shape[1]:
                self.color = self.colorCycle()
            for i in range(result.shape[1] - 1):
                plt.plot(result[:,0], result[:,i], color = self.color[i], linewidth = self.width)

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
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        self.colormap = "seismic"
        self.colorbar = True
        self.antialias = True
        self.sameColor = False
        
        
    def Sim(self):
        """Runs a simulation and returns the result for a plotting function. Not intended to 
        be called by user."""
        if self.selection is None:
            result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                                      integrator = self.integrator)
        else:
            result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                                      self.selection, integrator = self.integrator)
        return result
                             
    def plotArray(self):
        """Plots result of simulation with options for linewdith and line color.
        
        p.plotArray()"""
        result = self.Sim()
        if self.color is None:
            plt.plot(result[:,0], result[:,1:], linewidth = self.width)
        else: 
            plt.plot(result[:,0], result[:,1:], self.color, linewidth = self.width)    
        
        if self.ylabel is not None:
            plt.ylabel(self.ylabel) 
        if self.xlabel is not None:
            plt.xlabel(self.xlabel)
        if self.title is not None:
            plt.suptitle(self.title)
        plt.show()
    
    def graduatedSim(self):
        """Runs successive simulations with incremental changes in one species, and returns 
        results for a plotting function. Not intended to be called by user."""
        if self.startValue is None:
            self.startValue = self.rr.model[self.value]
        else:
            self.startValue = self.startValue
        if self.endValue is None:
            self.endValue = self.startValue + 5
        else:
            self.endValue = self.endValue
        if self.value is None:
            self.value = self.rr.model.getFloatingSpeciesIds()[0]
            print 'warning: self.value not set. Using self.value = %s' % self.value
        m = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                             ["Time", self.selection], integrator = self.integrator)
        interval = ((self.endValue - self.startValue) / (self.polyNumber - 1)) 
        start = self.startValue
        while start < (self.endValue - .00001):
            self.rr.reset()   
            start += interval
            self.rr.model[self.value] = start   
            m1 = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                                  [self.selection], integrator = self.integrator)
            m = np.hstack((m, m1))
        return m
          
    def plotGraduatedArray(self):
        """Plots array with either default multiple colors or user sepcified colors using 
        results from graduatedSim().
        
        p.plotGraduatedArray()"""
        result = self.graduatedSim()
        if self.color is None and self.sameColor is True:
            plt.plot(result[:,0], result[:,1:], linewidth = self.width, color = 'b')
        elif self.color is None:
            plt.plot(result[:,0], result[:,1:], linewidth = self.width)
        else:
            if len(self.color) != self.polyNumber:
                self.color = self.colorCycle()
            for i in range(self.polyNumber):
                plt.plot(result[:,0], result[:,(i+1)], color = self.color[i], 
                         linewidth = self.width)
        if self.ylabel is not None:
            plt.ylabel(self.ylabel) 
        if self.xlabel is not None:
            plt.xlabel(self.xlabel)
        if self.title is not None:
            plt.suptitle(self.title)
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
        columnNumber = int((((self.endValue - self.startValue) / self.polyNumber)) + 2)
        columnNumber = self.polyNumber
        lastPoint = [self.endTime]
        for i in range(columnNumber):
            lastPoint.append(0)
        lastPoint = np.array(lastPoint)
        lastPoint = np.vstack((result, lastPoint))
        zs = []
        result = []
        for i in range(columnNumber):
            zs.append(i)
            result.append(zip(lastPoint[:,0], lastPoint[:,(i+1)]))
        if self.color is None:        
            poly = PolyCollection(result)
        else:
            if len(self.color) != self.polyNumber:
                self.color = self.colorCycle()
            poly = PolyCollection(result, facecolors = self.color)
            
        poly.set_alpha(self.alpha)
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlim3d(0, self.endTime)
        ax.set_ylim3d(0, (columnNumber - 1))
        ax.set_zlim3d(0, (self.endValue + interval))
        ax.set_xlabel('Time') if self.xlabel is None else ax.set_xlabel(self.xlabel)
        ax.set_ylabel('Trial Number') if self.ylabel is None else ax.set_ylabel(self.ylabel)
        ax.set_zlabel(self.value) if self.zlabel is None else ax.set_zlabel(self.zlabel)
        if self.title is not None:
            ax.set_title(self.title)
        plt.show()
        
    def plotSurface(self):
        """ Plots results of simulation as a colored surface. Takes three variables, two independent
        and one dependent. Legal colormap names can be found at 
        http://matplotlib.org/examples/color/colormaps_reference.html. 
        
        p.plotSurface()"""
        if self.independent is None or self.dependent is None:
            self.independent = ['Time']
            aa = self.rr.model.getGlobalParameterIds()[0]
            self.independent.append(aa)
            self.dependent = self.rr.model.getFloatingSpeciesIds()[0].split()
            print 'Warning: self.independent and self.dependent not set. Using' \
            ' self.independent = %s and self.dependent = %s' % (self.independent, self.dependent)
        if not isinstance(self.independent, list) or not isinstance(self.dependent, list):
            raise Exception('self.indpendent and self.dependent must be lists')
        if self.startValue is None:
            if self.independent[0] != 'Time' and self.independent[0] != 'time':
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
        Z = self.rr.simulate(self.startTime, self.endTime, (self.numberOfPoints - 1), 
                             self.dependent, integrator = self.integrator)
        Z = Z.T
        for i in range(self.numberOfPoints - 1):
            self.rr.reset()
            self.rr.model[self.independent[1]] = self.startValue + ((i + 1) * interval)
            Z1 = self.rr.simulate(self.startTime, self.endTime, (self.numberOfPoints - 1), 
                                 self.dependent, integrator = self.integrator)
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
        ax.set_xlabel(self.independent[0]) if self.xlabel is None else ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.independent[1]) if self.ylabel is None else ax.set_ylabel(self.ylabel)
        ax.set_zlabel(self.dependent[0]) if self.zlabel is None else ax.set_zlabel(self.zlabel)
        if self.title is not None:
            ax.set_title(self.title)

        if self.colorbar is True:
            fig.colorbar(surf, shrink=0.5, aspect=4)

        plt.show()
        
    def plotMultiArray(self, param1, param1Range, param2, param2Range):
        """Plots separate arrays for each possible combination of the contents of param1range and 
        param2range as an array of subplots. The ranges are lists of values that determine the
        initial conditions of each simulation. 
        
        p.multiArrayPlot('S1', [1, 2, 3], 'S2', [1, 2])"""
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
                self.rr.model[param1], self.rr.model[param2] = k1, k2
                if self.selection is None:
                    result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                                              integrator = self.integrator)
                else:
                     result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                                               self.selection, integrator = self.integrator)         
                columns = result.shape[1]
                legendItems = self.rr.selections[1:]
                if columns-1 != len(legendItems):
                    raise Exception('Legend list must match result array')
                for c in range(columns-1):
                    axarr[i, j].plot(
                        result[:, 0], 
                        result[:, c+1],
                        linewidth = self.width,
                        label = legendItems[c])

                if (i == (len(param1Range) - 1)):
                    axarr[i, j].set_xlabel('%s = %.2f' % (param2, k2))
                if (j == 0):
                    axarr[i, j].set_ylabel('%s = %.2f' % (param1, k1))
                if self.title is not None:
                    plt.suptitle(self.title)
                    
                    
    def createColorMap(self, color1, color2):
        """Creates a color map for plotSurface using two colors in RGB tuplets.
        p.colormap = p.createColorMap([0,0,0], [1,1,1])"""
        
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
            print self.color
        return self.color
        

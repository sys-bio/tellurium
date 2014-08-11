import tellurium as te
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

class parameterScan (object):
    def __init__(self, rr):
        self.startTime = 0
        self.endTime = 20
        self.numberOfPoints = 100
        self.interval = 1
        self.endValue = 10
        self.parameter = "S1"
        self.independent = ["Time", "k2"]
        self.selection = ["S1"]
        self.dependent = ["S1"]
        self.startInd = [1]
        self.endInd = [5]
        self.integrator = "cvode"
        self.rr = rr
        self.colorSelect = None
        self.width = 2.5
        self.alpha = 0.7
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        self.colormap = "seismic"
        self.colorbar = True
    
    def graduatedSim(self):
        """Runs successive simulations with incremental changes in one species."""
        start = self.rr.model[self.parameter]
        m = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                             ["Time", self.selection], integrator = self.integrator)
        while start <= self.endValue:
            start += self.interval   
            self.rr.reset()        
            self.rr.model[self.parameter] = start   
            m1 = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                                  [self.selection], integrator = self.integrator)
            m = np.hstack((m, m1))      
        return m
            
    def plotSameColorArray(self):
        """Overrides default color selection and plots all lines in one color"""
        result = self.graduatedSim()
        plt.plot(result[:,0], result[:,1:], color = self.colorSelect[0], linewidth = self.width)
        plt.show()
          
    def plotArray(self):
        """Plots array with either default multiple colors or user sepcified colors"""
        result = self.graduatedSim()
        self.rr.reset()
        columnNumber = int((((self.endValue - self.rr.model[self.parameter]) / self.interval)) + 2)
        print columnNumber
        if self.colorSelect is None:
            plt.plot(result[:,0], result[:,1:], linewidth = self.width)
        else:
            for i in range(columnNumber):
                plt.plot(result[:,0], result[:,(i+1)], color = self.colorSelect[i], 
                          linewidth = self.width)
                          
                          
    def threeDPlot(self):
        """Plots results as individual graphs parallel to each other in 3D space"""
        result = self.graduatedSim()
        self.rr.reset()
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        columnNumber = int((((self.endValue - self.rr.model[self.parameter]) / self.interval)) + 2)
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
            print result
        if self.colorSelect is None:        
            poly = PolyCollection(result)
        else:
            poly = PolyCollection(result, facecolors = self.colorSelect)
        poly.set_alpha(self.alpha)
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlim3d(0, self.endTime)
        ax.set_ylim3d(0, (columnNumber - 1))
        ax.set_zlim3d(0, (self.endValue + self.interval))
        ax.set_xlabel('Time')
        ax.set_ylabel('Trial Number')
        ax.set_zlabel(self.parameter)
        plt.show()
        
    def surfacePlot(self):
        """ Plots results of simulation as a colored surface. Takes three variables, two independent
        and one dependent. Legal colormap names can be found at 
        http://matplotlib.org/examples/color/colormaps_reference.html. 
        
        p.surfacePlot()"""
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        interval = (self.endTime - self.startTime) / float(self.numberOfPoints - 1)
        X = np.arange(self.startTime, (self.endTime + (interval - 0.001)), interval)
        interval = (self.endInd - self.startInd) / float(self.numberOfPoints - 1)
        Y = np.arange(self.startInd, (self.endInd + (interval - 0.001)), interval)
        X, Y = np.meshgrid(X, Y)
        self.rr.reset()
        self.rr.model[self.independent[1]] = self.startInd
        Z = self.rr.simulate(self.startTime, self.endTime, (self.numberOfPoints - 1), 
                                 self.dependent, integrator = self.integrator)
        Z = Z.T
        for i in range(self.numberOfPoints - 1):
            self.rr.reset()
            self.rr.model[self.independent[1]] = self.startInd + ((i + 1) * interval)
            Z1 = self.rr.simulate(self.startTime, self.endTime, (self.numberOfPoints - 1), 
                                 self.dependent, integrator = self.integrator)
            Z1 = Z1.T
            Z = np.concatenate ((Z, Z1))  
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap = self.colormap,
                               linewidth=0)
        ax.yaxis.set_major_locator(LinearLocator((6)))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax.set_xlabel(self.independent[0]) if self.xlabel is None else ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.independent[1]) if self.ylabel is None else ax.set_ylabel(self.ylabel)
        ax.set_zlabel(self.dependent[0]) if self.zlabel is None else ax.set_zlabel(self.zlabel)

        if self.colorbar is True:
            fig.colorbar(surf, shrink=0.5, aspect=4)

        plt.show()

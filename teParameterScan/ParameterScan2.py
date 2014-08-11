import tellurium as te
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

class parameterScan (object):
    def __init__(self, rr):
        self.startTime = 0
        self.endTime = 20
        self.numberOfPoints = 100
        self.independent = ["Time", "k2"]
        self.selection = ["Time", "S1"]
        self.dependent = ["S1"]
        self.startInd = [1]
        self.endInd = [5]
        self.integrator = "cvode"
        self.rr = rr
        self.colorSelect = None
        self.width = 2.5
        self.color = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        self.colormap = "seismic"
        self.colorbar = True
        self.title = None
    
    def Sim(self):
        result = self.rr.simulate(self.startTime, self.endTime, self.numberOfPoints, 
                             self.selection, integrator = self.integrator)
        return result            
    def plotArray(self):
        """Plots result of simulation with options for linewdith and line color"""
        result = self.Sim()
        
        if self.color is None:
            plt.plot(result[:,0], result[:,1:], linewidth = self.width)
        else: 
            plt.plot(result[:,0], result[:,1:], color = self.color, linewidth = self.width)    
        
        if self.ylabel is not None:
            plt.ylabel(self.ylabel) 
        if self.xlabel is not None:
            plt.xlabel(self.xlabel)
        if self.title is not None:
            plt.suptitle(self.title)
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
    
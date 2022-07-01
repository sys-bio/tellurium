"""
Extending the RoadRunner object with additional fields.
"""

from __future__ import print_function, division, absolute_import
import os
import roadrunner
import warnings
import copy
# ---------------------------------------------------------------------
# Extended RoadRunner class
# ---------------------------------------------------------------------
class ExtendedRoadRunner(roadrunner.RoadRunner):

    def __init__(self, *args, **kwargs):
        super(ExtendedRoadRunner, self).__init__(*args, **kwargs)

    # ---------------------------------------------------------------------
    # Model access
    # ---------------------------------------------------------------------
    # def getBoundarySpeciesConcentrations(self):
    #     return self.model.getBoundarySpeciesConcentrations()
    # getBoundarySpeciesConcentrations.__doc__ = roadrunner.ExecutableModel.getBoundarySpeciesConcentrations.__doc__

    # These model functions are attached after class creation
    _model_functions = [
        'getBoundarySpeciesIds',
        'getBoundarySpeciesConcentrationIds',
        'getBoundarySpeciesConcentrations',
        'getBoundarySpeciesAmounts',
        'getNumBoundarySpecies',

        'getFloatingSpeciesIds',
        'getFloatingSpeciesConcentrationIds',
        'getFloatingSpeciesConcentrations',
        'getFloatingSpeciesAmounts',
        'getNumFloatingSpecies',

        'getGlobalParameterIds',
        'getGlobalParameterValues',
        'getNumGlobalParameters',

        'getCompartmentIds',
        'getCompartmentVolumes',
        'getNumCompartments',

        'getConservedMoietyValues',
        'getNumConservedMoieties',

        'getReactionIds',
        'getReactionRates',
        'getNumReactions',
        'getNumEvents',
        'getNumRateRules'
     ]

    # ---------------------------------------------------------------------
    # Jarnac compatibility layer
    # ---------------------------------------------------------------------
    def fjac(self):
        return self.getFullJacobian()
    fjac.__doc__ = roadrunner.RoadRunner.getFullJacobian.__doc__

    def sm(self):
        return self.getFullStoichiometryMatrix()
    sm.__doc__ = roadrunner.RoadRunner.getFullStoichiometryMatrix.__doc__

    def rs(self):
        return self.model.getReactionIds()
    rs.__doc__ = roadrunner.ExecutableModel.getReactionIds.__doc__

    def fs(self):
        return self.model.getFloatingSpeciesIds()
    fs.__doc__ = roadrunner.ExecutableModel.getFloatingSpeciesIds.__doc__

    def bs(self):
        return self.model.getBoundarySpeciesIds()
    bs.__doc__ = roadrunner.ExecutableModel.getBoundarySpeciesIds.__doc__

    def ps(self):
        return self.model.getGlobalParameterIds()
    ps.__doc__ = roadrunner.ExecutableModel.getGlobalParameterIds.__doc__

    def vs(self):
        return self.model.getCompartmentIds()
    vs.__doc__ = roadrunner.ExecutableModel.getCompartmentIds.__doc__

    def dv(self):
        return self.getRatesOfChange()
    dv.__doc__ = roadrunner.RoadRunner.getRatesOfChange.__doc__

    def rv(self):
        return self.model.getReactionRates()
    rv.__doc__ = roadrunner.ExecutableModel.getReactionRates.__doc__

    def sv(self):
        return self.model.getFloatingSpeciesConcentrations()
    sv.__doc__ = roadrunner.ExecutableModel.getFloatingSpeciesConcentrations.__doc__

    # ---------------------------------------------------------------------
    # Export Utilities
    # ---------------------------------------------------------------------
    def __getSBML(self, current):
        if current is True:
            return self.getCurrentSBML()
        else:
            return self.getSBML()

    def getAntimony(self, current=False):
        """ Antimony string of the original model loaded into roadrunner.

        :param current: return current model state
        :type current: bool
        :return: Antimony
        :rtype: str
        """
        sbml = self.__getSBML(current)
        from .. import sbmlToAntimony
        return sbmlToAntimony(sbml)

    def getCurrentAntimony(self):
        """ Antimony string of the current model state.

        See also: :func:`getAntimony`
        :returns: Antimony string
        :rtype: str
        """
        return self.getAntimony(current=True)

    def getCellML(self, current=False):
        """ CellML string of the original model loaded into roadrunner.

        :param current: return current model state
        :type current: bool
        :returns: CellML string
        :rtype: str
        """
        sbml = self.__getSBML(current)
        from .. import sbmlToCellML
        return sbmlToCellML(sbml)

    def getCurrentCellML(self):
        """ CellML string of current model state.

        See also: :func:`getCellML`
        :returns: CellML string
        :rtype: str
        """
        return self.getCellML(current=True)

    def getMatlab(self, current=False):
        """ Matlab string of the original model loaded into roadrunner.

        See also: :func:`getCurrentMatlab`
        :returns: Matlab string
        :rtype: str
        """
        try:
            from sbml2matlab import sbml2matlab
            sbml = self.__getSBML(current)
            return sbml2matlab.sbml2matlab(sbml)
        except ImportError:
            warnings.warn("'sbml2matlab' could not be imported, no support for Matlab code generation",
                          RuntimeWarning, stacklevel=2)
            return ""

    def getCurrentMatlab(self):
        """ Matlab string of current model state.

        :param current: return current model state
        :type current: bool
        :returns: Matlab string
        :rtype: str
        """
        return self.getMatlab(current=True)

    def exportToSBML(self, filePath, current=True):
        """ Save current model as SBML file.

        :param current: export current model state
        :type current: bool
        :param filePath: file path of SBML file
        :type filePath: str
        """
        with open(filePath, 'w') as f:
            f.write(self.__getSBML(current))

    def exportToAntimony(self, filePath, current=True):
        """ Save current model as Antimony file.

        :param current: export current model state
        :type current: bool
        :param filePath: file path of Antimony file
        :type filePath: str
        """
        with open(filePath, 'w') as f:
            f.write(self.getAntimony(current))

    def exportToCellML(self, filePath, current=True):
        """ Save current model as CellML file.

        :param current: export current model state
        :type current: bool
        :param filePath: file path of CellML file
        :type filePath: str
        """
        with open(filePath, 'w') as f:
            f.write(self.getCellML(current))

    def exportToMatlab(self, filePath, current=True):
        """ Save current model as Matlab file.
        To save the original model loaded into roadrunner use
        current=False.

        :param self: RoadRunner instance
        :type self: RoadRunner.roadrunner
        :param filePath: file path of Matlab file
        :type filePath: str
        """
        with open(filePath, 'w') as f:
            f.write(self.getMatlab(current))

    # ---------------------------------------------------------------------
    # Plotting Utilities
    # ---------------------------------------------------------------------
    def draw(self, **kwargs):
        """ Draws an SBMLDiagram of the current model.

        To set the width of the output plot provide the 'width' argument.
        Species are drawn as white circles (boundary species
        shaded in blue), reactions as grey squares.
        Currently only the drawing of medium-size networks is supported.
        """
        import shutil
        # PATH variable may not be present - cannot use os.environ['PATH']
        # but can use shutil.which for Python 3.3+
        if hasattr(shutil, 'which'):
            if shutil.which('dot') is None:
                warnings.warn("Graphviz is not installed in your machine or could not be found. 'draw' command cannot produce a diagram.",
                    Warning, stacklevel=2)
                return
        elif not 'PATH' in os.environ or any([ os.access( os.path.join( p, 'dot' ), os.X_OK ) for p in os.environ['PATH'].split( os.pathsep )]):
            warnings.warn("Graphviz is not installed in your machine or could not be found. 'draw' command cannot produce a diagram.",
                Warning, stacklevel=2)
            return

        from tellurium import SBMLDiagram
        diagram = SBMLDiagram(self.getSBML())
        diagram.draw(**kwargs)


    def plot(self, result=None, show=True,
             xtitle=None, ytitle=None, title=None, linewidth=2, xlim=None, ylim=None, logx=False, logy=False,
             xscale='linear', yscale='linear', grid=False, ordinates=None, tag=None, labels=None, 
             figsize=(6,4), savefig=None, dpi=80, alpha=1.0, **kwargs):
        """ Plot roadrunner simulation data.

        Plot is called with simulation data to plot as the first argument. If no data is provided the data currently
        held by roadrunner generated in the last simulation is used. The first column is considered the x axis and
        all remaining columns the y axis.
        If the result array has no names, then the current r.selections are used for naming. In this case the
        dimension of the r.selections has to be the same like the number of columns of the result array.

        Curves are plotted in order of selection (columns in result).

        In addition to the listed keywords plot supports all matplotlib.pyplot.plot keyword arguments,
        like color, alpha, linewidth, linestyle, marker, ...
        ::

            sbml = te.getTestModel('feedback.xml')
            r = te.loadSBMLModel(sbml)
            s = r.simulate(0, 100, 201)
            r.plot(s, loc="upper right", linewidth=2.0, lineStyle='-', marker='o', markersize=2.0,
                   alpha=0.8, title="Feedback Oscillation", xlabel="time", ylabel="concentration",
                   xlim=[0,100], ylim=[-1, 4])

        :param result: results data to plot (numpy array)
        :param show: show=True (default) shows the plot, use show=False to plot multiple simulations in one plot
        :type show: bool
        :param xtitle: x-axis label
        :type xtitle: str
        :param xlabel: x-axis label (same as xtitle)
        :type xlabel: str
        :param ytitle: y-axis label
        :type ytitle: str
        :param ylabel: y-axis label (same as ytitle)
        :type ylabel: str
        :param title: plot title
        :type title: str
        :param linewidth: linewidth of the plot
        :type linewidth: float
        :param xlim: limits on x-axis (tuple [start, end])
        :param ylim: limits on y-axis
        :param logx: use log scale for x-axis
        :type logx: bool
        :param logy: use log scale for y-axis
        :type logy: bool
        :param xscale: 'linear' or 'log' scale for x-axis
        :param yscale: 'linear' or 'log' scale for y-axis
        :param grid: show grid
        :type grid: bool
        :param ordinates: If supplied, only these selections will be plotted (see RoadRunner selections)
        :param tag: If supplied, all traces with the same tag will be plotted with the same color/style
        :param labels: 'id' to use species IDs
        :param figsize: If supplied, customize the size of the figure (width,height)
        :param savefig: If supplied, saves the figure to specified location
        :type savefig: str
        :param dpi: Change the dpi of the saved figure
        :type dpi: int
        :param alpha: Change the alpha value of the figure
        :type alpha: float
        :param kwargs: additional matplotlib keywords like marker, lineStyle, ...
        """
        if result is None:
            simData = self.getSimulationData()
            result = copy.copy(simData)
            result.colnames = simData.colnames

        from .. import getPlottingEngine

        if xtitle:
            kwargs['xtitle'] = xtitle
        if ytitle:
            kwargs['ytitle'] = ytitle
        if title:
            kwargs['title'] = title
        if linewidth:
            kwargs['linewidth'] = linewidth
        if xlim:
            kwargs['xlim'] = xlim
        if ylim:
            kwargs['ylim'] = ylim
        if logx:
            kwargs['logx'] = logx
        if logy:
            kwargs['logy'] = logy
        if xscale:
            kwargs['xscale'] = xscale
        if yscale:
            kwargs['yscale'] = yscale
        if grid:
            kwargs['grid'] = grid
        if ordinates:
            kwargs['ordinates'] = ordinates
        if tag:
            kwargs['tag'] = tag
        if labels:
            kwargs['labels'] = labels
        if figsize:
            kwargs['figsize'] = figsize
        if savefig:
            kwargs['savefig'] = savefig
        if dpi:
            kwargs['dpi'] = dpi
        if alpha:
            kwargs['alpha'] = alpha            

        # FIXME: provide the additional parameters to the plotting engine

        engine = getPlottingEngine()
        if show:
            # show the plot immediately
            engine.plotTimecourse(result, **kwargs)
        else:
            # otherwise, accumulate the traces
            engine.accumulateTimecourse(result, **kwargs)

    def show(self, reset=True):
        """ Show plot. """
        from .. import getPlottingEngine
        getPlottingEngine().show(reset=reset)

    # ---------------------------------------------------------------------
    # Stochastic Simulation Methods
    # ---------------------------------------------------------------------
    def getSeed(self, integratorName="gillespie"):
        """ Current seed used by the integrator with integratorName.
        Defaults to the seed of the gillespie integrator.

        :param integratorName: name of the integrator for which the seed should be retured
        :type integratorName: str
        :returns: current seed
        :rtype: float
        """
        integrator = self.getIntegratorByName(integratorName)
        return integrator.getValue('seed')

    @property
    def seed(self):
        """ Getter for Gillespie seed. """
        return self.getSeed()

    def setSeed(self, seed, integratorName="gillespie"):
        """ Set seed in integrator with integratorName.
        Defaults to the seed of the gillespie integrator.

        Raises Error if integrator does not have key 'seed'.

        :param seed: seed to set
        :param integratorName: name of the integrator for which the seed should be retured
        :type integratorName: str
        """
        # there are some issues converting big Python (greater than 4,294,967,295) integers
        # to C integers on 64 bit machines. If its converted to float before, works around the issue.
        self.setIntegratorSetting(integratorName=integratorName, settingName="seed", value=float(seed))

    @seed.setter
    def seed(self, value):
        """ Setter for Gillespie seed. """
        return self.setSeed(value)

    def gillespie(self, *args, **kwargs):
        """ Run a Gillespie stochastic simulation.

        Sets the integrator to gillespie and performs simulation.
        ::

            rr = te.loada ('S1 -> S2; k1*S1; k1 = 0.1; S1 = 40')
            # Simulate from time zero to 40 time units using variable step sizes (classic Gillespie)
            result = rr.gillespie (0, 40)
            # Simulate on a grid with 10 points from start 0 to end time 40
            rr.reset()
            result = rr.gillespie (0, 40, 10)
            # Simulate from time zero to 40 time units using variable step sizes with given selection list
            # This means that the first column will be time and the second column species S1
            rr.reset()
            result = rr.gillespie (0, 40, selections=['time', 'S1'])
            # Simulate on a grid with 20 points from time zero to 40 time units
            # using the given selection list
            rr.reset()
            result = rr.gillespie (0, 40, 20, ['time', 'S1'])
            rr.plot(result)

        :param seed: seed for gillespie
        :type seed: int
        :param args: parameters for simulate
        :param kwargs: parameters for simulate
        :returns: simulation results
        """

        integratorName = self.integrator.getName()
        vss = self.integrator.variable_step_size
        if (integratorName != 'gillespie'):
            self.setIntegrator('gillespie')
            self.integrator.variable_step_size = True        
        if (len(args) > 3):
            self.integrator.variable_step_size = False
        if (len(args) == 3):
            if (type(args[2]) != list):
                self.integrator.variable_step_size = False
        elif ('points' in kwargs or 'steps' in kwargs):
            self.integrator.variable_step_size = False
        if "seed" in kwargs:
            self.integrator.setValue("seed", kwargs["seed"])
            del kwargs["seed"]

        s = self.simulate(*args, **kwargs)
        self.setIntegrator(integratorName)
        self.integrator.variable_step_size = vss
        return s

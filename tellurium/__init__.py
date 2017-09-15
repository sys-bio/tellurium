from __future__ import print_function, division, absolute_import

# ----------------------------------------------------------------
# TELLURIUM API
# ----------------------------------------------------------------

# General
from .tellurium import (
    getVersionInfo,
    printVersionInfo,
    getTelluriumVersion,
    noticesOff,
    noticesOn,
    )

# Converters
from .teconverters import (
    antimonyConverter,
    inlineOmex,
    )

# Model import
from .tellurium import (
    loadAntimonyModel,     # load antimony from string
    loada,                 # same as loadAntimonyModel
    loadSBMLModel,         # load sbml from string
    loads,                 # same as loadSBMLModel
    )

# Keeps a dictionary of loaded models
from .tellurium import (
    __set_model, # associates model name with roadrunner instance
    model,       # retrieve a roadrunner instance previously set with __set_model
    )

# Legacy import, use antimonyConverter
from .tellurium import (
    antimonyToSBML,
    sbmlToAntimony,
    )

# CellML converters
try:
    from .tellurium import (
        loadCellMLModel,
        antimonyToCellML,
        sbmlToCellML,
        cellmlToAntimony,
        cellmlToSBML,
        )
except ImportError:
    # CellML not available
    pass


# Plotting
from .tellurium import (
    plot,
    show,
    getPlottingEngine,
    getDefaultPlottingEngine,
    setDefaultPlottingEngine,
    setSavePlotsToPDF,
    )
# Legacy plotting
from .tellurium import (
    plotArray,
    plotWithLegend,
    )

# Test models
from .tellurium import (
    loadTestModel,
    getTestModel,
    listTestModels,
    )

# Latex
from .teio.latex import LatexExport


# Parameter scanning
from .analysis.parameterscan import (
    ParameterScan,
    SteadyStateScan,
    )

# Distributed computing
from .analysis.stochasticmodel import StochasticSimulationModel
from .analysis.parameterestimation import ParameterEstimation
from .analysis.sensitivityanalysis import SensitivityAnalysis

from .tellurium import (
    # distrib. parameter scan
    distributed_parameter_scanning, sample_plot, plotImage,
    # distrib. stochastic sims & fitting
    distributed_stochastic_simulation, plot_distributed_stochastic, plot_stochastic_result, distributed_sensitivity_analysis
    )

# Bifurcations
from .analysis.bifurcation import (
    plotBifurcation,
    )

# sedml support
from .sedml.tesedml import sedmlToPython, executeSEDML

# Combine archive support
from .tellurium import (
    convertCombineArchive,
    convertAndExecuteCombineArchive,
    extractFileFromCombineArchive,
    exportInlineOmex,
    executeInlineOmex,
    executeInlineOmexFromFile,
)


# Package utilities
from .package_utils import (
    searchPackage,
    installPackage,
    upgradePackage,
    uninstallPackage,
)

# Dist config
from .tellurium import (
    DumpJSONInfo,
    getAppDir,
    )

# SBML test cases
from .tellurium import (
    getSupportedTestCases,
    )

# SED-ML reports
from .tellurium import (
    setLastReport,
    getLastReport,
    )

# Do not use
# from .sedml.tephrasedml import experiment
# from .tecombine import combine

# Misc
from .tellurium import getEigenvalues

# Utilities
from .utils import (
    runTool,
    saveToFile,
    readFromFile,
    rank,
    nullspace,
    rref,
    )

# import .optimization  # nothing here

# display with graphviz
from .visualization import (
    SBMLDiagram,
    )

# import .tests         # needs to be refactored for Python 3

try:
    import temiriam
except ImportError:
    pass

# Needs to be checked for compatibility with latest Jupyter and Python 3
# import notebooks

__version__ = getTelluriumVersion()

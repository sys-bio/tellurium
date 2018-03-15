"""
Tellurium API definition.

The API functions are made available via imports from
the respective packages and modules.
"""
from __future__ import absolute_import

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
    loadAntimonyModel,
    loada,
    loadSBMLModel,
    loads,
)

# Dictionary of loaded models
from .tellurium import (
    __set_model,  # associates model name with roadrunner instance
    model,        # retrieve a roadrunner instance previously set with __set_model
)

# Legacy import, use antimonyConverter
from .tellurium import (
    antimonyToSBML,
    sbmlToAntimony,
)

# CellML support
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
    nextFigure,
    tiledFigure,
    newTiledFigure,
    newLowerTriFigure,
    clearTiledFigure,
    getDefaultPlottingEngine,
    setDefaultPlottingEngine,
    disablePlotting,
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
    distributed_parameter_scanning, sample_plot, plotImage,
    distributed_stochastic_simulation, plot_distributed_stochastic, plot_stochastic_result, distributed_sensitivity_analysis
)

# Bifurcations
from .analysis.bifurcation import (
    plotBifurcation,
)

# SED-ML support
from .sedml.tesedml import sedmlToPython, executeSEDML, executeCombineArchive

# Combine archive support
from .tellurium import (
    addFileToCombineArchive,
    addFilesToCombineArchive,
    convertCombineArchive,
    convertAndExecuteCombineArchive,
    extractFileFromCombineArchive,
    exportInlineOmex,
    executeInlineOmex,
    executeInlineOmexFromFile,
)

# Package utilities
from tellurium.utils.package import (
    searchPackage,
    installPackage,
    upgradePackage,
    uninstallPackage,
)
from tellurium.utils.misc import(
    saveToFile,
    readFromFile,
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

# Eigenvalues
from .tellurium import getEigenvalues

# SBML diagram with graphviz
from .visualization import (
    SBMLDiagram,
)

__version__ = getTelluriumVersion()

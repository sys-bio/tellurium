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
    saveToFile,
    readFromFile,
    )

# Converters
from .teconverters import (
    antimonyConverter,
    partitionInlineOMEXString, # partition an inline omex string into phrasedml and antimony parts
    inlineOmex,
    )

# Model import
from .tellurium import (
    __set_model, # associates model name with roadrunner instance
    model,       # retrieve a roadrunner instance previously set with __set_model
    )

from .tellurium import (
    loada,             # load antimony
    loadAntimonyModel, # same as loada
    loads,             # load sbml
    loadSBMLModel,     # same as loads
    )

# Legacy import, use antimonyConverter
from .tellurium import antimonyToSBML
from .tellurium import sbmlToAntimony

# CellML converters
if hasattr(tellurium, 'loadCellMLModel'):
    from .tellurium import (
        loadCellMLModel,
        antimonyToCellML,
        sbmlToCellML,
        cellmlToAntimony,
        cellmlToSBML,
        )

from .tellurium import getEigenvalues

# Plotting
from .tellurium import (
    getPlottingEngine,
    getDefaultPlottingEngine,
    setDefaultPlottingEngine,
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

# helper classes
from .teio.latex import LatexExport
from .analysis.parameterscan import ParameterScan, SteadyStateScan

# sedml & combine support
from .sedml.tesedml import sedmlToPython, executeSEDML, executeOMEX
# from .sedml.tephrasedml import experiment
#from .tecombine import combine

# try:
#     import tellurium.optimization
#     import tellurium.visualization
#     import tellurium.tests
# except ImportError:
#     import optimization
#     import visualization
#     import tests

try:
    import temiriam
except ImportError:
    pass
#import notebooks

__version__ = getTelluriumVersion()

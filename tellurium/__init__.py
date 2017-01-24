# ----------------------------------------------------------------
# TELLURIUM API
# ----------------------------------------------------------------
# make explicit imports to avoid namespace pollution
from .tellurium import getVersionInfo
from .tellurium import printVersionInfo
from .tellurium import getTelluriumVersion
from .tellurium import noticesOff
from .tellurium import noticesOn
from .tellurium import saveToFile
from .tellurium import readFromFile

from .tellurium import loada
from .tellurium import loadAntimonyModel
from .tellurium import loads

from .tellurium import loadSBMLModel
from .tellurium import antimonyToSBML
from .tellurium import sbmlToAntimony

if hasattr(tellurium, 'loadCellMLModel'):
    from .tellurium import loadCellMLModel
    from .tellurium import antimonyToCellML
    from .tellurium import sbmlToCellML
    from .tellurium import cellmlToAntimony
    from .tellurium import cellmlToSBML

from .tellurium import getEigenvalues
from .tellurium import plotArray
from .tellurium import plotWithLegend
from .tellurium import loadTestModel
from .tellurium import getTestModel
from .tellurium import listTestModels

# helper classes
from .teio.latex import LatexExport
#from .analysis.parameterscan import ParameterScan, SteadyStateScan

# sedml & combine support
#from .sedml.tesedml import sedmlToPython, executeSEDML, executeOMEX
#from .sedml.tephrasedml import experiment
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
import notebooks

__version__ = getTelluriumVersion()

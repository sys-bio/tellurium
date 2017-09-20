"""
Example Running the Combine Showcase Archive.

https://github.com/SemsProject/CombineArchiveShowCase
"""

# TODO: FIXME: import omex from test data

# TODO: create results dir

# redirect backend, so plots only in files and not shown
import matplotlib.pyplot
matplotlib.pyplot.switch_backend("Agg")

# running all SED-ML simulations in archive
# outputs are stored next to the respective SED-ML files in the workingDir
import os.path
from tellurium.sedml.tesedml import executeOMEX, executeSEDML

omexDir = os.path.dirname(os.path.realpath(__file__))
omexPath = os.path.join(omexDir, "CombineArchiveShowCase.omex")
workingDir = os.path.join(omexDir, "./results/_te_CombineArchiveShowCase")

executeOMEX(omexPath, workingDir=workingDir)

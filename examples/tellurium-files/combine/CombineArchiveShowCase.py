"""
Running the Combine Showcase.
https://github.com/SemsProject/CombineArchiveShowCase
"""

# redirect backend, so plots only in files and not shown
import matplotlib.pyplot
matplotlib.pyplot.switch_backend("Agg")

# running all SED-ML simulations in archive
# outputs are stored next to the respective SED-ML files in the workingDir
import os.path
import tellurium as te

omexDir = os.path.dirname(os.path.realpath(__file__))
omexPath = os.path.join(omexDir, "CombineArchiveShowCase.omex")
workingDir = os.path.join(omexDir, "_te_CombineArchiveShowCase")

te.executeOMEX(omexPath, workingDir=workingDir)

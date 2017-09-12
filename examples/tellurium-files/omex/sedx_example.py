"""
Example running sedx examples.
"""


# redirect backend, so plots only in files and not shown
# import matplotlib.pyplot
# matplotlib.pyplot.switch_backend("Agg")

# running all SED-ML simulations in archive
# outputs are stored next to the respective SED-ML files in the workingDir
import os.path
from tellurium.sedml.tesedml import executeOMEX, executeSEDML

omexDir = os.path.dirname(os.path.realpath(__file__))
omexPath = os.path.join(omexDir, "sedx_files/wodarz2007_fig1-user_hr5XMv9.sedx")
workingDir = os.path.join(omexDir, "./results/_te_wodarz2007_fig1-user_hr5XMv9")

executeOMEX(omexPath, workingDir=workingDir)
# executeSEDML(omexPath, workingDir=workingDir)

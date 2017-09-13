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

# L1V3 non-conform data
# omexPath = os.path.join(omexDir, "sedx_files/kouril3_experiment-user_EqhV27r.sedx")
# workingDir = os.path.join(omexDir, "./results/_te_kouril3_experiment-user_EqhV27r")

# omexPath = os.path.join(omexDir, "sedx_files/chan2004_fig3_ojaH5KH.sedx")
# workingDir = os.path.join(omexDir, "./results/_te_chan2004_fig3_ojaH5KH.sedx")

omexPath = os.path.join(omexDir, "sedx_files/test_2d-parameter-scan.sedx")
workingDir = os.path.join(omexDir, "./results/_te_test_2d-parameter-scan")


executeOMEX(omexPath, workingDir=workingDir)
# executeSEDML(omexPath, workingDir=workingDir)

# -*- coding: utf-8 -*-
"""
Use Biomodels in phrasedml.

Example is the introduction example for the SED-ML specification.
Model is repressilator.
"""
from __future__ import print_function
import os
import tellurium as te
from tellurium import temiriam
import phrasedml
print('phrasedml version:', phrasedml.__version__)

# Get SBML from URN and set for phrasedml
urn = "urn:miriam:biomodels.db:BIOMD0000000012"
sbml_str = temiriam.getSBMLFromBiomodelsURN(urn=urn)
return_code = phrasedml.setReferencedSBML(urn, sbml_str)
print('valid SBML', return_code)

# <SBML species>
#   PX - LacI protein
#   PY - TetR protein
#   PZ - cI protein
#   X - LacI mRNA
#   Y - TetR mRNA
#   Z - cI mRNA

# <SBML parameters>
#   ps_a - tps_active: Transcription from free promotor in transcripts per second and promotor
#   ps_0 - tps_repr: Transcription from fully repressed promotor in transcripts per second and promotor

phrasedml_str = """
    model1 = model "{}"
    model2 = model model1 with ps_0=1.3E-5, ps_a=0.013
    sim1 = simulate uniform(0, 1000, 1000)
    task1 = run sim1 on model1
    task2 = run sim1 on model2

    # A simple timecourse simulation
    plot "Figure 1.1 Timecourse of repressilator" task1.time vs task1.PX, task1.PZ, task1.PY

    # Applying preprocessing
    plot "Figure 1.2 Timecourse after pre-processing" task2.time vs task2.PX, task2.PZ, task2.PY

    # Applying postprocessing
    plot "Figure 1.3 Timecourse after post-processing" task1.PX/max(task1.PX) vs task1.PZ/max(task1.PZ), \
                                                       task1.PY/max(task1.PY) vs task1.PX/max(task1.PX), \
                                                       task1.PZ/max(task1.PZ) vs task1.PY/max(task1.PY)
""".format(urn)

# convert to SED-ML (this worked before, but does not anymore)

sedml_str = phrasedml.convertString(phrasedml_str)
if sedml_str is None:
    print(phrasedml.getLastError())
else:
    print(sedml_str)

# execution: not possible to execute the phrasedml as inline_omex
inline_omex = phrasedml_str
te.executeInlineOmex(inline_omex)
te.exportInlineOmex(inline_omex, os.path.join('.', 'repressilator.omex'))


'''

# Run the SED-ML file with results written in workingDir
import tempfile
import shutil
workingDir = tempfile.mkdtemp(suffix="_sedml")
te.executeSEDML(sedmlStr, workingDir=workingDir)
shutil.rmtree(workingDir)


# [2] store as combine archive and run
import os
from tellurium.tecombine import CombineArchive
combine = CombineArchive()
combine.addSEDMLStr(sedmlStr, 'specificationL1V2.sedml')
from tellurium.tests.testdata import sedxDir
combinePath = os.path.join(sedxDir, 'specificationL1V2.omex')
combine.write(combinePath)

# Run Combine archive
te.executeSEDML(combinePath)

# remove sedx (not hashable due to timestamp)
# os.remove(combinePath)


inline_omex = phrasedml_str
te.executeInlineOmex(inline_omex)
te.exportInlineOmex(inline_omex, os.path.join(tmpdir, 'archive.omex'))
        shutil.rmtree(tmpdir)
'''
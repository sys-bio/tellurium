# -*- coding: utf-8 -*-
"""
Use Biomodels in phrasedml.

Example is the introduction example for the SED-ML specification.
Model is repressilator.
"""

from __future__ import absolute_import, print_function
import os
import tempfile
import shutil

from tellurium import temiriam
from tellurium.sedml.tesedml import executeCombineArchive, executeSEDML
from tellurium.utils import omex
import phrasedml

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
    plot "Timecourse of repressilator" task1.time vs task1.PX, task1.PZ, task1.PY

    # Applying preprocessing
    plot "Timecourse after pre-processing" task2.time vs task2.PX, task2.PZ, task2.PY

    # Applying postprocessing
    plot "Timecourse after post-processing" task1.PX/max(task1.PX) vs task1.PZ/max(task1.PZ), \
                                                       task1.PY/max(task1.PY) vs task1.PX/max(task1.PX), \
                                                       task1.PZ/max(task1.PZ) vs task1.PY/max(task1.PY)
""".format(urn)

# convert to sedml
sedml_str = phrasedml.convertString(phrasedml_str)
if sedml_str is None:
    print(phrasedml.getLastError())
    raise IOError("sedml could not be generated")

# run SEDML directly
try:
    tmp_dir = tempfile.mkdtemp()
    executeSEDML(sedml_str, workingDir=tmp_dir)
finally:
    shutil.rmtree(tmp_dir)


# create combine archive and execute
try:
    tmp_dir = tempfile.mkdtemp()
    sedml_location = "repressilator_sedml.xml"
    sedml_path = os.path.join(tmp_dir, sedml_location)
    omex_path = os.path.join(tmp_dir, "repressilator.omex")
    with open(sedml_path, "w") as f:
        f.write(sedml_str)

    entries = [
        omex.Entry(location=sedml_location, formatKey="sedml", master=True)
    ]
    omex.combineArchiveFromEntries(omexPath=omex_path, entries=entries, workingDir=tmp_dir)
    executeCombineArchive(omex_path, workingDir=tmp_dir)

finally:
    shutil.rmtree(tmp_dir)

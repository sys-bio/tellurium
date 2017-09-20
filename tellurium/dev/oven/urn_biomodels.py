import roadrunner
from tellurium.temiriam import getSBMLFromBiomodelsURN


print("Get SBML from URN")
# urn = 'urn:miriam:biomodels.db:BIOMD0000000003'
urn = 'urn:miriam:biomodels.db:BIOMD0000000139'
sbml = getSBMLFromBiomodelsURN(urn)
print(sbml)
print(type(sbml))

import roadrunner
r = roadrunner.RoadRunner(sbml)
print(r)

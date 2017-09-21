import os

testDir = os.path.dirname(os.path.realpath(__file__))
sedmlDir = os.path.join(testDir, 'sedml', 'sed-ml')
omexDir = os.path.join(testDir, 'sedml', 'omex')


OMEX_SHOWCASE = os.path.join(omexDir, "CombineArchiveShowCase.omex")
FEEDBACK_SBML = os.path.join(testDir, 'models/feedback.xml')

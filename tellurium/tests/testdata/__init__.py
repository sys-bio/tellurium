import os

testDir = os.path.dirname(os.path.realpath(__file__))
sedmlDir = os.path.join(testDir, 'sedml', 'sed-ml')
sedxDir = os.path.join(testDir, 'sedml', 'sedx')

FEEDBACK_SBML = os.path.join(testDir, 'models/feedback.xml')

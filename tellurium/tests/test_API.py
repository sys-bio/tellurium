"""
Here the supported API is tested.
"""
# TODO: write in file
from __future__ import print_function, division
import unittest

import tellurium as te
r = te.loada('''
  model pathway()
    S1 + S2 -> 2 S3; k1*S1*S2
    3 S3 -> 4 S4 + 6 S5; k2*S3^3
    k1 = 0.1;k2 = 0.1;
  end
''')

# ----------------------------------------------------------------
# SUPPORTED API v1.3.0
# ----------------------------------------------------------------
api_calls = [
    # <te>
    #   utility functions
    'te.getVersionInfo',
    'te.printVersionInfo',
    'te.getTelluriumVersion',
    'te.noticesOff',
    'te.noticesOn',
    'te.saveToFile',
    'te.readFromFile',
    #   load methods
    'te.loada',
    'te.loadAntimonyModel',
    'te.loadSBMLModel',
    'te.loadCellMLModel',
    #   conversion methods
    'te.antimonyToSBML',
    'te.antimonyToCellML',
    'te.sbmlToAntimony',
    'te.sbmlToCellML',
    'te.cellmlToAntimony',
    'te.cellmlToSBML',
    #   experiment
    'te.experiment',
    #   math
    'te.getEigenvalues',
    #   plotting
    'te.plotArray',
    #   tests
    'te.loadTestModel',
    'te.getTestModel',
    'te.listTestModels',
    #   export
    'te.LatexExport',
    #   scans
    'te.ParameterScan',
    'te.SteadyStateScan',
    # <ExtendedRoadRunner>
    'r.getAntimony',
    'r.getCurrentAntimony',
    'r.getCellML',
    'r.getCurrentCellML',
    'r.getMatlab',
    'r.getCurrentMatlab',
    'r.exportToAntimony',
    'r.exportToCellML',
    'r.exportToMatlab',
    'r.resetToOrigin',
    'r.resetAll',
    'r.getRatesOfChange',
    'r.draw',
    'r.plot',
    'r.getSeed',
    'r.setSeed',
    'r.gillespie',
    #   jarnac layer
    'r.fjac',
    'r.sm',
    'r.rs',
    'r.fs',
    'r.bs',
    'r.ps',
    'r.vs',
    'r.dv',
    'r.rv',
    'r.sv',
    #   model functions
    'r.getBoundarySpeciesConcentrations',
    'r.getBoundarySpeciesIds',
    'r.getNumBoundarySpecies',
    'r.getFloatingSpeciesConcentrations',
    'r.getFloatingSpeciesIds',
    'r.getNumFloatingSpecies',
    'r.getGlobalParameterIds',
    'r.getGlobalParameterValues',
    'r.getNumGlobalParameters',
    'r.getCompartmentIds',
    'r.getCompartmentVolumes',
    'r.getNumCompartments',
    'r.getConservedMoietyValues',
    'r.getNumConservedMoieties',
    'r.getNumDepFloatingSpecies',
    'r.getNumIndFloatingSpecies',
    'r.getReactionIds',
    'r.getReactionRates',
    'r.getNumReactions',
    'r.getNumEvents',
    'r.getNumRateRules',
]
# ----------------------------------------------------------------




class APITestCase(unittest.TestCase):
    pass


# ----------------------------------------------------------------
# Dynamic generation of tests
# ----------------------------------------------------------------
def ftest_generator(name):
    def test(self=None):
        """ Test fails if class or function is not callable under the given name str. """
        if self is not None:
            f = eval(name)
            # test if exist
            self.assertIsNotNone(f)
            # test if callable
            self.assertTrue(hasattr(f, '__call__'))

    return test

for k, name in enumerate(api_calls):
    test_name = 'test_api{:03d}_{}'.format(k, name)
    test = ftest_generator(name)
    setattr(APITestCase, test_name, test)


if __name__ == "__main__":
    unittest.main()


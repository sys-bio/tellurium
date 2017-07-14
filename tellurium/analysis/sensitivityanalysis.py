class SensitivityAnalysis(object):
    def __init__(self,model=None,sbml=False,conservedMoietyAnalysis=True):
        self._model = model
        self._sbml = sbml
        self._conservedMoietyAnalysis = conservedMoietyAnalysis
        self._filename = None
        self._simulation = None
        self._bounds = None
        self._args = None
        self._allowLog = False


    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @model.deleter
    def model(self):
        del self._model

    @property
    def sbml(self):
        return self._sbml

    @sbml.setter
    def sbml(self, value):
        self._sbml = value

    @sbml.deleter
    def sbml(self):
        del self._sbml

    @property
    def conservedMoietyAnalysis(self):
        return self._conservedMoietyAnalysis

    @conservedMoietyAnalysis.setter
    def conservedMoietyAnalysis(self, value):
        self._conservedMoietyAnalysis = value

    @conservedMoietyAnalysis.deleter
    def conservedMoietyAnalysis(self):
        del self._conservedMoietyAnalysis


    @property
    def simulation(self):
        return self._simulation

    @simulation.setter
    def simulation(self, value):
        self._simulation = value

    @simulation.deleter
    def simulation(self):
        del self._simulation


    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @filename.deleter
    def filename(self):
        del self._filename


    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        self._bounds = value

    @bounds.deleter
    def bounds(self):
        del self._bounds

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @args.deleter
    def args(self):
        del self._args

    @property
    def allowLog(self):
        return self._allowLog

    @allowLog.setter
    def allowLog(self, value):
        self._allowLog = value

    @allowLog.deleter
    def allowLog(self):
        del self._allowLog




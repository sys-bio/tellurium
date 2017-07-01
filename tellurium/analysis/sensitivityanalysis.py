class SensitivityAnalysis(object):
    def __init__(self,model=None,sbml=False,conservedMoietyAnalysis=True):
        self._model = model
        self._sbml = sbml
        self._conservedMoietyAnalysis = conservedMoietyAnalysis
        self._preprocessingFunc = None
        self._bounds = None
        self._args = None


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
    def preprocessingFunc(self):
        return self._preprocessingFunc

    @preprocessingFunc.setter
    def preprocessingFunc(self, value):
        self._preprocessingFunc = value

    @preprocessingFunc.deleter
    def preprocessingFunc(self):
        del self._preprocessingFunc


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


    def setPreProcessingFunction(self,func,*args):
        self._preprocessingFunc = func
        self._args = args


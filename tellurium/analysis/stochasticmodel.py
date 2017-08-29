
class StochasticSimulationModel (object) :
    def __init__(self,model=None,
                 integrator="gillespie",
                 seed=1234,
                 variable_step_size = False,
                 from_time=0,
                 to_time=40,
                 step_points=50):

        self._model = model
        self._integrator = integrator
        self._seed = seed
        self._variable_step_size = variable_step_size
        self._from_time = from_time
        self._to_time = to_time
        self._step_points = step_points

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
    def integrator(self):
        return self._integrator

    @integrator.setter
    def integrator(self, value):
        self._integrator = value

    @integrator.deleter
    def integrator(self):
        del self._integrator

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value

    @seed.deleter
    def seed(self):
        del self._seed

    @property
    def variable_step_size(self):
        return self._variable_step_size

    @variable_step_size.setter
    def variable_step_size(self, value):
        self._variable_step_size = value

    @variable_step_size.deleter
    def variable_step_size(self):
        del self._variable_step_size

    @property
    def from_time(self):
        return self._from_time

    @from_time.setter
    def from_time(self, value):
        self._from_time = value

    @from_time.deleter
    def from_time(self):
        del self._from_time

    @property
    def to_time(self):
        return self._to_time

    @to_time.setter
    def to_time(self, value):
        self._to_time = value

    @to_time.deleter
    def to_time(self):
        del self._to_time

    @property
    def step_points(self):
        return self._step_points

    @step_points.setter
    def step_points(self, value):
        self._step_points = value

    @step_points.deleter
    def step_points(self):
        del self._step_points


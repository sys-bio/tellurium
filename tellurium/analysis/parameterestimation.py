import csv
import numpy as np
import tellurium as te
from scipy.optimize import differential_evolution
import random

class ParameterEstimation(object):

    def __init__(self, stochastic_simulation_model,bounds, data=None, func="differential_evolution"):
        if(data is not None):
            self.data = data

        self.model = stochastic_simulation_model
        self.bounds = bounds
        self.func = func


    def setDataFromCSV(self,FILENAME, delimiter=",", headers=True):
        with open(FILENAME,'r') as dest_f:
            data_iter = csv.reader(dest_f,
                                   delimiter = ",",
                                   quotechar = '"')
            self.data = [data for data in data_iter]
        if(headers):
            self.data = self.data[1:]

        self.data = np.asarray(self.data, dtype = float)

    def run(self):
        self._kinetic_rate_names = self.bounds.keys()
        self._kinetic_rate_bounds = self.bounds.values()
        self._model_roadrunner = te.loada(self.model.model)
        x_data = self.data[:,0]
        y_data = self.data[:,1:]
        arguments = (x_data,y_data)

        if(self.func.lower() == "differential_evolution"):
            result = differential_evolution(self._SSE, self._kinetic_rate_bounds, args=arguments)
            print(result.x)
        else:
            print "Function Not Defined"

    def _set_theta_values(self, theta):
        for theta_i,each_theta in enumerate(self._kinetic_rate_names):
            setattr(self._model_roadrunner, each_theta, theta[theta_i])


    def _SSE(self,parameters, *data):
        theta = parameters

        x, y = data
        sample_x, sample_y = data
        self._set_theta_values(theta)

        random.seed()
        # it is now safe to use random.randint
        #self._model.setSeed(random.randint(1000, 99999))

        self._model_roadrunner.integrator.variable_step_size = self.model.variable_step_size
        self._model_roadrunner.reset()
        simulated_data = self._model_roadrunner.simulate(self.model.from_time, self.model.to_time,
                                                                        self.model.step_points)

        simulated_data = np.array(simulated_data)
        simulated_x = simulated_data[:,0]
        simulated_y = simulated_data[:,1:]

        SEARCH_BEGIN_INDEX = 0
        SSE_RESULT = 0

        for simulated_i in range(len(simulated_y)):
            y_i = simulated_y[simulated_i]
            #yhat_i = sample_y[simulated_i]

            x_i = simulated_x[simulated_i]
            for search_i in range(SEARCH_BEGIN_INDEX+1,len(sample_x)):
                if(sample_x[search_i-1] <= x_i < sample_x[search_i]):
                    yhat_i = sample_y[search_i-1]
                    break
                SEARCH_BEGIN_INDEX += 1

            partial_result = 0
            for sse_i in range(len(y_i)):
                partial_result += (float(y_i[sse_i]) - float(yhat_i[sse_i])) ** 2
            SSE_RESULT += partial_result

        return SSE_RESULT ** 0.5


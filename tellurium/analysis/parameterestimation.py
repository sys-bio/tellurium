"""
Parameter estimation in tellurium.
"""
from __future__ import print_function, absolute_import
import csv
import numpy as np
import tellurium as te
from scipy.optimize import differential_evolution
import random


class ParameterEstimation(object):
    def __init__(self, stochastic_simulation_model, bounds, species=None, data=None, stochastic=False, sc=None,
                 allow_log=False, func=None):
        self._model = stochastic_simulation_model
        self._bounds = bounds
        self._species = species
        self._data = data
        self._stochastic = stochastic
        self._sc = sc
        self._allow_log = allow_log
        self._func = func
        self._collected_values = np.array([])
        self.validate_parameters()


    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value
        self.validate_parameters()

    @model.deleter
    def model(self):
        del self._model

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, value):
        self._bounds = value
        self.validate_parameters()

    @bounds.deleter
    def bounds(self):
        del self._bounds

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        self._species = value
        self.validate_parameters()

    @species.deleter
    def species(self):
        del self._species

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.validate_parameters()

    @data.deleter
    def data(self):
        del self._data

    @property
    def stochastic(self):
        return self._stochastic

    @stochastic.setter
    def stochastic(self, value):
        self._stochastic = value

    @stochastic.deleter
    def stochastic(self):
        del self._stochastic

    @property
    def sc(self):
        return self._sc

    @sc.setter
    def sc(self, value):
        self._sc = value
        self.validate_parameters()

    @sc.deleter
    def sc(self):
        del self._sc

    @property
    def allow_log(self):
        return self._allow_log

    @allow_log.setter
    def allow_log(self, value):
        self._allow_log = value
        self.validate_parameters()

    @allow_log.deleter
    def allow_log(self):
        del self._allow_log

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, value):
        self._func = value


    @func.deleter
    def func(self):
        del self._func

    def validate_parameters(self):
        if(self._stochastic):
            if self._sc is None:
                raise ValueError('If you want to run it in a distributed mode, provide spark context')
        if(self._allow_log):
            for each_parameter in self._bounds.keys():
                _begin = self._bounds[each_parameter][0]*1.0
                _end = self._bounds[each_parameter][1]*1.0
                self._bounds[each_parameter] = tuple(np.logspace(_begin,_end, num=2))





    def run(self, func=None):
        """
        Allows the user to set the data from a File
        This data is to be compared with the simulated data in the process of parameter estimation

        Args:
            func: An Optional Variable with default value (None) which by default run differential evolution
                which is from scipy function. Users can provide reference to their defined function as argument.


        Returns:
            The Value of the parameter(s) which are estimated by the function provided.

        .. sectionauthor:: Shaik Asifullah <s.asifullah7@gmail.com>

        """

        self._parameter_names = self._bounds.keys()
        self._parameter_bounds = self._bounds.values()
        self._model_roadrunner = te.loada(self._model.model)

        if self._data is None:
            raise ValueError('Data is not available. Set the data using setDataFromFile method')
            return
        else:
            # Pre-computed data provided by the user
            x_axis_time = self._data[:, 0]
            y_axis_values = self._data[:, 1:]
            arguments = (x_axis_time, y_axis_values)

        if (self._func is None): # Then Differential Evolution is used (default)
            result = differential_evolution(self._SSE, self._parameter_bounds, args=arguments,maxiter=500)

        else:
            result = func(self._SSE, self._parameter_bounds, args=arguments)

        metrics = {
            "Parameters": self._parameter_names,
            "Average SSE": self._collected_values.mean(0),
            "estimated_value": result.x
        }
        self._collected_values = np.array([])
        return (metrics)

    def setDataFromFile(self, FILENAME, delimiter=",", headers=True):
        """Allows the user to set the data from a File
        This data is to be compared with the simulated data in the process of parameter estimation

        Args:
            FILENAME: A Complete/relative readable Filename with proper permissions
            delimiter: An Optional variable with comma (",") as default value.
                A delimiter with which the File is delimited by.
                It can be Comma (",") , Tab ("\t") or anyother thing
            headers: Another optional variable, with Boolean True as default value
                If headers are not available in the File, it can be set to False

        Returns:
            None but sets class Variable data with the data provided

        .. sectionauthor:: Shaik Asifullah <s.asifullah7@gmail.com>


        """
        with open(FILENAME, 'r') as dest_f:
            data_iter = csv.reader(dest_f,
                                   delimiter=",",
                                   quotechar='"')
            self._data = [data for data in data_iter]
        if (headers):
            self._species = self._data[0]
            self._data = self._data[1:]

        self._data = np.asarray(self._data, dtype=float)

    def _set_theta_values(self, theta):
        """ Sets the Theta Value in the range of bounds provided to the Function.
            Not intended to be called by user.

        Args:
            theta: The Theta Value that is set for the function defined/provided


        Returns:
            None but it sets the parameter(s) to the stochastic model provided

        .. sectionauthor:: Shaik Asifullah <s.asifullah7@gmail.com>


        """
        for theta_i, each_theta in enumerate(self._parameter_names):
            setattr(self._model_roadrunner, each_theta, theta[theta_i])



    def _SSE(self,parameters, *data):
        """ Runs a simuation of SumOfSquares that get parameters and data and compute the metric.
            Not intended to be called by user.

        Args:
            parameters: The tuple of theta values  whose output is compared against the data provided
            data: The data provided by the user through FileName or manually
                  which is used to compare against the simulations


        Returns:
            Sum of Squared Error

        .. sectionauthor:: Shaik Asifullah <s.asifullah7@gmail.com>


        """
        theta = parameters

        sample_x, sample_y = data
        self._set_theta_values(theta)

        random.seed()


        self._model_roadrunner.integrator.variable_step_size = self._model.variable_step_size
        self._model_roadrunner.reset()

        try: # the simulation may fail
            if(not self._stochastic):
                simulated_data = self._model_roadrunner.simulate(self._model.from_time, self.model.to_time,
                                                                           self._model.step_points)
                if (self._species is not None):
                    # Check it the concentration in eclosed in Square brackets
                    try:
                        simulated_data = [simulated_data[colname] for colname in self.species]

                    except:
                        simulated_data = [
                            simulated_data["[" + colname + "]"] if colname != "time" else simulated_data["time"] for
                            colname in self.species]

                simulated_data = np.array(simulated_data)
                simulated_x = simulated_data[0]
                simulated_y = simulated_data[1:].T

            else:

                stoch_model = self._model
                spark_context = self._sc
                result = spark_context.parallelize([stoch_model] * 20, 20).map(stochastic_sim).collect()
                col_names = result[0][0]
                sim_result = np.array([item[1] for item in result])
                mean_result = sim_result.mean(0)


                if(self._species is not None):
                    col_indices = []
                    selected_species = set(col_names)
                    for each_comp in self._species:

                        if "["+each_comp+"]" in selected_species:
                            col_indices.append(col_names.index("["+each_comp+"]"))
                        elif each_comp in selected_species:
                            col_indices.append(col_names.index(each_comp))
                        else:
                            continue
                    simulated_x = mean_result[:,0]
                    if 0 in col_indices:
                        col_indices.remove(0)
                    simulated_y = mean_result[:,col_indices]
                else:
                    simulated_x = mean_result[:,0]
                    simulated_y = mean_result[:,1:]


        except: # if it does fail, need to apply a large penalty
            return 10000000.




        SEARCH_BEGIN_INDEX = 0
        SSE_RESULT = 0

        total_observations = 0

        for simulated_i in range(len(simulated_y)):
            y_i = simulated_y[simulated_i]
            yhat_i = None
            x_i = simulated_x[simulated_i]
            for search_i in range(SEARCH_BEGIN_INDEX+1,len(sample_x)):
                if(sample_x[search_i-1] <= x_i < sample_x[search_i]):
                    yhat_i = sample_y[search_i-1]
                    break
                SEARCH_BEGIN_INDEX += 1

            #If the bounds are not found for the X to be searched, the last
            # value will be used for comparision
            if(yhat_i is None and SEARCH_BEGIN_INDEX >= len(sample_x)-1):
                yhat_i = sample_y[-1]



            partial_result = 0
            for sse_i in range(len(y_i)):
                partial_result += (float(y_i[sse_i]) - float(yhat_i[sse_i])) ** 2
            SSE_RESULT += partial_result
            total_observations += len(y_i)

        final_result = (SSE_RESULT / total_observations) ** 0.5
        self._collected_values = np.append(self._collected_values,final_result)
        print(final_result)
        return final_result

def stochastic_sim(model_object):
    import tellurium as te
    model_roadrunner = te.loada(model_object.model)
    model_roadrunner.integrator = model_object.integrator
    # seed the randint method with the current time
    random.seed()
    # it is now safe to use random.randint
    model_roadrunner.setSeed(random.randint(1000, 99999))
    model_roadrunner.integrator.variable_step_size = model_object.variable_step_size
    model_roadrunner.reset()
    simulated_data = model_roadrunner.simulate(model_object.from_time, model_object.to_time,
                                               model_object.step_points)
    return ([simulated_data.colnames, np.array(simulated_data)])







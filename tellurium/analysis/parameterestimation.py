"""
Parameter estimation in tellurium.
"""
from __future__ import print_function, absolute_import
import csv
import numpy as np
import tellurium as te
from scipy.optimize import differential_evolution
import random
import pandas


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


    def _handle_allow_log(self):
        if self._allow_log:
            for each_parameter in self._bounds.keys():
                _begin = self._bounds[each_parameter][0]*1.0
                _end = self._bounds[each_parameter][1]*1.0
                self._bounds[each_parameter] = tuple(np.logspace(_begin,_end, num=2))


    def run(self, func=None, **kwargs):
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

        if self._data is None:
            raise ValueError('Data is not available. Set the data using setDataFromFile method')
            return

        self._handle_allow_log()
        self._parameter_names = self._bounds.keys()
        self._parameter_bounds = self._bounds.values()

        self._prepare_model()

        if (self._func is None): # Then Differential Evolution is used (default)
            result = differential_evolution(self._SSE, self._parameter_bounds, **kwargs)

        else:
            result = func(self._SSE, self._parameter_bounds,**kwargs)

        metrics = {
            "Parameters": self._parameter_names,
            "Average SSE": self._collected_values.mean(0),
            "Estimated Result": result.x
        }

        self._collected_values = np.array([])
        return (metrics)

    def setDataFromFile(self, FILENAME, delimiter=",", headers=True, time_column="time", usecols=None):
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

        data = np.genfromtxt(FILENAME, dtype=float, delimiter=delimiter, names=headers, usecols=usecols)
        self._data = pandas.DataFrame(data=data, index=data[time_column])
        self._data.drop(["time"], axis=1, inplace=True)




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

    def _prepare_model(self):
        random.seed()
        self._model_roadrunner = te.loada(self._model.model)
        self._model_roadrunner.integrator.variable_step_size = self._model.variable_step_size
        self._model_roadrunner.integrator = self._model.integrator




    def _SSE(self,parameters):
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
        random.seed()
        self._prepare_model()
        self._set_theta_values(theta)
        

        try: # The Simulation may fail. If so, throw a large penalty
            sim_data = None
            if self._stochastic:
                modified_model = self._model_roadrunner.getCurrentAntimony()
                stochastic_simulation_model = te.StochasticSimulationModel(model=modified_model,
                                                                   seed=1234,  # not used
                                                                   variable_step_size=self._model.variable_step_size,
                                                                   from_time=self._model.from_time,
                                                                   to_time=self._model.to_time,
                                                                   step_points=self.model._step_points)
                stochastic_simulation_model.integrator = self._model.integrator
                results = te.distributed_stochastic_simulation(self._sc, stochastic_simulation_model, 50)

                column_names = results[0][0]
                column_names = [item[1:-1] if (item != "time" and item[0] == '[') else item for item in column_names]

                mean_result = np.array([item[1] for item in results]).mean(0)

                sim_data = pandas.DataFrame(data=mean_result, columns=column_names)

            else:

                normal_sim = self._model_roadrunner.simulate(self._model.from_time, self._model.to_time,
                                                                           self._model.step_points)

                sim_data = pandas.DataFrame(data=normal_sim, index=normal_sim["time"], columns=normal_sim.colnames)

                column_names = {}
                for each_column in normal_sim.colnames:
                    if (each_column != "time" and each_column[0] == '['):
                        column_names[each_column] = each_column[1:-1]
                    else:
                        column_names[each_column] = each_column

                sim_data.rename(columns=column_names,inplace=True)



            if sim_data is None:
                raise ValueError("Something wrong in calculating Simulation Data")

            partial_result = 0.0
            total_observations = 0
            for _, row in sim_data.iterrows():

                row_timestamp = float(row["time"])

                comp_data = self._data[self._data.index <= row_timestamp].iloc[-1]

                star = 6
                for each_key in comp_data.keys():
                    partial_result += (comp_data[each_key] - row[each_key]) ** 2

                    total_observations += 1

            final_result = (partial_result / total_observations) ** 0.5

            self._collected_values = np.append(self._collected_values, final_result)

            print("SSE :"+str(final_result))
            return(final_result)

        except Exception as e:
            
            return 10000000.

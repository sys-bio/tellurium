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
    """Parameter Estimation"""
    def __init__(self, stochastic_simulation_model,bounds, data=None):
        if(data is not None):
            self.data = data

        self.model = stochastic_simulation_model
        self.bounds = bounds
        


    def setDataFromFile(self,FILENAME, delimiter=",", headers=True):
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
        with open(FILENAME,'r') as dest_f:
            data_iter = csv.reader(dest_f,
                                   delimiter = ",",
                                   quotechar = '"')
            self.data = [data for data in data_iter]
        if(headers):
            self.data = self.data[1:]

        self.data = np.asarray(self.data, dtype = float)
        

    def run(self,func=None):
        """Allows the user to set the data from a File
        This data is to be compared with the simulated data in the process of parameter estimation
        
        Args:
            func: An Optional Variable with default value (None) which by default run differential evolution
                which is from scipy function. Users can provide reference to their defined function as argument.
            

        Returns:
            The Value of the parameter(s) which are estimated by the function provided.
        
        .. sectionauthor:: Shaik Asifullah <s.asifullah7@gmail.com>
        
        
        """
        
        self._parameter_names = self.bounds.keys()
        self._parameter_bounds = self.bounds.values()
        self._model_roadrunner = te.loada(self.model.model)
        x_data = self.data[:,0]
        y_data = self.data[:,1:]
        arguments = (x_data,y_data)

        if(func is not None):
            result = differential_evolution(self._SSE, self._parameter_bounds, args=arguments)
            return(result.x)
        else:
            result = func(self._SSE,self._parameter_bounds,args=arguments)
            return(result.x)

    def _set_theta_values(self, theta):
        """ Sets the Theta Value in the range of bounds provided to the Function.
            Not intended to be called by user.
            
        Args:
            theta: The Theta Value that is set for the function defined/provided
            

        Returns:
            None but it sets the parameter(s) to the stochastic model provided
        
        .. sectionauthor:: Shaik Asifullah <s.asifullah7@gmail.com>
        
        
        """
        for theta_i,each_theta in enumerate(self._parameter_names):
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


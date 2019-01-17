"""
Created on Fri Oct 12 09:42:34 2018

@author: YeonMi
"""

import tellurium as te
te.setDefaultPlottingEngine("matplotlib")
import numpy as np 
import random
import roadrunner
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs 
import pandas as pd 


def UncertaintySingleP(model, variables, runType = None, parameters = None, simulation = None, degreeofVariability = None,
                      excludedParameters = None, sizeofEnsemble = None, ConfidenceInterval = None,  
                      limitc = None, midc = None, fillc = None, barc = None, 
                      limitw = None, midw = None,
                      fontsize = None,  
                      callback = None, datasave = None, imagesave = None):
    
    """ Measures the contribution of a singple parameter uncertainty to the model output. 
    The row of the grid indicates individual parameter, the independent variable of the simulation.
    The column of the grid is the varaiable of interest. 
    The x-axis of the subplot is time. 
    The y-axis of the subplot is the value of the species variable. 
    For each subplot, the model is simulated multiple time (default : 10000 times) 
    while varying the value of one parameter and keeping other parameters constant. 
    
   
    :param model: roadrunner variable. model to be simulated.
    :param variables: variables of interest (list).
    :param runType: mode of simulation (str). Two options, "TimeCourse" and "SteadyState", available.
    :param parameters: parameters to use for the uncertainty quantification (list). If not designated, all parameters will be run.  
    :param simulation: simulation time range (tuple, (start time, end time, number of points)).
	:param degreeofVariability: degree of variability (float) 
    :param excludedParameters: parameters to be excluded from the uncertainty quantification (list) .
    :param sizeofEnsemble: number of simulations (integer).
    :param ConfidenceInterval: 95 (default) level of confidence interval. (int, 0-100).
    :param limitc: linecolor of confidence interval limit (str).
    :param midc: linecolor of median (str).
    :param fillc: fill color of confidence interval (str). 
    :param barc: color of the bar (str)
    :param limitw: linewidth of the confidence interval limit (int).
    :param midw: linewidth of the median (int). 
    :param fontsize: font size (int).
    :param callback: callback (bool) If `True`, shows the progress of the task by returning the coordinate of subplot
    :param datasave: name of the directory (str). creates a new directory in current working directory and save raw data in CSV format.
    :param imagesave: name of the image file (str, "filename.format"). saves the image file of the grid output. 
    """
    
    #default settings for function arguments 
    if parameters is None: 
        parameters = model.getGlobalParameterIds()
    for v in variables:
        if v in parameters:
            parameters.remove(v)    
        
    if simulation is None: 
        simulation = (0,60,241)
    
    if degreeofVariability is None: 
        degreeofVariability = 0.1

    if excludedParameters is None: 
        excludedParameters = []
    else:
        for e in excludedParameters:
            if e in parameters:
                parameters.remove(e)
                
    if sizeofEnsemble is None: 
        sizeofEnsemble = 10000

    if ConfidenceInterval is None: 
        ConfidenceInterval = 95 
    
    if limitc is None: 
        limitc = "cadetblue"
        
    if midc is None: 
        midc = "cornflowerblue"        
    
    if fillc is None: 
        fillc = "lavender" 
    
    if barc is None:
        barc = "cornflowerblue"
          
    if limitw is None:
        limitw = 0
        
    if midw is None: 
        midw = 1   
        
    if fontsize is None:
        matplotlib.rcParams.update({'font.size': 12})
    else: 
        matplotlib.rcParams.update({'font.size' : fontsize })
        
    if callback is None:
        callback = False 
        
    if runType is None:
        runType = "TimeCourse"  
    
    #create a new directory to save raw data
    if datasave is not None:
        import os
        cwd = os.getcwd()
        os.makedirs(datasave)
        newdir = os.path.join(cwd, datasave)    
    
    # set lower and upper limit of the confidence interval 
    cilimit = [(100-ConfidenceInterval)/2, 100/2, (100-ConfidenceInterval)/2 + ConfidenceInterval]  
           
    
    
    # Timecourse simulation
    
    if runType == "TimeCourse":
        if imagesave is not None: 
            #adjust pdf image size 
            if imagesave.split(".")[1] == "pdf":
                if len(parameters) > 50 and len(parameters) <= 100 :
                    matplotlib.rcParams.update({'font.size':9})
                    figuresize = (len(variables)*3,len(parameters)*2)
                elif len(parameters) > 100:
                    matplotlib.rcParams.update({'font.size':7})
                    figuresize = (len(variables)*1.5,len(parameters)*1) 
                else:
                    figuresize = (len(variables)*5,len(parameters)*4)
            else:
               figuresize = (len(variables)*5,len(parameters)*4) 
        else:
            figuresize = (len(variables)*5,len(parameters)*4)
        
        fig = plt.figure(figsize = figuresize)
        grids = gs.GridSpec(nrows = len(parameters), ncols = len(variables), figure = fig)
        
        for v in variables:
            for p in parameters: 
                results = []
                lowers = []
                mids = []
                uppers = []
            
        # run simulations and collect all the results
                for i in range(0, sizeofEnsemble+1):
                    model.resetAll()
                    model[p] = random.normalvariate(model[p], degreeofVariability * model[p])
                    result = model.simulate(simulation[0], simulation[1], simulation[2], ['time'] + [v]) 
                    results.append(result)
                
                for j in range(0, len(results[0]['time'])):
                    timepoint=[]
                    for k in range(0,len(results)):
                        timepoint.append(results[k][v][j])
                    lowers.append(np.percentile(timepoint,cilimit[0]))
                    mids.append(np.percentile(timepoint,cilimit[1]))
                    uppers.append(np.percentile(timepoint,cilimit[2]))
            


                x = results[0]["time"]
                y1 = lowers
                y2 = mids
                y3 = uppers
            
            #save the data file(csv form) in a new directory 
                
                if datasave is not None:        
                    import pandas as pd 
                    filename =  "%s_%s.csv" % (p,v)
                    pathtofile = os.path.join(newdir,filename)
                    d = {'time':x, 'lower limit' : y1, 'mean' : y2, 'upper limit': y3}
                    df = pd.DataFrame(data = d)
                    df.to_csv(pathtofile)
                    
                
                nwsub=fig.add_subplot(grids[parameters.index(p),variables.index(v)])
                if variables.index(v) == 0:
                    nwsub.set_ylabel(p)
                if parameters.index(p) == 0:
                    nwsub.set_title(v)
                nwsub.plot(x,y1,color = limitc, linewidth=limitw)
                nwsub.plot(x,y2,color = midc, linewidth=midw, label=v)
                nwsub.plot(x,y3,color = limitc, linewidth=limitw)
                nwsub.fill_between(x,y1,y3, facecolor = fillc)
                nwsub.legend()
                
                if callback is True: 
                    print ((parameters.index(p),variables.index(v)),"complete")
    

        fig.tight_layout(pad=0.5,h_pad=0.5,w_pad=0.5)
        fig.align_ylabels()
        if imagesave is not None:
            fig.savefig(imagesave)
        else:
            fig.savefig("SingleP_UQ.png")
            
    #Steady State simulation

    elif runType == "SteadyState": 

        
        figuresize = (len(parameters),len(variables)*4)
        fig = plt.figure(figsize = figuresize)
        grids = gs.GridSpec(nrows = len(variables), ncols = 1, figure = fig)
        newvars = []
        for v in variables:
            if v in model.getFloatingSpeciesIds():
                newvars.append("["+v+"]")
            else:
                newvars.append(v)
        model.steadyStateSelections = newvars
        for nv in newvars:
            midpoints = []
            lowlimits = []
            upplimits = []
            for p in parameters:
                ssresults=[]
                for i in range(0,sizeofEnsemble+1):
                    model.resetAll()
                    model[p]=random.normalvariate(model[p], degreeofVariability * model[p]) 
                    ssresult = model.getSteadyStateValuesNamedArray()[nv][0]
                    ssresults.append(ssresult)
                lowlimits.append(np.percentile(ssresults,cilimit[0]))
                midpoints.append(np.percentile(ssresults,cilimit[1]))
                upplimits.append(np.percentile(ssresults,cilimit[2]))        
                if callback is True: 
                    print ("ss:",(nv,parameters.index(p)),"complete")     
            barheights = list(np.asarray(upplimits)-np.asarray(lowlimits))
            nwsub = fig.add_subplot(grids[newvars.index(nv),0])           
            nwsub.bar(x = parameters, height = barheights, color = barc)
            nwsub.set_ylabel(nv)
            nwsub.set_title("UQ at steadystate : %s" %(nv))
            
        
            if datasave is not None :
                import pandas as pd 
                filename =  "SS_%s.csv" % (nv)
                pathtofile = os.path.join(newdir,filename)
                d = {'parameters': parameters, 'lower limit' : lowlimits, 'midpoint' : midpoints, 'upper limit': upplimits}
                df = pd.DataFrame(data = d)
                df.to_csv(pathtofile)    
        
        
        if imagesave is not None:
            fig.savefig(imagesave)
        else:
            fig.savefig("SingleP_UQ.png")
            
            
def UncertaintyAllP(model, variables, runType = None, parameters = None, simulation = None, degreeofVariability = None, 
					excludedParameters = None, sizeofEnsemble = None, ConfidenceInterval = None,  
                    limitc = None, midc = None, fillc = None, barc = None, errorc = None, 
                    limitw = None, midw = None,
                    figtitle = None, xlabel = None, ylabel = None,
                    fontsize = None, 
                    callback = None, datasave = None, imagesave = None):
    
    """ Plots the confidence interval to visualize and quantify the uncertainty of the model. 
    The model is simulated multiple time (default : 10000 times) with changes in the value of entire set of parameters  
    following the probability of normal distribution. 
    
   
    :param model: roadrunner variable. model to be simulated.
    :param variables: variables of interest (list).
    :param runType: mode of simulation (str). Two options, "TimeCourse" and "SteadyState", available.
    :param parameters: parameters to use for the uncertainty quantification (list). If not designated, all parameters will be run.  
    :param simulation: simulation time range (tuple, (start time, end time, number of points)).
    :param excludedParameters: parameters to be excluded from the uncertainty quantification (list) .
    :param sizeofEnsemble: number of simulations (integer).
    :param ConfidenceInterval: 95 (default) level of confidence interval. (int, 0-100).
    :param limitc: linecolor of confidence interval limit (str).
    :param midc: linecolor of median (str).
    :param fillc: fill color of confidence interval (str). 
    :param barc: color of the bar (str)
    :param limitw: linewidth of the confidence interval limit (int).
    :param midw: linewidth of the median (int). 
    :param figtitle: title of the figure (str).
    :param xlabel: label of the x-axis (str).
    :param ylabel: label of the y-axis (str).
    :param fontsize: font size (int).
    :param callback: callback (bool) If `True`, shows the progress of the task by returning the coordinate of subplot.
    :param datasave: name of the directory (str). creates a new directory in current working directory and save raw data in CSV format.
    :param imagesave: name of the image file (str, "filename.format"). saves the image file of the grid output. 
    """
    
    if parameters is None: 
        parameters = model.getGlobalParameterIds()
        
    for v in variables:
        if v in parameters:
            parameters.remove(v)
    if simulation is None: 
        simulation = (0,60,241)
    
    if degreeofVariability is None:
        degreeofVariability = 0.1

	
    if excludedParameters is None: 
        excludedParameters = []
    else:
        for e in excludedParameters:
            if e in parameters:
                parameters.remove(e)
    
    if sizeofEnsemble is None: 
        sizeofEnsemble = 10000

    if ConfidenceInterval is None: 
        ConfidenceInterval = 95 
    
    if limitc is None: 
        limitc = "cadetblue"
        
    if midc is None: 
        midc = "cornflowerblue" 
    
    if fillc is None: 
        fillc = "lavender" 
    
    if barc is None:
        barc = "cornflowerblue"
        
    if errorc is None: 
        errorc = "midnightblue"
        
    if limitw is None: 
        limitw = 0
    
    if midw is None: 
        midw = 1.5
    
    if fontsize is None:
        matplotlib.rcParams.update({'font.size': 12})
    else: 
        matplotlib.rcParams.update({'font.size' : fontsize })
        
        
    if callback is None:
        callback = False 
    
    if runType is None:
        runType = "TimeCourse"
    if datasave is not None:
        import os
        cwd = os.getcwd()
        os.makedirs(datasave)
        newdir = os.path.join(cwd, datasave)
    
    
    # set lower and upper limit of the confidence interval 
    cilimit = [(100-ConfidenceInterval)/2, 100/2, (100-ConfidenceInterval)/2 + ConfidenceInterval]  
    

    
    #figure size 
    if runType == "TimeCourse":
        figuresize = (6*len(variables),4)
        fig = plt.figure(figsize = figuresize)
        grids = gs.GridSpec(nrows = 1, ncols= len(variables), figure = fig)
    elif runType == "SteadyState":
        figuresize = (2*len(variables), 4)
        fig = plt.figure(figsize = figuresize)
        grids = gs.GridSpec(nrows = 1, ncols = 1, figure = fig)
    #time course simulation 
    if runType == "TimeCourse":
        for v in variables:
            results = []
            lowers = []
            mids = []
            uppers = []
        #for each row
            for i in range(0, sizeofEnsemble+1):
                model.resetAll()
                for p in parameters: 
                    model[p] = random.normalvariate(model[p], degreeofVariability * model[p])
                result = model.simulate(simulation[0], simulation[1], simulation[2], ['time'] + [v]) 
                results.append(result)
            
                if callback is True: 
                    if i%(sizeofEnsemble/2)==0:
                        print (v, "simulation:", i/(sizeofEnsemble)*100, "% complete") 
        
            for j in range(0, len(results[0]['time'])):
                timepoint=[]
                for k in range(0,len(results)):
                    timepoint.append(results[k][v][j])
                lowers.append(np.percentile(timepoint,cilimit[0]))
                mids.append(np.percentile(timepoint,cilimit[1]))
                uppers.append(np.percentile(timepoint,cilimit[2]))
            

        #create a plot for confidence interval 
            x = results[0]["time"]
            y1 = lowers
            y2 = mids
            y3 = uppers
            
            #save the data file(csv form) in new directory 
            if datasave is not None:
                filename =  "%s.csv" % (v)
                pathtofile = os.path.join(newdir,filename)
                d = {'time':x, 'lower limit' : y1, 'median' : y2, 'upper limit': y3}
                df = pd.DataFrame(data = d)
                df.to_csv(pathtofile)
            
            nwsub=fig.add_subplot(grids[0,variables.index(v)])
            if xlabel is None:
                nwsub.set_xlabel("time")
            else:
                nwsub.set_xlabel(xlabel)
            if ylabel is None:
                nwsub.set_ylabel(v)
            else:
                nwsub.set_ylabel(ylabel)
        
            if figtitle is None : 
                nwsub.set_title("UQ : %s" %(v))
            else:
                nwsub.set_title(figtitle)
        
            nwsub.plot(x,y1,color = limitc, linewidth=limitw)
            nwsub.plot(x,y2,color = midc, linewidth=midw, label=v)
            nwsub.plot(x,y3,color = limitc, linewidth=limitw)
            nwsub.fill_between(x,y1,y3, facecolor = fillc)
        fig.tight_layout(pad=0.5,h_pad=0.5,w_pad=0.5)
        fig.align_xlabels()

    elif runType == "SteadyState":
        newvars = []
        mids_df = []
        lows_df = []
        upps_df = []
        for v in variables:
            if v in model.getFloatingSpeciesIds():
                newvars.append("["+v+"]")
            else:
                newvars.append(v)
        model.steadyStateSelections = newvars    
        for nv in newvars:
            ssresults = []
            for i in range(0,sizeofEnsemble+1):
                model.resetAll()
                for p in parameters:
                    model[p]=random.normalvariate(model[p], degreeofVariability *model[p])
                
                ssresults.append(model.getSteadyStateValuesNamedArray()[nv][0])
            midpoint = np.percentile(ssresults,cilimit[1])
            lowerlimit = np.percentile(ssresults,cilimit[0])
            upperlimit = np.percentile(ssresults,cilimit[2])
            mids_df.append(midpoint)
            lows_df.append(lowerlimit)
            upps_df.append(upperlimit)
            if callback == True: 
                print ("UQ_SS_AllP:",nv)
#        UQ = list(np.asarray(upps_df)-np.asarray(lows_df))
        lowerror = list(np.asarray(mids_df) - np.asarray(lows_df))
        upperror = list(np.asarray(upps_df) - np.asarray(mids_df))
        errorbar = [lowerror,upperror]
        nwsub = fig.add_subplot(grids[0,0])  
#        nwsub.bar(x=variables, height = UQ, color = barc)
        nwsub.axis([0,len(variables)+1,0,max(upps_df)*1.1])
        vartonum=[variables.index(v)+1 for v in variables]
        nwsub.errorbar(x=vartonum, y=mids_df, yerr=errorbar, ecolor="cornflowerblue", fmt = 'o', capsize = 10)
        nwsub.set_xticks(vartonum)
        nwsub.set_xticklabels(labels = variables)
        fig.tight_layout(pad=0.5,h_pad=0.5,w_pad=0.5)
        plt.subplots_adjust(top=0.88)
        if ylabel is None:
            nwsub.set_ylabel("")
        else:
            nwsub.set_ylabel(ylabel)
            
        if figtitle is None:
            nwsub.set_title("UQ at steady state")
        else:
            nwsub.set_title(figtitle)
        if datasave is not None: 
            filename =  "AllP_UQSS.csv" 
            pathtofile = os.path.join(newdir,filename)
            d = {'variable':newvars, 'lower limit':lows_df, 'median':mids_df, 'upper limit': upps_df}
            df = pd.DataFrame(data = d)
            df.to_csv(pathtofile)
            
    if imagesave is None:
        fig.savefig("AllP_UQ.png")
    else:
        fig.savefig(imagesave)
        








"""
Tellurium SED-ML support.
"""

from __future__ import print_function, division

import sys
import os.path
import re
import zipfile
import libsedml
import StringIO
import httplib
import xml.etree.ElementTree as et
from collections import namedtuple

raise ImportError("This should never be imported, use the new implementation")

MatchingSetsOfVariableIDs = namedtuple("MatchingSetsOfVariableIDs", "datagenID, taskReference, sedmlID, sbmlID")
MatchingSetsOfRepeatedTasksDataGenerators = namedtuple("MatchingSetsOfRepeatedTasksDataGenerators", "datagenID, rangeSize")

modelname = str()
outdir = str()

# Map of replaced words
mapping = [
    ('repeated', 'r'),
    ('Repeated', 'r'),
    ('task', 't'),
    ('Task', 't'),
    ('data', 'd'),
    ('Data', 'd'),
    ('generator', 'g'),
    ('Generator', 'g')
]


class SedmlException(Exception):
    pass


def sedml_to_python(inputstring):
    """ Convert sedml file to python code.
    Legacy support

    :param inputstring:
    :type inputstring:
    :return:
    :rtype:
    """
    import warnings
    warnings.warn('Use sedmlToPython instead, will be removed in v1.4',
                  DeprecationWarning, stacklevel=2)
    return sedmlToPython(inputstring)


def sedmlToPython(inputstring):
    """ Convert sedml file to python code.

    :param inputstring: full path name to SedML model or SED-ML string
    :type inputstring: path
    :return: contents
    :rtype:
    """

    class Tee(object):
        def __init__(self, *files):
            self.files = files
        def write(self, obj):
            for f in self.files:
                f.write(obj)

    if not isinstance(inputstring, basestring):
        raise TypeError("For SedmlToPy translation, input must be string")

    if inputstring.startswith(r"<?"):  # Check if string is a SED-ML string
        sedmlDoc = libsedml.readSedMLFromString(inputstring)
        path = os.getcwd() + "\\" # Temp. assumption

    else: # Else assume file path
        if not os.path.exists(inputstring):
            raise IOError("Cannot find SED-ML file")

        global modelname

        modelName = os.path.splitext(os.path.basename(inputstring))[0]
        extension = os.path.splitext(os.path.basename(inputstring))[1]
        path = inputstring.rsplit(os.path.basename(inputstring), 1)[0]

        if extension == ".sedx":
            zip = zipfile.ZipFile(inputstring, 'r')
            path = path + modelName
            if not os.path.isdir(path):
                os.makedirs(path)
            for each in zip.namelist():
            # check if the item includes a subdirectory
            # if it does, create the subdirectory in the output folder and write the file
            # otherwise, just write the file to the output folder
                if not each.endswith('/'):
                    root, name = os.path.split(each)
                    directory = os.path.normpath(os.path.join(path, root))
                    if not os.path.isdir(directory):
                        os.makedirs(directory)
                    file(os.path.join(directory, name), 'wb').write(zip.read(each))
            zip.close()

            tree = et.parse(path + "/manifest.xml")
            root = tree.getroot()
            print(root)
            for child in root:
                format = child.attrib['format']
                if(format.endswith("sed-ml")):
                    inputstring = child.attrib['location']

            k = inputstring.rfind("/")
            inputstring = inputstring[k+1:]
            inputstring = path + "/" + inputstring

        sedmlDoc = libsedml.readSedMLFromFile(inputstring)

    if sedmlDoc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_ERROR) > 0:
        raise SedmlException(sedmlDoc.getErrorLog().toString())

    f = StringIO.StringIO()
    original = sys.stdout
    #sys.stdout = Tee(sys.stdout, f)   # output to console and file
    sys.stdout = Tee(f)              # output to file only

    print("# Translated SED-ML")
    print("# Beginning of generated script")
    print("import roadrunner")
    print("import numpy as np")
    print("import matplotlib.pyplot as plt")
    print("")
    for i in range(0, sedmlDoc.getNumModels()):
        currentModel = sedmlDoc.getModel(i)
        print("# Execute the tasks of model: " + currentModel.getId())
        rrName = currentModel.getId()
        #rrName = "rr" + str(i)
        print(rrName + " = roadrunner.RoadRunner()")
        generateTasks(rrName, sedmlDoc, currentModel, path)
        print("")
    print("# List of Data Generators")
    dataGeneratorsList = []
    for i in range(0, sedmlDoc.getNumModels()):
        currentModel = sedmlDoc.getModel(i)
        generateData(sedmlDoc, currentModel, dataGeneratorsList)
    print("# List of Outputs")
    generateOutputs(sedmlDoc, dataGeneratorsList)
    print("# End of generated script")

    contents = f.getvalue()
    sys.stdout = original  # restore print to stdout only
    f.close()
    return contents


def generateTasks(rrName, sedmlDoc, currentModel, path):
    """ Generate the SED-ML Tasks.

    :param rrName:
    :type rrName:
    :param sedmlDoc:
    :type sedmlDoc:
    :param currentModel:
    :type currentModel:
    :param path:
    :type path:
    :return:
    :rtype:
    """
    listOfChanges = []
    loadModel(rrName, sedmlDoc, currentModel, path)
    #print(rrName + ".simulateOptions.structuredResult = False")
    bFoundAtLeastOneTask = False

    for i in range(0, currentModel.getNumChanges()):
        aChange = currentModel.getChange(i)
        if aChange.getElementName() == "changeAttribute":
            newValue = aChange.getNewValue()
            variableName = aChange.getTarget()
            if (("model" in variableName) and ("parameter" in variableName)):
                variableName = variableName.rsplit("id=\'",1)[1]
                variableName = variableName.rsplit("\'",1)[0]
                aStr = rrName + ".model[\"" + variableName + "\"] = " + newValue    # set amount
                listOfChanges.append(aStr)
                print(aStr)
            elif (("model" in variableName) and ("species" in variableName)):
                variableName = variableName.rsplit("id=\'",1)[1]
                variableName = variableName.rsplit("\'",1)[0]
                aStr = rrName + ".model[\"init([" + variableName + "])\"] = " + newValue    # set amount
                #aStr = rrName + ".model[\"[" + variableName + "]\"] = " + newValue    # set amount
                listOfChanges.append(aStr)
                print(aStr)
            else:
                print("# Unsupported changeAttribute target " + variableName)
                return          # nothing to do repeatedly since our change is bad
        else:
            aStr = "# Unsupported change " + aChange.getElementName() + " for model " + currentModel.getId()
            print(aStr)
            return

    # The 'selections' are a list of all the 'variable' elements from the dataGenerators
    # we first deal with normal tasks, if any
    for e in range(0, sedmlDoc.getNumTasks()):
        task1 = sedmlDoc.getTask(e)
        if task1.getElementName() == "repeatedTask":
            pass
        else:
            if task1.getModelReference() != currentModel.getId():
                continue
            variablesDictionary = []
            variablesList = []
            populateVariableLists(sedmlDoc, task1, variablesList, variablesDictionary)
            if len(variablesList) == 0:  # nothing to do if no data generators refer to this task
                continue
            generateSimulation(rrName, sedmlDoc, currentModel, task1, variablesList, variablesDictionary, -1)
            bFoundAtLeastOneTask = True

    # now deal with repeated tasks, if any
    for e in range(0, sedmlDoc.getNumTasks()):
        task1 = sedmlDoc.getTask(e)
        if task1.getElementName() == "repeatedTask":
            for i in range(0, task1.getNumSubTasks()):
                task2 = task1.getSubTask(i)     # the subtask which points to the real task we need to call repeatedly for each value in range
                task2 = task2.getTask()         # the Id of the real task
                task2 = sedmlDoc.getTask(task2) # get real task by Id
                if task2.getModelReference() != currentModel.getId():
                    continue
                aRange = task1.getRange(0)       # we assume one single master range - we don't know how to deel flatten
                if aRange.getElementName() != "uniformRange":
                    print("# Only uniformRange ranges are supported at this time")
                    continue

                # if resetModel is true we need to reapply all the changes from above
                print("")
                bResetModel = task1.getResetModel()
                # FIXME: no code generation with simulateOptions
                if bResetModel:
                    print(rrName + ".simulateOptions.resetModel = True")
                else:
                    print(rrName + ".simulateOptions.resetModel = False")

                # need to use the RepeatedTask because the data generators refer to it
                variablesDictionary = []      # matching pairs of sedml variable ID and sbml variable ID
                variablesList = []            # the IDs of the sbml variables, non duplicate entries
                populateVariableLists(sedmlDoc, task1, variablesList, variablesDictionary)
                # iterate over all changes
                aChange = task1.getTaskChange(0)
                if aChange.getElementName() != "setValue":
                    print("# Only setValue changes are supported at this time")
                    continue
                variableName = aChange.getTarget()
                vn = variableName
                vn = vn.rsplit("id=\'",1)[1]
                vn = vn.rsplit("\'",1)[0]
                # for each point in the range we compute the new values of the variables affected
                # and generate a task
                for j in range(0, aRange.getNumberOfPoints()):
                    print("")
                    if bResetModel == True: # if we reset the model we need to repeat again all the Changes from above
                        for aStr in listOfChanges:
                            print(aStr)
                    start = aRange.getStart()
                    end = aRange.getEnd()
                    newValue = start + j * (end - start) / (aRange.getNumberOfPoints()-1)
                    if (("model" in variableName) and ("parameter" in variableName)):
                        print(rrName + ".model[\"" + vn + "\"] = " + str(newValue))                   # set amount
                    elif (("model" in variableName) and ("species" in variableName)):
                        print(rrName + ".model[\"init([" + vn + "])\"] = " + str(newValue))                   # set amount
                    else:
                        print("# Unsupported setValue target " + variableName)
                        return          # nothing to do repeatedly since our change is bad
                    # need to use both the real Task (task2) because it has the reference to model and simulation
                    # and the repeated task (task1) because its Id is used for generating the flattened Id's
                    generateSimulation(rrName, sedmlDoc, currentModel, task2, variablesList, variablesDictionary, j, task1)
                    bFoundAtLeastOneTask = True

    if bFoundAtLeastOneTask == False:
        print("# There are no simulations to run for this model: " + currentModel.getId())


def loadModel(rrName, sedmlDoc, currentModel, path):
    """ Load model.

    :param rrName:
    :type rrName:
    :param sedmlDoc:
    :type sedmlDoc:
    :param currentModel:
    :type currentModel:
    :param path:
    :type path:
    :return:
    :rtype:
    """
    global modelname
    global outdir
    string = currentModel.getSource()
    string = string.replace("\\", "/")
    if isId(string):                             # it's the Id of a model
        originalModel = sedmlDoc.getModel(string)
        if originalModel is not None:
            string = originalModel.getSource()          #  !!! for now, we reuse the original model to which the current model is referring to
        else:
            pass
    if string.startswith("."):                  # relative location, we trust it but need it trimmed
        if string.startswith("../"):
            string = string[3:]
        elif string.startswith("./"):
            string = string[2:]
        print(rrName + ".load('" + path.replace("\\","/") + string + "')")    # SBML model name recovered from "source" attr
        #from os.path import expanduser
        #path = expanduser("~")
        #print(rrName + ".load('" + path + "\\" + string + "')")    # SBML model name recovered from "source" attr
    elif "\\" or "/" or "urn:miriam" not in string:
        print(rrName + ".load('" + path.replace("\\","/") + string + "')")
    elif string.startswith("urn:miriam"):
        print("Downloading model from BioModels Database...")
        astr = string.rsplit(':', 1)
        astr = astr[1]
        string = path + astr + ".xml"
        if not os.path.exists(string):
            conn = httplib.HTTPConnection("www.ebi.ac.uk")
            conn.request("GET", "/biomodels-main/download?mid=" + astr)
            r1 = conn.getresponse()
            #print(r1.status, r1.reason)
            data1 = r1.read()
            conn.close()
            f1 = open(string, 'w')
            f1.write(data1)
            f1.close()
        else:
            pass
        print(rrName + ".load('" + string +"'))")
    else:         # assume absolute path pointing to hard disk location
        string = string.replace("\\", "/")
        print(rrName + ".load('" + string + "')")


def populateVariableLists(sedmlDoc, task1, variablesList, variablesDictionary):
    """ Populate variable lists.

    :param sedmlDoc:
    :type sedmlDoc:
    :param task1:
    :type task1:
    :param variablesList:
    :type variablesList:
    :param variablesDictionary:
    :type variablesDictionary:
    :return:
    :rtype:
    """
    for i in range(0,  sedmlDoc.getNumDataGenerators()):
        current = sedmlDoc.getDataGenerator(i)
        vl = current.getListOfVariables()
        for j in range(0, vl.size()):
            currentVar = vl[j]
            if currentVar.getTaskReference() != task1.getId():
                continue
            if currentVar.isSetSymbol():    # symbol field of variable is set
                cvs = currentVar.getSymbol()
                astr = cvs.rsplit("symbol:")
                astr = astr[1]
                if variablesList.count(astr) < 1:
                    variablesList.append(astr)
                m = MatchingSetsOfVariableIDs(current.getId(), currentVar.getTaskReference(), currentVar.getId(), astr)
                variablesDictionary.append(m)
            elif currentVar.isSetTarget():
                cvt = currentVar.getTarget()    # target field of variable is set
                astr = cvt.rsplit("@id='")
                astr = astr[1]
                astr = astr[:-2]
                if variablesList.count(astr) < 1:
                    variablesList.append(astr)
                m = MatchingSetsOfVariableIDs(current.getId(), currentVar.getTaskReference(), currentVar.getId(), astr)
                variablesDictionary.append(m)
            else:
                print("# Unrecognized data generator variable")
                sys.exit(5)
    return


def generateSimulation(rrName, sedmlDoc, currentModel, task1, variablesList, variablesDictionary, repeatedTaskIndex, repeatedTask = None):
    """ Generate simulation. """
    __uniform = False
    __steady = False

    for j  in range(0, sedmlDoc.getNumSimulations()):
        currentSimulation = sedmlDoc.getSimulation(j)
        if task1.getSimulationReference() != currentSimulation.getId():
            continue
        if currentSimulation.getTypeCode() == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
            if __steady:
                print(rrName + ".conservedMoietyAnalysis = False")
            else:
                pass
            if not __uniform:
                string = rrName + ".timeCourseSelections = ["
                for i in range(0, len(variablesList)):
                    if i > 0:
                        string += ","
                    string += "\"" + variablesList[i] + "\""
                string += "]"
                print(string)
            __uniform = True
            algorithm = currentSimulation.getAlgorithm()
            if currentSimulation.isSetAlgorithm() == False:
                print("# Algorithm not set for simulation " + currentSimulation.getName())
                continue
            if algorithm.getKisaoID() != "KISAO:0000019":
                print("# Unsupported KisaoID " + algorithm.getKisaoID() + " for simulation " + currentSimulation.getName())
                continue
            if repeatedTaskIndex == -1:    # we expand the repeatedTask id because they need to be flattened for each element in ranges
                taskId = task1.getId()
            else:
                taskId = repeatedTask.getId() + "_" + str(repeatedTaskIndex)
            for k, v in mapping:
                taskId = taskId.replace(k, v)
            string = taskId + " = " + rrName + ".simulate("
            tc = currentSimulation
            totNumPoints = tc.getOutputEndTime() * tc.getNumberOfPoints() / (tc.getOutputEndTime() - tc.getOutputStartTime())
            string += str(int(0)) + ", " + str(int(tc.getOutputEndTime())) + ", " + str(int(totNumPoints))
            string += ")"
            print(string)
        elif currentSimulation.getTypeCode() == libsedml.SEDML_SIMULATION_STEADYSTATE:
            if not __steady:
                print(rrName + ".conservedMoietyAnalysis = True")
                string = rrName + ".steadyStateSelections = ["
                for i in range(0, len(variablesList)):
                    if i > 0:
                        string += ","
                    string += "\"" + variablesList[i] + "\""
                string += "]"
                print(string)
            else:
                pass
            __steady = True
            algorithm = currentSimulation.getAlgorithm()
            if algorithm.getKisaoID() != "KISAO:0000099":
                print("# Unsupported KisaoID " + algorithm.getKisaoID() + " for simulation " + currentSimulation.getName())
                continue
            if repeatedTaskIndex == -1:
                taskId = task1.getId()
            else:
                taskId = repeatedTask.getId() + "_" + str(repeatedTaskIndex)
            for k, v in mapping:
                taskId = taskId.replace(k, v)
            string = taskId + " = np.tile(" + rrName + ".getSteadyStateValues(), (2,1))"
            print(string)
            print(taskId + "[1][0] = 10")
        elif currentSimulation.getTypeCode() == libsedml.SEDML_SIMULATION_ONESTEP:
            if __steady:
                print(rrName + ".conservedMoietyAnalysis = False")
            else:
                pass
            string = rrName + ".timeCourseSelections = ["
            for i in range(0, len(variablesList)):
                if i > 0:
                    string += ","
                string += "\"" + variablesList[i] + "\""
            string += "]"
            print(string)
            algorithm = currentSimulation.getAlgorithm()
            if not currentSimulation.isSetAlgorithm():
                print("# Algorithm not set for simulation " + currentSimulation.getName())
                continue
            if algorithm.getKisaoID() != "KISAO:0000019":
                print("# Unsupported KisaoID " + algorithm.getKisaoID() + " for simulation " + currentSimulation.getName())
                continue
            if repeatedTaskIndex == -1:    # we expand the repeatedTask id because they need to be flattened for each element in ranges
                taskId = task1.getId()
            else:
                taskId = repeatedTask.getId() + "_" + str(repeatedTaskIndex)
            for k, v in mapping:
                taskId = taskId.replace(k, v)
            stepsize = currentSimulation.getStep()
            if __uniform:
                string = taskId + " = " + rrName + ".simulate(" + str(variablesList[-2]) + ", " + str(variablesList[-2] + stepsize) + ", 1)"
            else:
                string = taskId + " = " + rrName + ".simulate(0, " + str(stepsize) + ", 1)"
            print(string)
        else:
            print("# Unsupported type " + str(currentSimulation.getTypeCode()) + " for simulation " + currentSimulation.getName())


def generateData(sedmlDoc, currentModel, dataGeneratorsList):
    """ Handle the data generators.

    :return:
    :rtype:
    """
    variablesDictionary = []      # matching pairs of sedml variable ID and sbml variable ID
    variablesList = []            # the IDs of the sbml variables, non duplicate entries
    bFoundAtLeastOneTask = False

    for e in range(0,sedmlDoc.getNumTasks()):
        task1 = sedmlDoc.getTask(e)

        # repeated task
        if task1.getElementName() == "repeatedTask":
            for i in range(0, task1.getNumSubTasks()):
                task2 = task1.getSubTask(i)     # the subtask which points to the real task we need to call repeatedly for each value in range
                task2 = task2.getTask()         # the Id of the real task
                task2 = sedmlDoc.getTask(task2) # get real task by Id
                if task2.getModelReference() != currentModel.getId():
                    continue
                aRange = task1.getRange(0)       # we assume one single master range - we don't know how to deel flatten
                if aRange.getElementName() != "uniformRange":
                    print("# Only uniformRange ranges are supported at this time")
                    continue
                variablesDictionary = []
                variablesList = []
                # need to use the RepeatedTask because the data generators refer to it
                populateVariableLists(sedmlDoc, task1, variablesList, variablesDictionary)
                # for each point in the range we compute the new values of the variables affected
                # and generate a task
                for j in range(0, aRange.getNumberOfPoints()):
                    # need to use both the real Task (task2) because it has the reference to model and simulation
                    # and the repeated task (task1) because its Id is used for generating the flattened Id's
                    generateDataLoop(sedmlDoc, currentModel, task2, variablesList, variablesDictionary, j, task1, dataGeneratorsList)
                    bFoundAtLeastOneTask = True
                    print("")

        # not a repeated task
        else:
            if task1.getModelReference() != currentModel.getId():
                continue
            variablesDictionary = []
            variablesList = []
            populateVariableLists(sedmlDoc, task1, variablesList, variablesDictionary)
            if len(variablesList) == 0:
                continue
            generateDataLoop(sedmlDoc, currentModel, task1, variablesList, variablesDictionary, -1)
            bFoundAtLeastOneTask = True

    if bFoundAtLeastOneTask == False:
        pass
        #print("# No dataGenerator for this model: " + currentModel.getId());
    elif task1.getElementName() == "repeatedTask":
        pass
    else:
        print("")


def generateDataLoop(sedmlDoc, currentModel, task1, variablesList, variablesDictionary, repeatedTaskIndex, repeatedTask = None, dataGeneratorsList = None):
    """ Generate data loops. """
    # Each dataGenerator is calculated from the resulting output
    for s in range(0, sedmlDoc.getNumSimulations()):
        currentSimulation = sedmlDoc.getSimulation(s)
        if task1.getSimulationReference() == currentSimulation.getId():
            break           # we found the simulation referred to by this task (can't be more than one)

    dataGeneratorOutputList = []
    dataGeneratorTemp = str()

    for j in range(0, len(variablesDictionary)):
        m = variablesDictionary[j]
        current = sedmlDoc.getDataGenerator(m.datagenID)
        dataGeneratorResult = libsedml.formulaToString(current.getMath())

        if current.getId() == m.datagenID:
            stringToReplace = m.sedmlID
            position = m.sbmlID
            for k in range(0, len(variablesList)):
                if position == variablesList[k]:
                    position = k
                    break
            if repeatedTaskIndex == -1:
                taskId = task1.getId()
            else:
                taskId = repeatedTask.getId() + "_" + str(repeatedTaskIndex)
            if currentSimulation.getTypeCode() == libsedml.SEDML_SIMULATION_UNIFORMTIMECOURSE:
                tc = currentSimulation
                totNumPoints = tc.getOutputEndTime() * tc.getNumberOfPoints() / (tc.getOutputEndTime() - tc.getOutputStartTime())
                replacementString = taskId + "[" + '{0:g}'.format(totNumPoints - currentSimulation.getNumberOfPoints()) + ":," + str(position) + "]"
            elif currentSimulation.getTypeCode() == libsedml.SEDML_SIMULATION_STEADYSTATE:
                replacementString = taskId + "[0:," + str(position) + "]"
            elif currentSimulation.getTypeCode() == libsedml.SEDML_SIMULATION_ONESTEP:
                replacementString = taskId + "[0:," + str(position) + "]"
            else:
                print("# Unsupported type " + str(currentSimulation.getTypeCode()) + " for simulation " + currentSimulation.getName())

            if dataGeneratorResult != dataGeneratorTemp:
                if stringToReplace in dataGeneratorResult:
                    dataGeneratorReplaced = dataGeneratorResult.replace(stringToReplace, replacementString)
                else:
                    dataGeneratorReplaced = stringToReplace.replace(stringToReplace, replacementString)
                dataGeneratorId = current.getId()       # we expand the datagen id because they need to be flattened for repeated tasks
                if repeatedTaskIndex != -1:
                    dataGeneratorId += "_" + str(repeatedTaskIndex)
                dataGeneratorElement = dataGeneratorId + " = " + dataGeneratorReplaced
                dataGeneratorOutputList.append(dataGeneratorElement)
                dataGeneratorTemp = dataGeneratorResult

            else:
                dataGeneratorOutputList[-1] = dataGeneratorOutputList[-1].replace(stringToReplace, replacementString)

            if repeatedTaskIndex != -1:      # list of data generators flattening (when part of a range)
                position = -1
                for i in range(0, len(dataGeneratorsList)):
                    rtdg = dataGeneratorsList[i]
                    if rtdg.datagenID == current.getId():   # already present
                        position = i
                        break
                if position == -1:        # create it
                    rtdg = MatchingSetsOfRepeatedTasksDataGenerators(current.getId(), repeatedTaskIndex+1 )
                    dataGeneratorsList.append(rtdg)
                else:
                    rtdg = MatchingSetsOfRepeatedTasksDataGenerators(current.getId(), repeatedTaskIndex+1 )
                    dataGeneratorsList[position] = rtdg

    dataGeneratorOutput = '\n'.join(dataGeneratorOutputList)
    for k, v in mapping:
        dataGeneratorOutput = dataGeneratorOutput.replace(k, v)
    print(dataGeneratorOutput)


def generateOutputs(sedmlDoc, dataGeneratorsList):
    """ Generate the outputs.

    :param sedmlDoc:
    :type sedmlDoc:
    :param dataGeneratorsList:
    :type dataGeneratorsList:
    :return:
    :rtype:
    """
    #The 'plot' len(dataGeneratorsList)output, minus the legend
    taskList = []

    for i in range(0, sedmlDoc.getNumOutputs()):
        reportList = []
        output = sedmlDoc.getOutput(i)
        typeCode = output.getTypeCode()
        if typeCode == libsedml.SEDML_OUTPUT_REPORT:
            for x in range(0, output.getNumDataSets()):
                dataSet1 = output.getDataSet(x)
                if not dataSet1.getLabel():
                    reportList.append(dataSet1.getDataReference())
                else:
                    reportList.append(dataSet1.getLabel())
            print("print '--------------------" + output.getName().replace("'","") + "--------------------'")
            print("import pandas")
            print("df = pandas.DataFrame(np.array(" + str(reportList).replace("'","") + ").T, \ncolumns=" + str(reportList) + ")")
            print("print df.head(5)")
            print("print '--------------------Report End--------------------'\n")

        elif typeCode == libsedml.SEDML_OUTPUT_PLOT2D:
            for x in range(0, sedmlDoc.getNumTasks()):
                task1 = sedmlDoc.getTask(x)
                taskList.append(task1.getElementName())
            if "repeatedTask" in taskList:    #For repeated tasks
                for y in range(0, sedmlDoc.getNumTasks()):
                    task1 = sedmlDoc.getTask(y)
                    if task1.getElementName() == "repeatedTask":
                        for z in range(0, task1.getNumSubTasks()):
                            aRange = task1.getRange(0)
                            for l in range(0, aRange.getNumberOfPoints()):
                                if output.getNumCurves() > 1:
                                    allX = []
                                    allY = []
                                    for q in range(0, output.getNumCurves()):
                                        curve = output.getCurve(q)
                                        xDataReference = curve.getXDataReference()
                                        yDataReference = curve.getYDataReference()
                                        for k, v in mapping:
                                            xDataReference = xDataReference.replace(k, v)
                                            yDataReference = yDataReference.replace(k, v)
                                        if not len(dataGeneratorsList) == 0:
                                            allX.append(xDataReference + "_" + str(i))
                                            allY.append(yDataReference + "_" + str(i))
                                        else:
                                            allX.append(xDataReference)
                                            allY.append(yDataReference)
            elif "repeatedTask" not in taskList:    #There is no repeated tasks
                if output.getNumCurves() > 0:
                    allX = []
                    allY = []
                    for m in range(0, output.getNumCurves()):
                        curve = output.getCurve(m)
                        xDataReference = curve.getXDataReference()
                        yDataReference = curve.getYDataReference()
                        for k, v in mapping:
                            xDataReference = xDataReference.replace(k, v)
                            yDataReference = yDataReference.replace(k, v)
                        if not len(dataGeneratorsList) == 0:
                            allX.append(xDataReference + "_" + str(i))
                            allY.append(yDataReference + "_" + str(i))
                        else:
                            allX.append(xDataReference)
                            allY.append(yDataReference)
            if checkEqualIvo(allX) == True:
                pass
            else:
                print("X_" + str(i) + " = np.array(" + str(allX).replace("'","") + ").T")
            print("Y_" + str(i) + " = np.array(" + str(allY).replace("'","") + ").T")
            if checkEqualIvo(allX) == True:
                print("plt.plot(" + allX[0] + ", Y_" + str(i) + ")")
            else:
                print("plt.plot(X_" + str(i) + ", Y_" + str(i) + ")")
            if curve.getLogX() == True:
                print("plt.xscale('log')")
            if curve.getLogY() == True:
                print("plt.yscale('log')")
            if output.getName() != '':
                print("plt.title('" + output.getName() + "')")
            else:
                print("plt.title('" + output.getId() + "')")
            print("plt.show()\n")
        elif typeCode == libsedml.SEDML_OUTPUT_PLOT3D:
            print("from mpl_toolkits.mplot3d import Axes3D")
            print("fig = plt.figure()")
            print("ax = fig.gca(projection='3d')")
            for x in range(0, sedmlDoc.getNumTasks()):
                task1 = sedmlDoc.getTask(x)
                taskList.append(task1.getElementName())
            if "repeatedTask" in taskList:    #For repeated tasks
                for y in range(0, sedmlDoc.getNumTasks()):
                    task1 = sedmlDoc.getTask(y)
                    if task1.getElementName() == "repeatedTask":
                        for z in range(0, task1.getNumSubTasks()):
                            aRange = task1.getRange(0)
                            for l in range(0, aRange.getNumberOfPoints()):
                                if output.getNumSurfaces() > 1:
                                    allX = []
                                    allY = []
                                    allZ = []
                                    for q in range(0, output.getNumSurfaces()):
                                        surface = output.getSurface(q)
                                        xDataReference = surface.getXDataReference()
                                        yDataReference = surface.getYDataReference()
                                        zDataReference = surface.getZDataReference()
                                        for k, v in mapping:
                                            xDataReference = xDataReference.replace(k, v)
                                            yDataReference = yDataReference.replace(k, v)
                                            zDataReference = zDataReference.replace(k, v)
                                        if not len(dataGeneratorsList) == 0:
                                            allX.append(xDataReference + "_" + str(i))
                                            allY.append(yDataReference + "_" + str(i))
                                            allZ.append(zDataReference + "_" + str(i))
                                        else:
                                            allX.append(xDataReference)
                                            allY.append(yDataReference)
                                            allZ.append(zDataReference)
            elif "repeatedTask" not in taskList:    #There is no repeated tasks
                if output.getNumSurfaces() > 0:
                    allX = []
                    allY = []
                    allZ = []
                    for m in range(0, output.getNumSurfaces()):
                        surface = output.getSurface(m)
                        xDataReference = surface.getXDataReference()
                        yDataReference = surface.getYDataReference()
                        zDataReference = surface.getZDataReference()
                        for k, v in mapping:
                            xDataReference = xDataReference.replace(k, v)
                            yDataReference = yDataReference.replace(k, v)
                            zDataReference = zDataReference.replace(k, v)
                        if not len(dataGeneratorsList) == 0:
                            allX.append(xDataReference + "_" + str(i))
                            allY.append(yDataReference + "_" + str(i))
                            allZ.append(zDataReference + "_" + str(i))
                        else:
                            allX.append(xDataReference)
                            allY.append(yDataReference)
                            allZ.append(zDataReference)
            #print "X_" + str(i) + " = np.array(" + str(allX).replace("'","") + ").T"
            #print "Y_" + str(i) + " = np.array(" + str(allY).replace("'","") + ").T"
            #print "Z_" + str(i) + " = np.array(" + str(allZ).replace("'","") + ").T"
            for x in range(len(allX)):
                print("ax.plot(" + str(allX[x]) + ", " + str(allY[x]) + ", " + str(allZ[x]) + ")")
            if output.getName() != '':
                print("plt.title('" + output.getName() + "')")
            else:
                print("plt.title('" + output.getId() + "')")
            print("plt.show()\n")
        else:
            print("# Unsupported output type")


def isId(string):
    regular = re.compile('[\\/:-]')               # a SedML Id cannot contain these characters
    if regular.search(string):
        return False
    else:
        return True


def checkEqualIvo(lst):
    return not lst or lst.count(lst[0]) == len(lst)


if __name__ == "__main__":
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'tests', 'testdata', 'sedml')
    f_sedml = os.path.join(test_dir, 'app2sim', 'app2sim.sedml')
    python_str = sedml_to_python(f_sedml)
    print(python_str)


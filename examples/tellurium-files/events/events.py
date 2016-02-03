#!/usr/bin/env python
"""
Functions to work with event triggers and event handling.
Example demonstrates ho to attach such function.
"""
import roadrunner


# --------------------------------------------------
# Event handling functions
# --------------------------------------------------
def onEventTrigger(model, eventIndex, eventId):
    print("event {} was triggered at time {}".format(eventId, model.getTime()))


def onEventAssignment(model, eventIndex, eventId):
    print("event {} was assignend at time {}".format(eventId, model.getTime()))


def testEvents(filePath):
    """ Attaches eventTrigger and eventAssignment functions to events.
        Runs simulation.

    :param filePath:
    :type filePath:
    """
    r = roadrunner.RoadRunner(filePath)
    eventIds = r.model.getEventIds()

    for eid in eventIds:
        e = r.model.getEvent(eid)
        e.setOnTrigger(onEventTrigger)
        e.setOnAssignment(onEventAssignment)

    r.simulate()


# --------------------------------------------------
# Integration handling function
# --------------------------------------------------
def onTimeStep(integrator, model, time):
    """ Is called after the internal integrator completes each internal time step. """
    print("onTimeStep, time: {}".format(time))


def onEvent(integrator, model, time):
    """ Whenever model event occurs and after it is procesed."""
    print("onEvent, time: {}".format(time))


def testMultiStepIntegrator(filePath, t0, tf, dt, minStep = -1, maxStep=-1):
    r = roadrunner.RoadRunner(filePath)

    listener = roadrunner.PyIntegratorListener()
    listener.setOnTimeStep(onTimeStep)
    listener.setOnEvent(onEvent)
    
    r.getIntegrator().setListener(listener)
    
    r.simulateOptions.integratorFlags = roadrunner.SimulateOptions.MULTI_STEP
    r.simulateOptions.initialTimeStep = dt
    r.simulateOptions.maximumTimeStep = maxStep
    r.simulateOptions.minimumTimeStep = minStep
    r.integrate(t0, tf)


#!/usr/bin/env python

import roadrunner 

retval = 0

## event handling functions
def onEventTrigger(model, eventIndex, eventId):
    print("event {} was triggered at time {}".format(eventId, model.getTime()))


def onEventAssignment(model, eventIndex, eventId):
    print("event {} was assignend at time {}".format(eventId, model.getTime()))

def testEvents(fileName):
    r=roadrunner.RoadRunner(fileName)

    eventIds = r.model.getEventIds()

    for eid in eventIds:
        e=r.model.getEvent(eid)
        e.setOnTrigger(onEventTrigger)
        e.setOnAssignment(onEventAssignment)

    r.simulate()

## integration handling functions

def onTimeStep(integrator, model, time):
    """
    is called after the internal integrator completes each internal time step.
    """
    print("onTimeStep, time: {}".format(time))

def onEvent(integrator, model, time):
    """
    whenever model event occurs and after it is procesed.
    """
    print("onEvent, time: {}".format(time))

def testMultiStepIntegrator(fname, t0, tf, dt, minStep = -1, maxStep=-1):
    r=roadrunner.RoadRunner(fname)

    listener = roadrunner.PyIntegratorListener()
    listener.setOnTimeStep(onTimeStep)
    listener.setOnEvent(onEvent)
    
    r.getIntegrator().setListener(listener)
    
    r.simulateOptions.integratorFlags = roadrunner.SimulateOptions.MULTI_STEP
    r.simulateOptions.initialTimeStep = dt
    r.simulateOptions.maximumTimeStep = maxStep
    r.simulateOptions.minimumTimeStep = minStep
    r.integrate(t0, tf)


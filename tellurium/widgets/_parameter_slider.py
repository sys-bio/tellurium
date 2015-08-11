from IPython.html.widgets import interact
from IPython.html import widgets
import sys

def simulateAndPlot(r, start, end, steps, selection=None):
    import tellurium as te
    if selection is None:
        result = r.simulate(start, end, steps)
    else:
        result = r.simulate(start, end, steps, selection)
    te.plotWithLegend(r, result)

class ParameterSlider():
    """
    Create interactive sliders to change model parameters.

    r - roadrunner instance with model loaded
    paramIds (optional) - list of parameter ids to create sliders,
                          by default creates slider for every parameter
    minFactor (optional) - scale factor multiplied with parameter value,
                           to determine minimum value of slider
    maxFactor (optional) - scale factor multiplied with parameter value,
                           to determine maximum value of slider
    sliderStepFactor (optional) - scale factor divided with parameter value,
                                  to determine step size of slider

    Example Usage:

    import tellurium as te
    from biomodeltoolbox.widgets import ParameterSlider
    model = '''
      model pathway()
        S1 -> S2; k1*S1 - k2*S2 # Reversible term added here

        # Initialize values
        S1 = 5; S2 = 0;
        k1 = 0.1;  k2 = 0.05;

      end
    '''
    r = te.loadAntimonyModel(model)
    ParameterSlider(r, paramIds=['k1'])
    """


    def __init__(self, r,
                 paramIds=None,
                 minFactor=0,
                 maxFactor=2,
                 sliderStepFactor=10,
                 selection=None,
                 simulateAndPlot=simulateAndPlot
                 ):

        if paramIds is None:
            paramIds = r.model.getGlobalParameterIds()
        paramMap = {}

        def runSim(start=0, stop=100, steps=100, **paramMap):
            r.reset()
            for k, v in paramMap.items():
                try:
                    key = k.encode('ascii', 'ignore')
                    r[key] = v
                except:
                    # error in setting model variable
                    e = sys.exc_info()
                    print e

            try:
                simulateAndPlot(r, start, stop, steps, selection)
            except:
                # error in simulation
                e = sys.exc_info()
                print e

        for i, id in enumerate(paramIds):
            val = r[id]
            try:
                r[id] = val
                paramMap[id] = widgets.FloatSliderWidget(
                    min=minFactor*val,
                    max=maxFactor*val,
                    step=val/sliderStepFactor,
                    value=val)
            except:
                e = sys.exc_info()
                print e

        interact(runSim,
                 start=widgets.FloatTextWidget(min=0, value=0),
                 stop=widgets.FloatTextWidget(min=0, value=100),
                 steps=widgets.IntTextWidget(min=0, value=100),
                 **paramMap
                 )

# tellurium
Copyright 2014  
Michal Galdzicki, Herbert Sauro

Tellurium is a python environment based on the spyder2 IDE that can be used for model construction and simulation in systems and synthetic biology. It combines a number of existing libraries, including libSBML, libRoadRunner (including libStruct), libAntimony.

In addition full access is available to other tools kits such as matplotlib.

The Tellurium project is funded from the NIH/NIGMS (GM081070).

Tellurium code is licensed under the Apache License, Version 2.0. Temporarily use PyQt4 GPL licensed code. Licences used include LGPL, Apache 2, MIT, and BSD.

**Usage**
```{python}
import tellurium as te

rr = te.loada('''
    model example0
      S1 -> S2; k1*S1
      S1 = 10
      S2 = 0
      k1 = 0.1
    end
''')

result = rr.simulate(0, 40, 500) 
te.plotArray(result)
```


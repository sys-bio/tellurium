

Steady state scan
~~~~~~~~~~~~~~~~~

Using ``te.ParameterScan.SteadyStateScan`` for scanning the steady
state.

.. code-block:: python

    import tellurium as te
    import matplotlib.pyplot as plt
    import tellurium as te
    import numpy as np
    from roadrunner import Config
    
    r = te.loada('''
        $Xo -> S1; vo;
        S1 -> S2; k1*S1 - k2*S2;
        S2 -> $X1; k3*S2;
        
        vo = 1
        k1 = 2; k2 = 0; k3 = 3;
    ''')
    
    p = te.SteadyStateScan(r,
        value = 'k3',
        startValue = 2,
        endValue = 3,
        numberOfPoints = 20,
        selection = ['S1', 'S2']                      
    )
    p.plotArray()



.. image:: _notebooks/core/steadystate_scan_files/steadystate_scan_2_0.png




.. parsed-literal::

    array([[2.05263158, 0.5       , 0.48717949],
           [2.10526316, 0.5       , 0.475     ],
           [2.15789474, 0.5       , 0.46341463],
           [2.21052632, 0.5       , 0.45238095],
           [2.26315789, 0.5       , 0.44186047],
           [2.31578947, 0.5       , 0.43181818],
           [2.36842105, 0.5       , 0.42222222],
           [2.42105263, 0.5       , 0.41304348],
           [2.47368421, 0.5       , 0.40425532],
           [2.52631579, 0.5       , 0.39583333],
           [2.57894737, 0.5       , 0.3877551 ],
           [2.63157895, 0.5       , 0.38      ],
           [2.68421053, 0.5       , 0.37254902],
           [2.73684211, 0.5       , 0.36538462],
           [2.78947368, 0.5       , 0.35849057],
           [2.84210526, 0.5       , 0.35185185],
           [2.89473684, 0.5       , 0.34545455],
           [2.94736842, 0.5       , 0.33928571],
           [3.        , 0.5       , 0.33333333],
           [3.05263158, 0.5       , 0.32758621]])



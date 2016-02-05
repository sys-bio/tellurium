

Interactive Parameter Slider
============================

Interactive parameter slider for IPython Notebooks and roadrunner
models.

.. code:: python


.. code:: python

    
    import tellurium as te
    from tellurium.widgets import ParameterSlider
    
    r = te.loada('''
          model pathway()
            S1 -> S2; k1*S1 - k2*S2 # Reversible term added here
    
            # Initialize values
            S1 = 5; S2 = 0;
            k1 = 0.1;  k2 = 0.05;
    
          end
    ''')

.. code:: python

    ParameterSlider(r, paramIds=['k1', 'k2']);



.. image:: _notebooks/core/widgets_parameter_slider_files/widgets_parameter_slider_4_0.png



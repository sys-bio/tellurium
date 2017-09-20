
.. code-block:: python

    import tellurium as te
    # install cobra (https://github.com/opencobra/cobrapy)
    te.installPackage('cobra')
    # update cobra to latest version
    te.upgradePackage('cobra')
    # remove cobra
    # te.removePackage('cobra')



.. raw:: html

    <script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window.Plotly) {{require(['plotly'],function(plotly) {window.Plotly=plotly;});}}</script>


.. parsed-literal::

    Requirement already satisfied: cobra in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages
    Requirement already satisfied: numpy>=1.6 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already satisfied: tabulate in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already satisfied: future in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already satisfied: swiglpk in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already satisfied: pandas>=0.17.0 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already satisfied: optlang>=1.2.1 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already satisfied: ruamel.yaml<0.15 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already satisfied: pytz>=2011k in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from pandas>=0.17.0->cobra)
    Requirement already satisfied: python-dateutil>=2 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from pandas>=0.17.0->cobra)
    Requirement already satisfied: sympy>=1.0.0 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from optlang>=1.2.1->cobra)
    Requirement already satisfied: six>=1.9.0 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from optlang>=1.2.1->cobra)
    Requirement already satisfied: mpmath>=0.19 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from sympy>=1.0.0->optlang>=1.2.1->cobra)
    Requirement already up-to-date: cobra in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages
    Requirement already up-to-date: numpy>=1.6 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already up-to-date: tabulate in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already up-to-date: future in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already up-to-date: swiglpk in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already up-to-date: pandas>=0.17.0 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already up-to-date: optlang>=1.2.1 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already up-to-date: ruamel.yaml<0.15 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from cobra)
    Requirement already up-to-date: pytz>=2011k in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from pandas>=0.17.0->cobra)
    Requirement already up-to-date: python-dateutil>=2 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from pandas>=0.17.0->cobra)
    Requirement already up-to-date: sympy>=1.0.0 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from optlang>=1.2.1->cobra)
    Requirement already up-to-date: six>=1.9.0 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from optlang>=1.2.1->cobra)
    Requirement already up-to-date: mpmath>=0.19 in /home/poltergeist/.config/Tellurium/telocal/python-3.6.1/lib/python3.6/site-packages (from sympy>=1.0.0->optlang>=1.2.1->cobra)


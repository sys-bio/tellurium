

tesedml
~~~~~~~

Simulations can be described within SED-ML, the Simulation Experiment
Description Markup Language (http://sed-ml.org/). SED-ML is an XML-based
format for encoding simulation setups, to ensure exchangeability and
reproducibility of simulation experiments.

| *Reproducible computational biology experiments with SED-ML - The
Simulation Experiment Description Markup Language.*
| Waltemath D., Adams R., Bergmann F.T., Hucka M., Kolpakov F., Miller
A.K., Moraru I.I., Nickerson D., Snoep J.L.,Le Novère, N.
| BMC Systems Biology 2011, 5:198 (http://www.pubmed.org/22172142)

Tellurium supports SED-ML via the packages ``tesedml`` and
``tephrasedml``. #### Creating SED-ML file

.. code:: python

    import tellurium as te
    import phrasedml
    
    antimony_str = '''
    model myModel
      S1 -> S2; k1*S1
      S1 = 10; S2 = 0
      k1 = 1
    end
    '''
    
    phrasedml_str = '''
      model1 = model "myModel"
      sim1 = simulate uniform(0, 5, 100)
      task1 = run sim1 on model1
      plot "Figure 1" time vs S1, S2
    '''
    
    # create the sedml xml string from the phrasedml
    sbml_str = te.antimonyTosbml(antimony_str)
    phrasedml.setReferencedSBML("myModel", sbml_str)
    
    sedml_str = phrasedml.convertString(phrasedml_str)
    if sedml_str == None:
        print(phrasedml.getLastPhrasedError())
    print(sedml_str)


::


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-1-29fbe2e89b23> in <module>()
         20 
         21 # create the sedml xml string from the phrasedml
    ---> 22 sbml_str = te.antimonyTosbml(antimony_str)
         23 phrasedml.setReferencedSBML("myModel", sbml_str)
         24 


    AttributeError: 'module' object has no attribute 'antimonyTosbml'


.. code:: python

    # Create the temporary files and execute the code
    import tempfile
    f_sbml = tempfile.NamedTemporaryFile(prefix="myModel", suffix=".xml")
    f_sbml.write(sbml_str)
    f_sbml.flush()
    print(f_sbml.name)
    
    f_sedml = tempfile.NamedTemporaryFile(suffix=".sedml")
    f_sedml.write(sedml_str)
    f_sedml.flush()
    print(f_sedml.name)
    
    import libsedml
    sedml_doc = libsedml.readSedML(f_sedml.name)
    if sedml_doc.getErrorLog().getNumFailsWithSeverity(libsedml.LIBSEDML_SEV_ERROR) > 0:
        print(sedml_doc.getErrorLog().toString())
    
    f_sbml.close()
    f_sedml.close()
    
    # Create executable python code sedml with roadrunner
    # import tellurium.tesedml as s2p
    # s2p.sedml_to_python(s2p)


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-2-366616856903> in <module>()
          2 import tempfile
          3 f_sbml = tempfile.NamedTemporaryFile(prefix="myModel", suffix=".xml")
    ----> 4 f_sbml.write(sbml_str)
          5 f_sbml.flush()
          6 print(f_sbml.name)


    NameError: name 'sbml_str' is not defined



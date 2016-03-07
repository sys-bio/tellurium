

tesedml
~~~~~~~

Simulations can be described within SED-ML, the Simulation Experiment
Description Markup Language (http://sed-ml.org/). SED-ML is an XML-based
format for encoding simulation setups, to ensure exchangeability and
reproducibility of simulation experiments.

    Reproducible computational biology experiments with SED-ML - The
    Simulation Experiment Description Markup Language. Waltemath D.,
    Adams R., Bergmann F.T., Hucka M., Kolpakov F., Miller A.K., Moraru
    I.I., Nickerson D., Snoep J.L.,Le Novère, N. BMC Systems Biology
    2011, 5:198 (http://www.pubmed.org/22172142)

Tellurium supports SED-ML via the packages ``tesedml`` and
``tephrasedml``.

Creating SED-ML file
^^^^^^^^^^^^^^^^^^^^

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
    sbml_str = te.antimonyToSBML(antimony_str)
    phrasedml.setReferencedSBML("myModel", sbml_str)
    
    sedml_str = phrasedml.convertString(phrasedml_str)
    if sedml_str == None:
        print(phrasedml.getLastPhrasedError())
    print(sedml_str)


.. parsed-literal::

    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Created by phraSED-ML version v1.0.1 on 2016-03-07 15:45 with libSBML version 5.12.1. -->
    <sedML xmlns="http://sed-ml.org/sed-ml/level1/version2" level="1" version="2">
      <listOfSimulations>
        <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="5" numberOfPoints="100">
          <algorithm kisaoID="KISAO:0000019"/>
        </uniformTimeCourse>
      </listOfSimulations>
      <listOfModels>
        <model id="model1" language="urn:sedml:language:sbml.level-3.version-1" source="myModel"/>
      </listOfModels>
      <listOfTasks>
        <task id="task1" modelReference="model1" simulationReference="sim1"/>
      </listOfTasks>
      <listOfDataGenerators>
        <dataGenerator id="plot_0_0_0" name="time">
          <listOfVariables>
            <variable id="time" symbol="urn:sedml:symbol:time" taskReference="task1"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> time </ci>
          </math>
        </dataGenerator>
        <dataGenerator id="plot_0_0_1" name="S1">
          <listOfVariables>
            <variable id="S1" target="/sbml:sbml/sbml:model/descendant::*[@id='S1']" taskReference="task1" modelReference="model1"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> S1 </ci>
          </math>
        </dataGenerator>
        <dataGenerator id="plot_0_1_1" name="S2">
          <listOfVariables>
            <variable id="S2" target="/sbml:sbml/sbml:model/descendant::*[@id='S2']" taskReference="task1" modelReference="model1"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> S2 </ci>
          </math>
        </dataGenerator>
      </listOfDataGenerators>
      <listOfOutputs>
        <plot2D id="plot_0" name="Figure 1">
          <listOfCurves>
            <curve logX="false" logY="false" xDataReference="plot_0_0_0" yDataReference="plot_0_0_1"/>
            <curve logX="false" logY="false" xDataReference="plot_0_0_0" yDataReference="plot_0_1_1"/>
          </listOfCurves>
        </plot2D>
      </listOfOutputs>
    </sedML>
    


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
    # py_code = s2p.sedml_to_python(s2p)


.. parsed-literal::

    /tmp/myModelG2F3dU.xml
    /tmp/tmpBxMyz0.sedml


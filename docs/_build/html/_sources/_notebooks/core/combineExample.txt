

Combine archives
~~~~~~~~~~~~~~~~

The experiment, i.e. model with the simulation description, can be
stored as Combine Archive.

.. code:: python

    import tellurium as te
    
    antimonyStr = """
    model test()
        J0: S1 -> S2; k1*S1;
        S1 = 10.0; S2=0.0;
        k1 = 0.1;
    end
    """
    
    phrasedmlStr = """
        model0 = model "test"
        sim0 = simulate uniform(0, 6, 100)
        task0 = run sim0 on model0
        plot "Timecourse test model" task0.time vs task0.S1
    """
    
    # phrasedml experiment
    exp = te.experiment(antimonyStr, phrasedmlStr)
    exp.execute(phrasedmlStr)
    
    # create Combine Archive
    import tempfile
    f = tempfile.NamedTemporaryFile()
    exp.exportAsCombine(f.name)
    
    # print the content of the Combine Archive
    import zipfile
    zip=zipfile.ZipFile(f.name)
    print(zip.namelist())



.. image:: _notebooks/core/combineExample_files/combineExample_2_0.png


.. parsed-literal::

    ['test.xml', 'experiment1.xml', 'manifest.xml']


Create combine archive
~~~~~~~~~~~~~~~~~~~~~~

TODO

.. code:: python

    import tellurium as te
    import phrasedml
    
    antTest1Str = """
    model test1()
        J0: S1 -> S2; k1*S1;
        S1 = 10.0; S2=0.0;
        k1 = 0.1;
    end
    """
    
    antTest2Str = """
    model test2()
        v0: X1 -> X2; p1*X1;
        X1 = 5.0; X2 = 20.0;
        k1 = 0.2;
    end
    """
    
    phrasedmlStr = """
        model1 = model "test1"
        model2 = model "test2"
        model3 = model model1 with S1=S2+20
        sim1 = simulate uniform(0, 6, 100)
        task1 = run sim1 on model1
        task2 = run sim1 on model2
        plot "Timecourse test1" task1.time vs task1.S1, task1.S2
        plot "Timecourse test2" task2.time vs task2.X1, task2.X2
    """
    
    # phrasedml.setReferencedSBML("test1")
    exp = te.experiment(phrasedmlList=[phrasedmlStr], antimonyList=[antTest1Str])
    print(exp)
    
    # set first model
    phrasedml.setReferencedSBML("test1", te.antimonyToSBML(antTest1Str))
    phrasedml.setReferencedSBML("test2", te.antimonyToSBML(antTest2Str))
    
    sedmlstr = phrasedml.convertString(phrasedmlStr)
    if sedmlstr is None:
        raise Exception(phrasedml.getLastError())
    print(sedmlstr)


.. parsed-literal::

    <tellurium.sedml.tephrasedml.experiment object at 0x7f6faa81b5d0>
    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Created by phraSED-ML version v1.0.1 on 2016-03-09 12:23 with libSBML version 5.12.1. -->
    <sedML xmlns="http://sed-ml.org/sed-ml/level1/version2" level="1" version="2">
      <listOfSimulations>
        <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="6" numberOfPoints="100">
          <algorithm kisaoID="KISAO:0000019"/>
        </uniformTimeCourse>
      </listOfSimulations>
      <listOfModels>
        <model id="model1" language="urn:sedml:language:sbml.level-3.version-1" source="test1"/>
        <model id="model2" language="urn:sedml:language:sbml.level-3.version-1" source="test2"/>
        <model id="model3" language="urn:sedml:language:sbml.level-3.version-1" source="model1">
          <listOfChanges>
            <computeChange target="/sbml:sbml/sbml:model/descendant::*[@id='S1']">
              <listOfVariables>
                <variable id="S2" target="/sbml:sbml/sbml:model/descendant::*[@id='S2']" modelReference="model3"/>
              </listOfVariables>
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <apply>
                  <plus/>
                  <ci> S2 </ci>
                  <cn type="integer"> 20 </cn>
                </apply>
              </math>
            </computeChange>
          </listOfChanges>
        </model>
      </listOfModels>
      <listOfTasks>
        <task id="task1" modelReference="model1" simulationReference="sim1"/>
        <task id="task2" modelReference="model2" simulationReference="sim1"/>
      </listOfTasks>
      <listOfDataGenerators>
        <dataGenerator id="plot_0_0_0" name="task1.time">
          <listOfVariables>
            <variable id="task1_____time" symbol="urn:sedml:symbol:time" taskReference="task1"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> task1_____time </ci>
          </math>
        </dataGenerator>
        <dataGenerator id="plot_0_0_1" name="task1.S1">
          <listOfVariables>
            <variable id="task1_____S1" target="/sbml:sbml/sbml:model/descendant::*[@id='S1']" taskReference="task1" modelReference="model1"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> task1_____S1 </ci>
          </math>
        </dataGenerator>
        <dataGenerator id="plot_0_1_1" name="task1.S2">
          <listOfVariables>
            <variable id="task1_____S2" target="/sbml:sbml/sbml:model/descendant::*[@id='S2']" taskReference="task1" modelReference="model1"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> task1_____S2 </ci>
          </math>
        </dataGenerator>
        <dataGenerator id="plot_1_0_0" name="task2.time">
          <listOfVariables>
            <variable id="task2_____time" symbol="urn:sedml:symbol:time" taskReference="task2"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> task2_____time </ci>
          </math>
        </dataGenerator>
        <dataGenerator id="plot_1_0_1" name="task2.X1">
          <listOfVariables>
            <variable id="task2_____X1" target="/sbml:sbml/sbml:model/descendant::*[@id='X1']" taskReference="task2" modelReference="model2"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> task2_____X1 </ci>
          </math>
        </dataGenerator>
        <dataGenerator id="plot_1_1_1" name="task2.X2">
          <listOfVariables>
            <variable id="task2_____X2" target="/sbml:sbml/sbml:model/descendant::*[@id='X2']" taskReference="task2" modelReference="model2"/>
          </listOfVariables>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> task2_____X2 </ci>
          </math>
        </dataGenerator>
      </listOfDataGenerators>
      <listOfOutputs>
        <plot2D id="plot_0" name="Timecourse test1">
          <listOfCurves>
            <curve logX="false" logY="false" xDataReference="plot_0_0_0" yDataReference="plot_0_0_1"/>
            <curve logX="false" logY="false" xDataReference="plot_0_0_0" yDataReference="plot_0_1_1"/>
          </listOfCurves>
        </plot2D>
        <plot2D id="plot_1" name="Timecourse test2">
          <listOfCurves>
            <curve logX="false" logY="false" xDataReference="plot_1_0_0" yDataReference="plot_1_0_1"/>
            <curve logX="false" logY="false" xDataReference="plot_1_0_0" yDataReference="plot_1_1_1"/>
          </listOfCurves>
        </plot2D>
      </listOfOutputs>
    </sedML>
    




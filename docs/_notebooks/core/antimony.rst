

Antimony model building
~~~~~~~~~~~~~~~~~~~~~~~

Description Text

.. code:: python

    import tellurium as te
    
    print('-' * 80)
    te.printVersionInfo()
    print('-' * 80)
    
    r = te.loada('''
    model example
        p1 = 0;
        at time>=10: p1=10;
        at time>=20: p1=0;
    end
    ''')
    
    # look at model
    ant_str = r.getCurrentAntimony()
    sbml_str = r.getCurrentSBML()
    print(ant_str)
    print(sbml_str)
    # r.exportToSBML('/home/mkoenig/Desktop/test.xml')
    
    # set selections
    r.selections=['time', 'p1']
    r.integrator.setValue("variable_step_size", False)
    s1 = r.simulate(0, 40, 40)
    r.plot()
    print(s1)
    # hitting the trigger point directly works
    s2 = r.simulate(0, 40, 21)
    r.plot()
    print(s2)
    
    # variable step size also does not work
    r.integrator.setValue("variable_step_size", True)
    s3 = r.simulate(0, 40)
    r.plot()
    print(s3)


.. parsed-literal::

    --------------------------------------------------------------------------------
    tellurium : 1.3.0
    roadrunner : 1.4.2; Compiler: gcc 4.8.4, C++ version: 199711; JIT Compiler: LLVM-3.4; Date: Feb  3 2016, 08:19:01; LibSBML Version: 5.12.0
    antimony : v2.8.0
    snbw_viewer : No information for sbnw viewer
    libsbml : 5.12.1
    libsedml : 401
    phrasedml : v0.5 beta
    --------------------------------------------------------------------------------
    // Created by libAntimony v2.8.1
    model *example()
    
      // Events:
      _E0: at time >= 10: p1 = 10;
      _E1: at time >= 20: p1 = 0;
    
      // Variable initializations:
      p1 = 0;
    
      // Other declarations:
      var p1;
    end
    
    <?xml version="1.0" encoding="UTF-8"?>
    <sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
      <model id="example" name="example">
        <listOfParameters>
          <parameter id="p1" value="0" constant="false"/>
        </listOfParameters>
        <listOfEvents>
          <event id="_E0" useValuesFromTriggerTime="true">
            <trigger initialValue="true" persistent="true">
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <apply>
                  <geq/>
                  <csymbol encoding="text" definitionURL="http://www.sbml.org/sbml/symbols/time"> time </csymbol>
                  <cn type="integer"> 10 </cn>
                </apply>
              </math>
            </trigger>
            <listOfEventAssignments>
              <eventAssignment variable="p1">
                <math xmlns="http://www.w3.org/1998/Math/MathML">
                  <cn type="integer"> 10 </cn>
                </math>
              </eventAssignment>
            </listOfEventAssignments>
          </event>
          <event id="_E1" useValuesFromTriggerTime="true">
            <trigger initialValue="true" persistent="true">
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <apply>
                  <geq/>
                  <csymbol encoding="text" definitionURL="http://www.sbml.org/sbml/symbols/time"> time </csymbol>
                  <cn type="integer"> 20 </cn>
                </apply>
              </math>
            </trigger>
            <listOfEventAssignments>
              <eventAssignment variable="p1">
                <math xmlns="http://www.w3.org/1998/Math/MathML">
                  <cn type="integer"> 0 </cn>
                </math>
              </eventAssignment>
            </listOfEventAssignments>
          </event>
        </listOfEvents>
      </model>
    </sbml>
    



.. image:: _notebooks/core/antimony_files/antimony_2_1.png


.. parsed-literal::

           time, p1
     [[       0,  0],
      [ 1.02564,  0],
      [ 2.05128,  0],
      [ 3.07692,  0],
      [ 4.10256,  0],
      [ 5.12821,  0],
      [ 6.15385,  0],
      [ 7.17949,  0],
      [ 8.20513,  0],
      [ 9.23077,  0],
      [ 10.2564, 10],
      [ 11.2821, 10],
      [ 12.3077, 10],
      [ 13.3333, 10],
      [  14.359, 10],
      [ 15.3846, 10],
      [ 16.4103, 10],
      [ 17.4359, 10],
      [ 18.4615, 10],
      [ 19.4872, 10],
      [ 20.5128,  0],
      [ 21.5385,  0],
      [ 22.5641,  0],
      [ 23.5897,  0],
      [ 24.6154,  0],
      [  25.641,  0],
      [ 26.6667,  0],
      [ 27.6923,  0],
      [ 28.7179,  0],
      [ 29.7436,  0],
      [ 30.7692,  0],
      [ 31.7949,  0],
      [ 32.8205,  0],
      [ 33.8462,  0],
      [ 34.8718,  0],
      [ 35.8974,  0],
      [ 36.9231,  0],
      [ 37.9487,  0],
      [ 38.9744,  0],
      [      40,  0]]
    



.. image:: _notebooks/core/antimony_files/antimony_2_3.png


.. parsed-literal::

        time, p1
     [[    0,  0],
      [    2,  0],
      [    4,  0],
      [    6,  0],
      [    8,  0],
      [   10, 10],
      [   12, 10],
      [   14, 10],
      [   16, 10],
      [   18, 10],
      [   20,  0],
      [   22,  0],
      [   24,  0],
      [   26,  0],
      [   28,  0],
      [   30,  0],
      [   32,  0],
      [   34,  0],
      [   36,  0],
      [   38,  0],
      [   40,  0]]
    



.. image:: _notebooks/core/antimony_files/antimony_2_5.png


.. parsed-literal::

             time, p1
     [[         0,  0],
      [ 0.0013729,  0],
      [        10,  0],
      [        10, 10],
      [   10.0015, 10],
      [        20, 10],
      [        20,  0],
      [   20.0015,  0],
      [   35.1952,  0],
      [        40,  0]]
    


.. code:: python

    r.getSimulationData()




.. parsed-literal::

             time, p1
     [[         0,  0],
      [ 0.0013729,  0],
      [        10,  0],
      [        10, 10],
      [   10.0015, 10],
      [        20, 10],
      [        20,  0],
      [   20.0015,  0],
      [   35.1952,  0],
      [        40,  0]]




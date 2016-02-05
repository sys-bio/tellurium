

SBML
^^^^

.. code:: python

    import tellurium as te
    import tempfile
    
    # load model
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    # file for export
    f_sbml = tempfile.NamedTemporaryFile(suffix=".xml")
    
    # export current model state
    r.exportToSBML(f_sbml.name)
    
    # to export the initial state when the model was loaded
    # set the current argument to False
    r.exportToSBML(f_sbml.name, current=False)
    
    # The string representations of the current model are available via
    str_sbml = r.getCurrentSBML()
    
    # and of the initial state when the model was loaded via
    str_sbml = r.getSBML()
    print(str_sbml)


.. parsed-literal::

    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Created by libAntimony version v2.8.1 on 2016-02-05 16:24 with libSBML version 5.12.1. -->
    <sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
      <model id="__main" name="__main">
        <listOfCompartments>
          <compartment sboTerm="SBO:0000410" id="default_compartment" spatialDimensions="3" size="1" constant="true"/>
        </listOfCompartments>
        <listOfSpecies>
          <species id="S1" compartment="default_compartment" initialConcentration="10" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
          <species id="S2" compartment="default_compartment" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
        </listOfSpecies>
        <listOfParameters>
          <parameter id="k1" value="0.1" constant="true"/>
        </listOfParameters>
        <listOfReactions>
          <reaction id="_J0" reversible="true" fast="false">
            <listOfReactants>
              <speciesReference species="S1" stoichiometry="1" constant="true"/>
            </listOfReactants>
            <listOfProducts>
              <speciesReference species="S2" stoichiometry="1" constant="true"/>
            </listOfProducts>
            <kineticLaw>
              <math xmlns="http://www.w3.org/1998/Math/MathML">
                <apply>
                  <times/>
                  <ci> k1 </ci>
                  <ci> S1 </ci>
                </apply>
              </math>
            </kineticLaw>
          </reaction>
        </listOfReactions>
      </model>
    </sbml>
    


Antimony
^^^^^^^^

.. code:: python

    import tellurium as te
    import tempfile
    
    # load model
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    # file for export
    f_antimony = tempfile.NamedTemporaryFile(suffix=".txt")
    
    # export current model state
    r.exportToAntimony(f_antimony.name)
    
    # to export the initial state when the model was loaded
    # set the current argument to False
    r.exportToAntimony(f_antimony.name, current=False)
    
    # The string representations of the current model are available via
    str_antimony = r.getCurrentAntimony()
    
    # and of the initial state when the model was loaded via
    str_antimony = r.getAntimony()
    print(str_antimony)


.. parsed-literal::

    // Created by libAntimony v2.8.1
    // Compartments and Species:
    species S1, S2;
    
    // Reactions:
    _J0: S1 -> S2; k1*S1;
    
    // Species initializations:
    S1 = 10;
    S2 = ;
    
    // Variable initializations:
    k1 = 0.1;
    
    // Other declarations:
    const k1;
    


CellML
^^^^^^

.. code:: python

    import tellurium as te
    import tempfile
    
    # load model
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    # file for export
    f_cellml = tempfile.NamedTemporaryFile(suffix=".cellml")
    
    # export current model state
    r.exportToCellML(f_cellml.name)
    
    # to export the initial state when the model was loaded
    # set the current argument to False
    r.exportToCellML(f_cellml.name, current=False)
    
    # The string representations of the current model are available via
    str_cellml = r.getCurrentCellML()
    
    # and of the initial state when the model was loaded via
    str_cellml = r.getCellML()
    print(str_cellml)


.. parsed-literal::

    <?xml version="1.0"?>
    <model xmlns:cellml="http://www.cellml.org/cellml/1.1#" xmlns="http://www.cellml.org/cellml/1.1#" name="__main">
    <component name="__main">
    <variable initial_value="10" name="S1" units="dimensionless"/>
    <variable name="S2" units="dimensionless"/>
    <variable initial_value="0.1" name="k1" units="dimensionless"/>
    <variable name="_J0" units="dimensionless"/>
    <math xmlns="http://www.w3.org/1998/Math/MathML">
    <apply>
    <eq/>
    <ci>_J0</ci>
    <apply>
    <times/>
    <ci>k1</ci>
    <ci>S1</ci>
    </apply>
    </apply>
    </math>
    <variable name="time" units="dimensionless"/>
    <math xmlns="http://www.w3.org/1998/Math/MathML">
    <apply>
    <eq/>
    <apply>
    <diff/>
    <bvar>
    <ci>time</ci>
    </bvar>
    <ci>S1</ci>
    </apply>
    <apply>
    <minus/>
    <ci>_J0</ci>
    </apply>
    </apply>
    </math>
    <math xmlns="http://www.w3.org/1998/Math/MathML">
    <apply>
    <eq/>
    <apply>
    <diff/>
    <bvar>
    <ci>time</ci>
    </bvar>
    <ci>S2</ci>
    </apply>
    <ci>_J0</ci>
    </apply>
    </math>
    </component>
    <group>
    <relationship_ref relationship="encapsulation"/>
    <component_ref component="__main"/>
    </group>
    </model>


Matlab
^^^^^^

.. code:: python

    import tellurium as te
    import tempfile
    
    # load model
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    # file for export
    f_matlab = tempfile.NamedTemporaryFile(suffix=".m")
    
    # export current model state
    r.exportToMatlab(f_matlab.name)
    
    # to export the initial state when the model was loaded
    # set the current argument to False
    r.exportToMatlab(f_matlab.name, current=False)
    
    # The string representations of the current model are available via
    str_matlab = r.getCurrentMatlab()
    
    # and of the initial state when the model was loaded via
    str_matlab = r.getMatlab()
    print(str_matlab)


.. parsed-literal::

    


.. parsed-literal::

    /home/mkoenig/git/tellurium/tellurium/tellurium.py:606: RuntimeWarning: 'sbml2matlab' could not be imported, no support for Matlab code generation
      saveToFile(filePath, self.getMatlab(current))
    /home/mkoenig/git/tellurium/tellurium/tellurium.py:564: RuntimeWarning: 'sbml2matlab' could not be imported, no support for Matlab code generation
      return self.getMatlab(current=True)
    /usr/local/lib/python2.7/dist-packages/ipykernel/__main__.py:20: RuntimeWarning: 'sbml2matlab' could not be imported, no support for Matlab code generation


.. code:: python

    import antimony
    antimony.loadAntimonyString('''S1 -> S2; k1*S1; k1 = 0.1; S1 = 10''')
    ant_str = antimony.getCellMLString(antimony.getMainModuleName())
    print(ant_str)


.. parsed-literal::

    <?xml version="1.0"?>
    <model xmlns:cellml="http://www.cellml.org/cellml/1.1#" xmlns="http://www.cellml.org/cellml/1.1#" name="__main">
    <component name="__main">
    <variable initial_value="10" name="S1" units="dimensionless"/>
    <variable name="S2" units="dimensionless"/>
    <variable initial_value="0.1" name="k1" units="dimensionless"/>
    <variable name="_J0" units="dimensionless"/>
    <math xmlns="http://www.w3.org/1998/Math/MathML">
    <apply>
    <eq/>
    <ci>_J0</ci>
    <apply>
    <times/>
    <ci>k1</ci>
    <ci>S1</ci>
    </apply>
    </apply>
    </math>
    <variable name="time" units="dimensionless"/>
    <math xmlns="http://www.w3.org/1998/Math/MathML">
    <apply>
    <eq/>
    <apply>
    <diff/>
    <bvar>
    <ci>time</ci>
    </bvar>
    <ci>S1</ci>
    </apply>
    <apply>
    <minus/>
    <ci>_J0</ci>
    </apply>
    </apply>
    </math>
    <math xmlns="http://www.w3.org/1998/Math/MathML">
    <apply>
    <eq/>
    <apply>
    <diff/>
    <bvar>
    <ci>time</ci>
    </bvar>
    <ci>S2</ci>
    </apply>
    <ci>_J0</ci>
    </apply>
    </math>
    </component>
    <group>
    <relationship_ref relationship="encapsulation"/>
    <component_ref component="__main"/>
    </group>
    </model>



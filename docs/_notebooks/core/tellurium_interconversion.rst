

Antimony, SBML, CellML
^^^^^^^^^^^^^^^^^^^^^^

Tellurium can convert between Antimony, SBML, and CellML.

.. code-block:: python

    import tellurium as te
    
    # antimony model
    ant_model = """
        S1 -> S2; k1*S1;
        S2 -> S3; k2*S2;
    
        k1= 0.1; k2 = 0.2; 
        S1 = 10; S2 = 0; S3 = 0;
    """
    
    # convert to SBML
    sbml_model = te.antimonyToSBML(ant_model)
    print('sbml_model')
    print('*'*80)
    # print first 10 lines
    for line in list(sbml_model.splitlines())[:10]:
        print(line)
    print('...')
        
    # convert to CellML
    cellml_model = te.antimonyToCellML(ant_model)
    print('cellml_model (from Antimony)')
    print('*'*80)
    # print first 10 lines
    for line in list(cellml_model.splitlines())[:10]:
        print(line)
    print('...')
    
    # or from the sbml
    cellml_model = te.sbmlToCellML(sbml_model)
    print('cellml_model (from SBML)')
    print('*'*80)
    # print first 10 lines
    for line in list(cellml_model.splitlines())[:10]:
        print(line)
    print('...')


.. parsed-literal::

    sbml_model
    ********************************************************************************
    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Created by libAntimony version v2.9.4 with libSBML version 5.15.0. -->
    <sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
      <model id="__main" name="__main">
        <listOfCompartments>
          <compartment sboTerm="SBO:0000410" id="default_compartment" spatialDimensions="3" size="1" constant="true"/>
        </listOfCompartments>
        <listOfSpecies>
          <species id="S1" compartment="default_compartment" initialConcentration="10" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
          <species id="S2" compartment="default_compartment" initialConcentration="0" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    ...
    cellml_model (from Antimony)
    ********************************************************************************
    <?xml version="1.0"?>
    <model xmlns:cellml="http://www.cellml.org/cellml/1.1#" xmlns="http://www.cellml.org/cellml/1.1#" name="__main">
    <component name="__main">
    <variable initial_value="10" name="S1" units="dimensionless"/>
    <variable initial_value="0" name="S2" units="dimensionless"/>
    <variable initial_value="0.1" name="k1" units="dimensionless"/>
    <variable name="_J0" units="dimensionless"/>
    <variable initial_value="0" name="S3" units="dimensionless"/>
    <variable initial_value="0.2" name="k2" units="dimensionless"/>
    <variable name="_J1" units="dimensionless"/>
    ...
    cellml_model (from SBML)
    ********************************************************************************
    <?xml version="1.0"?>
    <model xmlns:cellml="http://www.cellml.org/cellml/1.1#" xmlns="http://www.cellml.org/cellml/1.1#" name="__main">
    <component name="__main">
    <variable initial_value="10" name="S1" units="dimensionless"/>
    <variable initial_value="0" name="S2" units="dimensionless"/>
    <variable initial_value="0" name="S3" units="dimensionless"/>
    <variable initial_value="0.1" name="k1" units="dimensionless"/>
    <variable initial_value="0.2" name="k2" units="dimensionless"/>
    <variable name="_J0" units="dimensionless"/>
    <variable name="_J1" units="dimensionless"/>
    ...


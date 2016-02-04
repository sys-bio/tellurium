

Antimony, SBML, CellML
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

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
    
    # convert to CellML
    cellml_model = te.antimonyToCellML(ant_model)
    
    # or from the sbml
    cellml_model = te.sbmlToCellML(sbml_model)


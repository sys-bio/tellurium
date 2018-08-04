

SBML
^^^^

Given a
`RoadRunner <http://sys-bio.github.io/roadrunner/python_docs/index.html>`__
instance, you can get an SBML representation of the current state of the
model using ``getCurrentSBML``. You can also get the initial SBML from
when the model was loaded using ``getSBML``. Finally, ``exportToSBML``
can be used to export the current model state to a file.

.. code-block:: python

    import tellurium as te
    te.setDefaultPlottingEngine('matplotlib')
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
    <!-- Created by libAntimony version v2.9.4 with libSBML version 5.15.0. -->
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

Similar to the SBML functions above, you can also use the functions
``getCurrentAntimony`` and ``exportToAntimony`` to get or export the
current Antimony representation.

.. code-block:: python

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

    // Created by libAntimony v2.9.4
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

Tellurium also has functions for exporting the current model state to
CellML. These functionalities rely on using Antimony to perform the
conversion.

.. code-block:: python

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

To export the current model state to MATLAB, use ``getCurrentMatlab``.

.. code-block:: python

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

    %  How to use:
    %
    %  __main takes 3 inputs and returns 3 outputs.
    %
    %  [t x rInfo] = __main(tspan,solver,options)
    %  INPUTS: 
    %  tspan - the time vector for the simulation. It can contain every time point, 
    %  or just the start and end (e.g. [0 1 2 3] or [0 100]).
    %  solver - the function handle for the odeN solver you wish to use (e.g. @ode23s).
    %  options - this is the options structure returned from the MATLAB odeset
    %  function used for setting tolerances and other parameters for the solver.
    %  
    %  OUTPUTS: 
    %  t - the time vector that corresponds with the solution. If tspan only contains
    %  the start and end times, t will contain points spaced out by the solver.
    %  x - the simulation results.
    %  rInfo - a structure containing information about the model. The fields
    %  within rInfo are: 
    %     stoich - the stoichiometry matrix of the model 
    %     floatingSpecies - a cell array containing floating species name, initial
    %     value, and indicator of the units being inconcentration or amount
    %     compartments - a cell array containing compartment names and volumes
    %     params - a cell array containing parameter names and values
    %     boundarySpecies - a cell array containing boundary species name, initial
    %     value, and indicator of the units being inconcentration or amount
    %     rateRules - a cell array containing the names of variables used in a rate rule
    %
    %  Sample function call:
    %     options = odeset('RelTol',1e-12,'AbsTol',1e-9);
    %     [t x rInfo] = __main(linspace(0,100,100),@ode23s,options);
    %
    function [t x rInfo] = __main(tspan,solver,options)
        % initial conditions
        [x rInfo] = model();
    
        % initial assignments
    
        % assignment rules
    
        % run simulation
        [t x] = feval(solver,@model,tspan,x,options);
    
        % assignment rules
    
    function [xdot rInfo] = model(time,x)
    %  x(1)        S1
    %  x(2)        S2
    
    % List of Compartments 
    vol__default_compartment = 1;		%default_compartment
    
    % Global Parameters 
    rInfo.g_p1 = 0.1;		% k1
    
    if (nargin == 0)
    
        % set initial conditions
       xdot(1) = 10*vol__default_compartment;		% S1 = S1 [Concentration]
       xdot(2) = 0*vol__default_compartment;		% S2 = S2 [Concentration]
    
       % reaction info structure
       rInfo.stoich = [
          -1
          1
       ];
    
       rInfo.floatingSpecies = {		% Each row: [Species Name, Initial Value, isAmount (1 for amount, 0 for concentration)]
          'S1' , 10, 0
          'S2' , 0, 0
       };
    
       rInfo.compartments = {		% Each row: [Compartment Name, Value]
          'default_compartment' , 1
       };
    
       rInfo.params = {		% Each row: [Parameter Name, Value]
          'k1' , 0.1
       };
    
       rInfo.boundarySpecies = {		% Each row: [Species Name, Initial Value, isAmount (1 for amount, 0 for concentration)]
       };
    
       rInfo.rateRules = { 		 % List of variables involved in a rate rule 
       };
    
    else
    
        % calculate rates of change
       R0 = rInfo.g_p1*(x(1));
    
       xdot = [
          - R0
          + R0
       ];
    end;
    
    
    %listOfSupportedFunctions
    function z = pow (x,y) 
        z = x^y; 
    
    
    function z = sqr (x) 
        z = x*x; 
    
    
    function z = piecewise(varargin) 
    		numArgs = nargin; 
    		result = 0; 
    		foundResult = 0; 
    		for k=1:2: numArgs-1 
    			if varargin{k+1} == 1 
    				result = varargin{k}; 
    				foundResult = 1; 
    				break; 
    			end 
    		end 
    		if foundResult == 0 
    			result = varargin{numArgs}; 
    		end 
    		z = result; 
    
    
    function z = gt(a,b) 
       if a > b 
       	  z = 1; 
       else 
          z = 0; 
       end 
    
    
    function z = lt(a,b) 
       if a < b 
       	  z = 1; 
       else 
          z = 0; 
       end 
    
    
    function z = geq(a,b) 
       if a >= b 
       	  z = 1; 
       else 
          z = 0; 
       end 
    
    
    function z = leq(a,b) 
       if a <= b 
       	  z = 1; 
       else 
          z = 0; 
       end 
    
    
    function z = neq(a,b) 
       if a ~= b 
       	  z = 1; 
       else 
          z = 0; 
       end 
    
    
    function z = and(varargin) 
    		result = 1;		 
    		for k=1:nargin 
    		   if varargin{k} ~= 1 
    		      result = 0; 
    		      break; 
    		   end 
    		end 
    		z = result; 
    
    
    function z = or(varargin) 
    		result = 0;		 
    		for k=1:nargin 
    		   if varargin{k} ~= 0 
    		      result = 1; 
    		      break; 
    		   end 
    		end 
    		z = result; 
    
    
    function z = xor(varargin) 
    		foundZero = 0; 
    		foundOne = 0; 
    		for k = 1:nargin 
    			if varargin{k} == 0 
    			   foundZero = 1; 
    			else 
    			   foundOne = 1; 
    			end 
    		end 
    		if foundZero && foundOne 
    			z = 1; 
    		else 
    		  z = 0; 
    		end 
    		 
    
    
    function z = not(a) 
       if a == 1 
       	  z = 0; 
       else 
          z = 1; 
       end 
    
    
    function z = root(a,b) 
    	z = a^(1/b); 
     
    


Using Antimony Directly
^^^^^^^^^^^^^^^^^^^^^^^

The above examples rely on Antimony as in intermediary between formats.
You can use this functionality directly using e.g.
``antimony.getCellMLString``. A comprehensive set of functions can be
found in the `Antimony API
documentation <http://antimony.sourceforge.net/antimony__api_8h.html>`__.

.. code-block:: python

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


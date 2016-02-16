

Version information
^^^^^^^^^^^^^^^^^^^

.. code:: python

    import tellurium as te
    
    # to get the tellurium version use
    print(te.getTelluriumVersion())
    
    # to print the full version info use
    print('-' * 80)
    te.printVersionInfo()
    print('-' * 80)


.. parsed-literal::

    1.3.0
    --------------------------------------------------------------------------------
    tellurium : 1.3.0
    roadrunner : 1.4.2; Compiler: gcc 4.8.4, C++ version: 199711; JIT Compiler: LLVM-3.4; Date: Feb 15 2016, 09:48:54; LibSBML Version: 5.12.0
    antimony : v2.8.0
    snbw_viewer : No information for sbnw viewer
    libsbml : 5.12.1
    libsedml : 401
    phrasedml : v0.5 beta
    --------------------------------------------------------------------------------


Repeat simulation without notification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # Load SBML file
    r = te.loada("""
    model test
        J0: X0 -> X1; k1*X0;
        X0 = 10; X1=0;
        k1 = 0.2
    end
    """)
    
    import matplotlib.pyplot as plt
    
    # Turn of notices so they don't clutter the output
    te.noticesOff()
    for i in xrange(0, 20):
        result = r.simulate (0, 10)
        r.reset()
        r.plot(result, loc=None, show=False, 
               linewidth=2.0, lineStyle='-', color='black', alpha=0.8)
        r.k1 = r.k1 + 0.2
    # Turn the notices back on
    te.noticesOn()



.. image:: _notebooks/core/tellurium_utility_files/tellurium_utility_4_0.png


File helpers for reading and writing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # create tmp file
    import tempfile
    ftmp = tempfile.NamedTemporaryFile(suffix=".xml")
    print(ftmp.name)
    # load model
    r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
    # save to file
    te.saveToFile(ftmp.name, r.getMatlab())
    
    # or easier via
    r.exportToMatlab(ftmp.name)
    
    # load file
    sbmlstr = te.readFromFile(ftmp.name)
    print(sbmlstr)


.. parsed-literal::

    /tmp/tmpKJPTzF.xml
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
     
    



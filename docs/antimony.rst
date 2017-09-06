==================
Antimony Reference
==================

Since the advent of SBML (the Systems Biology Markup Language) computer models of biological systems have been able to be transferred easily between different labs and different computer programs without loss of specificity. But SBML was not designed to be readable or writable by humans, only by computer programs, so other programs have sprung up to allow users to more easily create the models they need.

Many of these programs are GUI-based, and allow drag-and-drop editing of species and reactions, such as `CellDesigner <http://www.celldesigner.org/>`_. A few, like Jarnac, take a text-based approach, and allow the creation of models in a text editor. This has the advantage of being usable in an automated setting, such as generating models from a template metalanguage (`TemplateSB <https://github.com/BioModelTools/TemplateSB>`_ is such a metalanguage for Antimony) and readable by others without translation. Antimony (so named because the chemical symbol of the element is ‘Sb’) was designed as a successor to Jarnac’s model definition language, with some new features that mesh with newer elements of SBML, some new features we feel will be generally applicable, and some new features that are designed to aid the creation of genetic networks specifically. Antimony is available as a library and a Python package.

Antimony is the main method of building models in Tellurium. Its main features include:

* Easily define species, reactions, compartments, events, and other elements of a biological model.
* Package and re-use models as modules with defined or implied interfaces.
* Create ‘DNA strand’ elements, which can pass reaction rates to downstream elements, and inherit and modify reaction rates from upstream elements.

---------------------
Change Log
---------------------

In the 2.5 release of Antimony, translation of Antimony concepts to and from the Hierarchical Model Composition package was developed further to be much more robust, and a new test system was added to ensure that Antimony’s ‘flattening’ routine (which exports plain SBML) matches libSBML’s flattening routine.

In the 2.4 release of Antimony, use of the Hierarchical Model Composition package constructs in the SBML translation became standard, due to the package being fully accepted by the SBML community.

In the 2.2/2.3 release of Antimony, units, conversion factors, and deletions were added.

In the 2.1 version of Antimony, the ‘import‘ handling became much more robust, and it became additionally possible to export hierarchical models using the Hierarchical Model Composition package constructs for SBML level 3.

In the 2.0 version of Antimony, it became possible to export models as CellML. This requires the use of the CellML API, which is now available as an SDK. Hierarchical models are exported using CellML’s hierarchy, translated to accommodate their ‘black box’ requirements.

---------------------
Introduction: Basics
---------------------

Creating a model in Antimony is designed to be very straightforward and simple. Model elements are created and defined in text, with a simple syntax.

The most common way to use Antimony is to create a reaction network, where processes are defined wherein some elements are consumed and other elements are created. Using the language of SBML, the processes are called ‘reactions’ and the elements are called ‘species’, but any set of processes and elements may be modeled in this way. The syntax for defining a reaction in Antimony is to list the species being consumed, separated by a ‘+‘, followed by an arrow (‘->‘), followed by another list of species being created, followed by a semicolon. If this reaction has a defined mathematical rate at which this happens, that rate can be listed next:

.. code-block:: none
  S1 -> S2; k1*S1

The above model defines a reaction where ‘S1‘ is converted to ‘S2‘ at a rate of ‘k1*S1‘.

This model cannot be simulated, however, because a simulator would not know what the conditions are to start the simulation. These values can be set by using an equals sign:

.. code-block:: none
  S1 -> S2; k1*S1
  S1 = 10
  S2 = 0
  k1 = 0.1

The above, then, is a complete model that can be simulated by any software that understands SBML (to which Antimony models can be converted).

If you want to give your model a name, you can do that by wrapping it with the text: ``model [name] [reactions, etc.] end``:

.. code-block:: none
  # Simple UniUni reaction with first-order mass-action kinetics
  model example1
    S1 -> S2; k1*S1
    S1 = 10
    S2 = 0
    k1 = 0.1
  end

In subsequent examples in this tutorial, we’ll be using this syntax to name the examples, but for simple models, the name is optional. Later, when we discuss submodels, this will become more important.

There are many more complicated options in Antimony, but the above has enough power to define a wide variety of models, such as this oscillator:

.. code-block:: none
  model oscli
    #Reactions:
    J0:    -> S1;  J0_v0
    J1: S1 ->   ;  J1_k3*S1
    J2: S1 -> S2; (J2_k1*S1 - J2_k2*S2)*(1 + J2_c*S2^J2_q)
    J3: S2 ->   ;  J3_k2*S2

    # Species initializations:
    S1 = 0
    S2 = 1

    # Variable initializations:
    J0_v0 = 8
    J1_k3 = 0
    J2_k1 = 1
    J2_k2 = 0
    J2_c  = 1
    J2_q  = 3
    J3_k2 = 5
  end

Examples
========

Comments
--------

Single-line comments in Antimony can be created using the ``#`` or ``//`` symbols, and multi-line comments can be created by surrounding them with ``/* [comments] */``.

.. code-block:: none
  /* This is an example of a multi-line
      comment for this tutorial */
  model example2
    J0: S1 -> S2 + S3; k1*S1 #Mass-action kinetics
    S1 = 10  #The initial concentration of S1
    S2 = 0   #The initial concentration of S2
    S3 = 3   #The initial concentration of S3
    k1 = 0.1 #The value of the kinetic parameter from J0.
  end

The names of the reaction and the model are saved in SBML, but any comments are not.

Reactions
---------

Reactions can be created with multiple reactants and/or products, and the stoichiometries can be set by adding a number before the name of the species:

.. code-block:: none
  # Production of S1
      -> S1;                 k0
  # Conversion from S1 to S2
  S1 -> S2;                 k1*S1
  # S3 is the adduct of S1 and S2
  S1 + S2 -> S3;            k2*S1*S2
  # Dimerization of S1
  2 S1 -> S2;               k3*S1*S1
  # More complex stoichiometry
  S1 + 2 S2 -> 3 S3 + 5 S4; k4*S1*S2*S2

Rate Laws and Initializing Values
---------------------------------

Reactions can be defined with a wide variety of rate laws

.. code-block:: none
  model pathway()
    # Examples of different rate laws and initialization

    S1 -> S2; k1*S1
    S2 -> S3; k2*S2 - k3*S3
    S3 -> S4; Vm*S3/(Km + S3)
    S4 -> S5; Vm*S4^n/(Km + S4)^n

    S1 = 10
    S2 = 0
    S3 = 0
    S4 = 0
    S5 = 0
    k1 = 0.1
    k2 = 0.2
    Vm = 6.7
    Km = 1E-3
    n = 4
  end

Boundary Species
----------------

Boundary species are those species which are unaffected by the model. Usually this means they are fixed. There are two ways to declare boundary species.

1) Using a dollar sign to indicate that a particular species is fixed:

.. code-block:: none
  model pathway()
    # Example of using $ to fix species

    $S1 ->  S2; k1*S1
    S2 ->  S3; k2*S2
    S3 -> $S4; k3*S3
  end

2) Using the const keyword to declare species are fixed:

.. code-block:: none
  model pathway()
    # Examples of using the const keyword to fix species

    const S1, S4
    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3
  end

Compartments
------------

For multi-compartment models, or models where the compartment size changes over time, you can define the compartments in Antimony by using the ``compartment`` keyword, and designate species as being in particular compartments with the ``in`` keyword:

.. code-block:: none
  model pathway()
    # Examples of different compartments

    compartment cytoplasm = 1.5, mitochondria = 2.6
    const S1 in mitochondria
    var S2 in cytoplasm
    var S3 in cytoplasm
    const S4 in cytoplasm

    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3
  end

Assignments
-----------

You can also initialize elements with more complicated formulas than simple numbers:

.. code-block:: none
  model pathway()
    # Examples of different assignments

    A = 1.2
    k1 = 2.3 + A
    k2 = sin(0.5)
    k3 = k2/k1

    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3
  end

Assignments in Time
-------------------

If you want to define some elements as changing in time, you can either define the formula a variable equals at all points in time with a ``:=``, or you can define how a variable changes in time with X', in which case you’ll also need to define its initial starting value. The keyword ``time`` represents time.

.. code-block:: none
  model pathway()
    # Examples of assignments that change in time

    k1 := sin(time)  #  k1 will always equal the sine of time
    k2  = 0.2
    k2' = k1         #' k2 starts at 0.2, and changes according to the value
                     #   of k1: d(k2)/dt = k1

    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
  end

Events
------

Events are discontinuities in model simulations that change the definitions of one or more symbols at the moment when certain conditions apply. The condition is expressed as a boolean formula, and the definition changes are expressed as assignments, using the keyword ``at``:

.. code-block:: none
  at (x>5): y=3, x=r+2

In a model with this event, at any moment when x transitions from being less than or equal to 5 to being greater to five, y will be assigned the value of 3, and x will be assigned the value of r+2, using whatever value r has at that moment. The following model sees the conversion of S1 to S2 until a threshold is reached, at which point the cycle is reset.

.. code-block:: none
  model reset()

    S1 -> S2; k1*S1

    E1: at (S2>9): S2=0, S1=10

    S1 = 10
    S2 = 0
    k1 = 0.5
  end

For more advanced usage of events, see `Antimony’s reference documentation on events <events-ref>`_.

Function Definitions
--------------------

You may create user-defined functions in a similar fashion to the way you create modules, and then use these functions in Antimony equations. These functions must be basic single equations, and act in a similar manner to macro expansions. As an example, you might define the quadratic equation and use it in a later equation as follows:

.. code-block:: none
  function quadratic(x, a, b, c)
    a*x^2 + b*x + c
  end

  model quad1
    S3 := quadratic(s1, k1, k2, k3);
  end

This effectively defines S3 to always equal the equation ``k1*s1^2 + k2*s1 + k3``.

Modular Models
--------------

Antimony was actually originally designed to allow the modular creation of models, and has a basic syntax set up to do so. For a full discussion of Antimony modularity, see the full documentation, but at the most basic level, you define a re-usable module with the ‘model’ syntax, followed by parentheses where you define the elements you wish to expose, then import it by using the model’s name, and the local variables you want to connect to that module

.. code-block:: none
  # This creates a model 'side_reaction', exposing the variables 'S' and 'k1':
  model side_reaction(S, k1)
    J0: S + E -> SE; k1*k2*S*E - k2*ES;
    E = 3;
    SE = E+S;
    k2 = 0.4;
  end

  # In this model, 'side_reaction' is imported twice:
  model full_pathway
      -> S1; k1
    S1 -> S2; k2*S1
    S2 ->   ; k3*S2

    A: side_reaction(S1, k4)
    B: side_reaction(S2, k5)

    S1 = 0
    S2 = 0
    k1 = 0.3
    k2 = 2.3
    k3 = 3.5
    k4 = 0.0004
    k5 = 1

  end

In this model, ``A`` is a submodel that creates a side-reaction of ``S1`` with ``A.E`` and ``A.SE``, and ``B`` is a submodel that creates a side-reaction of ``S2`` with ``B.E`` and ``B.SE``. It is important to note that there is no connection between ``A.E`` and ``B.E`` (nor ``A.ES`` and ``B.ES``): they are completely different species in the model.

Importing Files
---------------

More than one file may be used to define a set of modules in Antimony through the use of the ‘import‘ keyword. At any point in the file outside of a module definition, use the word ‘import‘ followed by the name of the file in quotation marks, and Antimony will include the modules defined in that file as if they had been cut and pasted into your file at that point. SBML files may also be included in this way:

.. code-block:: none
  import "models1.txt"
  import "oscli.xml"

  model mod2()
    A: mod1();
    B: oscli();
  end

In this example, the file ``models1.txt`` is an Antimony file that defines the module ``mod1``, and the file ``oscli.xml`` is an SBML file that defines a model named ``oscli``. The Antimony module ``mod2`` may then use modules from either or both of the other imported files.

Units
-----

While units do not affect the mathematics of SBML or Antimony models, you can define them in Antimony for annotation purposes by using the ``unit`` keyword:

.. code-block:: none
  unit substance = 1e-6 mole;
  unit hour = 3600 seconds;

Adding an ‘s’ to the end of a unit name to make it plural is fine when defining a unit: ‘3600 second‘ is the same as ‘3600 seconds‘. Compound units may be created by using formulas with ‘*‘, ‘/‘, and ‘^‘. However, you must use base units when doing so (‘base units’ defined as those listed in Table 2 of the SBML Level 3 Version 1 specification, which mostly are SI and SI-derived units).

.. code-block:: none
  unit micromole = 10e-6 mole / liter;
  unit daily_feeding = 1 item / 86400 seconds
  unit voltage = 1000 grams * meters^2 / seconds^-3 * ampere^-1

You may use units when defining formulas using the same syntax as above: any number may be given a unit by writing the name of the unit after the number. When defining a symbol (of any numerical type: species, parameter, compartment, etc.), you can either use the same technique to give it an initial value and a unit, or you may just define its units by using the ‘has’ keyword:

.. code-block:: none
  unit foo = 100 mole/5 liter;
  x = 40 foo/3 seconds; # '40' now has units of 'foo' and '3' units of 'seconds'.
  y = 3.3 foo;          # 'y' is given units of 'foo' and an initial
                        #   value of '3.3'.
  z has foo;            # 'z' is given units of 'foo'.
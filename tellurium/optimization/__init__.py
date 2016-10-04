# coding=utf-8
"""
Tellurium optimization functions.

The modules in tellurium.optimization implement functions for the fitting of model
parameters to experimental data.

The fitting routines require
- model
    (SBML, Antimony)
- list of parameters to fit (with lower and upper bounds) + initial value (from model)
    {k1: [0.1, 1.0],
     k2: [0.1, 5.0]}
- list of experimental values for given time and selection
    time, selection, value
    0.0, S1, 10.0
    5.0, S1, 5.0
    10.0, S1, 2.0
    0.0, S2, 0.0
    5.0, S2, 5.0
    10.0, S2, 10.0
- minimization function
    This is build from the model, parameters, list of experimental data.
    Within the minimization function one (multiple) simulations are performed for
    the given parameter set and some distance measure calculated between simulation
    results and experimental data.


Algorithms which will be implemented in future versions are

Differential Evolution (SciPy)
    scipy.optimize.differential_evolution
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html#scipy.optimize.differential_evolution

    Finds the global minimum of a multivariate function. Differential Evolution is stochastic in nature
    (does not use gradient methods) to find the minimium, and can search large areas of candidate space,
    but often requires larger numbers of function evaluations than conventional gradient based techniques.
    The algorithm is due to Storn and Price [R140].

Grid Search (Scikit-Learn) | brute (SciPy)
    scipy.optimize.brute
    Minimize a function over a given range by brute force.
    Uses the “brute force” method, i.e. computes the function’s value at each point of a
    multidimensional grid of points, to find the global minimum of the function.

    scikit-learn.org/stable/modules/grid_search.html
    from sklearn.grid_search import GridSearchCV
    Parameters that are not directly learnt within estimators can be set by searching a parameter space for the
    best Cross-validation: evaluating estimator performance score. Typical examples include C, kernel and gamma for
    Support Vector Classifier, alpha for Lasso, etc.

Basin-hopping
    scipy.optimize.basinhopping
    Find the global minimum of a function using the basin-hopping algorithm

Levenberg-Marquardt

Particle Swarm

Simulated Annealing
"""


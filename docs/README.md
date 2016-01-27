# tellurium API documentation

The API documentation of tellurium is build from the python source code and restructured Text (reST) `*.rst` files located in `tellurium/docs`. The documentation is based on sphinx and uses the information encoded in the docstrings. The documentation is available at

**http://tellurium.readthedocs.org/en/latest/**

## Documentation guidlines
Documentation can be updated by changing `*.rst` files in `tellurium/docs`. Just edit the latest files in the git repository. Easy access is provided via the **Edit on GitHub** links in the documentation.

Do **NOT** edit the `*.rst` files in 
* `tellurium/docs/_apidoc`
* `tellurium/docs/_notebooks`
These are generated automatically from the python source code and the python notebooks. Changes to the API documentation or notebook examples have to be done in the respective python code (`tellurium/tellurium`) and notebook files (`tellurium/examples/notebooks`).

## Adding code examples to documentation
Examples are added via notebooks via the following workflow
* copy the notebook template `tellurium/examples/notebooks/core/template.ipynb` to a new file `tellurium/examples/notebooks/core/newExample.ipynb`
* add your python code in the notebook `newExample.ipynb`
* run the notebook to make sure everything works
* add the notebook to the notebook index `tellurium/examples/notebooks/index.ipynb`
* register the notebook in the docs in `tellurium/docs/notebooks.rst` via `.. include:: _notebooks/core/newExample.rst
After the next complete rebuild the example is available in the docs. 

All examples added via notebooks are run when building the docs, so problems with the examples are directly visible and can be fixed.

## Documentation of python source code
Modules, classes, functions and methods can be documented via their respective docstrings in sphinx format (for information see http://www.sphinx-doc.org/en/stable/). An example of the sphinx syntax is provided below:

```{python}
def function(arg1, arg2):
    """Short sentence describing the funtion. 
    Here comes a long explanation which describes in detail the function.
    see also: `:func:loadAntimonyModel`
    ::

        r = loada('S1 -> S2; k1*S1; k1 = 0.1; S2 = 10')

    :param arg1: parameter is ..
    :param arg2: This parameter is ...
    :returns: describe return object
    """
    return doSomesting(arg1, arg2)
```
Important points are:
* write one short sentence describing the function at begin of docstring.
* provide description of arguments via `:param arg1:`
* provide description of return type via `:returns:`
* code examples are written via `::` followed by empty line and **intended** code block

There are many more options available, see the sphinx documentation for more details.

## Build Documentation 
The python requirements for building the documentation are
```
pip install sphinx sphinx-autobuild sphinx_rtd_theme mock
```

### minimal build
After changes to the `*.rst` files the updated documentation can be build and viewed locally via
```
make html && firefox _build/html/index.html
```
The minimal build just rebuilds the html from the changes in the rst. As soon as the changes are commited to the master branch the online documentation on  
http://tellurium.readthedocs.org/en/latest/
will be updated via a commit hook. The update can take a few minutes.

The minimal build does not update 
* `tellurium/docs/_apidoc`
* `tellurium/docs/_notebooks`

### complete build
To build the complete API documentation use the build script `make_docs.sh` in the `tellurium/docs` folder, which mainly does

* removes old `_apidoc` and `_notebook` files
* creates the `_apidoc` `*.rst` from python source via `sphinx-apidoc`
* creates the `_notebook` `*.rst` from notebook files in `tellurium/examples/notebooks` (the notebooks are executed, so all the example code in the documentation is run with the latest source)
* creates the `*.py` code from notebook files in `tellurium/examples/notebook-py` (examples which can be loaded in Tellurium)
* creates the `html` documentation (analoque to minimal build)

## Open Issues
* links between functions in documentation (i.e. hyperlinks between functions for easy navigation in API)

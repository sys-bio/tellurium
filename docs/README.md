# tellurium API documentation

The API documentation of tellurium is build from the python source code and the `*.rst` files located in `tellurium/docs`. The documentation is based on sphinx and uses the information encoded in the docstrings. This replaces the old API documentation based on doxygen.

## Build Documentation 
The python requirements for building the documentation are
```
pip install sphinx sphinx-autobuild sphinx_rtd_theme mock
```
To build the API documentation use the build script `make_docs.sh` in the `tellurium/docs` folder, which mainly does
```{shell}
# remove old documentation
rm -rf _apidoc
rm -rf _built

# create auto documentation for tellurium packages
sphinx-apidoc -o _apidoc ../tellurium

# create html documentation
make html

# view documentation in docs/_built
firefox _build/html/index.html
```

## HowTo document python code in tellurium
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

## Open Issues
* commit hook for automatic generation (documentation should be created automatically on commits
* links between functions in documentation (i.e. hyperlinks between functions for easy navigation in API)
* python format of all source examples (if source examples provided make sure that they have python syntax highlighting)

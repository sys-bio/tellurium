# Documentation of tellurium code

The documentation for tellurium is build with sphinx from the python source code and the `*.rst` files in `tellurium/docs`.
The python requirements for building the documentation are
```
pip install sphinx sphinx-autobuild sphinx_rtd_theme
```
This replaces the documentation via doxygen.

## Documentation of python objects
Modules, classes, functions and methods are documented via their respective docstrings in sphinx format with information available at http://www.sphinx-doc.org/en/stable/

An example of the sphinx syntax is provided below:
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

## Create Documentation 
At the moment the documentation can be created via the script `make_docs.sh` in the docs folder
```
# remove old documentation
rm -rf _apidoc
rm -rf _built

# create auto documentation for tellurium package.
sphinx-apidoc -o _apidoc ../tellurium

# create html documentation
make html

# view new documentation in docs/_built
firefox _build/html/index.html
```
The documentation should be created automatically before commits (currently not implemented).

## Open Issues
* Auto reload & commit hook for automatic generation
* links between functions in documentation
* python formating for all source examples

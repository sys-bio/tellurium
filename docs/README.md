# Documentation of tellurium

Documentation is build with sphinx and read the docs schema.
The requirements are
```
pip install sphinx sphinx-autobuild sphinx_rtd_theme
```

# Create Documentation 
To create the documentation after changes to the docstrings use either
```
cd tellurium/docs
make html
```

or sphinx-autobild which monitors when files change and automatically updates
the documentation.
```
sphinx-autobuild docs docs/_build/html
```

# Open Issues
TODO: Auto reload

TODO: code examples in docstring
```
sphinx-apidoc -o _apidoc ../tellurium
```

TODO: Full API documentation
TODO: links to other function documentation


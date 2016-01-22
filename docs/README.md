# Documentation of tellurium

Documentation is build with sphinx and read the docs schema.
The requirements are
```
pip install sphinx sphinx-autobuild sphinx_rtd_theme
```

# Create Documentation 
To create the documentation
```
cd tellurium/docs
make html
```

TODO: Auto reload
TODO: sections
TODO: Full API documentation
```
make _apidoc _build html

sphinx-apidoc -o _apidoc ../tellurium
```


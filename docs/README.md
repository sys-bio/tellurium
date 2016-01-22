# Documentation of tellurium

Documentation is build with sphinx and readthedocs schema.
The necessary requirements to build the documentation are
```
pip install sphinx sphinx-autobuild sphinx_rtd_theme
```
All python objects are documented via docstrings in sphinx format
http://www.sphinx-doc.org/en/stable/


# Create Documentation 
The documentation should be created automatically before commits.
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

# Open Issues
* Auto reload & commit hook for automatic generation
* links between functions in documentation
* python formating for all source examples


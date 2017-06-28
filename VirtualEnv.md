# How to setup the VirtualEnvironment for development on linux?

Install the requirements available via pip
```
mkvirtualenv tellurium
(tellurium) 
pip install -r requirements.txt
```

Install the remaining requirements via the wheelhouse:
```
git clone https://github.com/sys-bio/wheelhouse.git te-wheelhouse
cd te-wheelhouse
workon tellurium
```

**py36**
```
pip install antimony-2.9.3-cp36-cp36m-manylinux1_x86_64.whl
pip install phrasedml-1.0.4-cp36-cp36m-manylinux1_x86_64.whl
pip install sbml2matlab-0.9.1-cp36-cp36m-manylinux1_x86_64.whl
pip install tecombine-0.2.0-cp36-cp36m-manylinux1_x86_64.whl
```

**py27**
```
pip install antimony-2.9.1-cp36-cp36m-manylinux1_x86_64.whl
pip install phrasedml-1.0.4-cp36-cp36m-manylinux1_x86_64.whl
pip install sbml2matlab-0.9.1-cp36-cp36m-manylinux1_x86_64.whl
pip install tecombine-0.2.0-cp36-cp36m-manylinux1_x86_64.whl
```

Install tellurium in the virtualenv
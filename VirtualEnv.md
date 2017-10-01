# python virtual environment
## How to setup the VirtualEnvironment for development on linux?

Install stable version from pip
```
mkvirtualenv tellurium
(tellurium) pip install tellurium
```

Install latest development version, or feature branch
```
# clone repository
git clone https://github.com/sys-bio/tellurium
cd tellurium

# make virtual environment
mkvirtualenv tellurium
(tellurium) pip install -r requirements.txt

# checkout branch 
(tellurium) git checkout master

# install tellurium
(tellurium) pip install -e .
```

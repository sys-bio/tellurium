# python virtual environment
## How to setup the VirtualEnvironment for development on linux?

Install the requirements available via pip
```
git clone https://github.com/sys-bio/tellurium
cd tellurium
mkvirtualenv tellurium
(tellurium) pip install -r requirements.txt
```

Install tellurium in the virtualenv
```
(tellurium) pip install -e .
```
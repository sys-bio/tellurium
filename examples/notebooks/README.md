# Ipython Notebooks
Example notebooks for tellurium. The examples require the Jupyter notebook server 
(http://jupyter.readthedocs.org/en/latest/install.html).

To get the examples clone the repository via
```
git clone https://github.com/sys-bio/tellurium.git
```

To run the notebooks first create a virtual environment with tellurium and jupyter notebook.
```
# create virtualenv
mkvirtualenv te
(te) pip install tellurium
(te) pip install jupyter notebook

# register the kernel
(te) ipython kernel install --user --name=te
```

Change in the notebook folder in the console and run jupyter
```
(te) cd tellurium/examples/notebooks
(te) jupyter notebook index.ipynb
```

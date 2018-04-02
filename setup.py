# -*- coding: utf-8 -*-
###################################
# tellurium setup script
#
# develop install via
# pip install -e .
###################################

from setuptools import setup
import os
try:
    with open(os.path.join(os.path.dirname(__file__), 'VERSION.txt'), 'r') as f:
        version = f.read().rstrip()
except IOError:
    # fallback location
    with open(os.path.join(os.path.dirname(__file__), 'tellurium/VERSION.txt'), 'r') as f:
        version = f.read().rstrip()

setup(name='tellurium',
      version=version,
      author='J. Kyle Medley, Kiri Choi, Matthias König, Lucian Smith, Herbert M. Sauro',
      description='Tellurium: An biological modeling environment for Python',
      url='http://tellurium.analogmachine.org/',
      packages=[
          'tellurium',
          'tellurium.analysis',
          'tellurium.notebooks',
          'tellurium.plotting',
          'tellurium.roadrunner',
          'tellurium.sedml',
          'tellurium.teconverters',
          'tellurium.teio',
          'tellurium.utils',
        #   'tellurium.optimization',
          'tellurium.visualization',
        #   'tellurium.tests',
      ],
      package_data={
          "tellurium": ["*.txt"],
          "tellurium.sedml": ["templates/*.template"],
      },
      install_requires=[
          # general
          'numpy>=1.11.0',  # 0.13.1
          'scipy>=0.19.0',  # 0.19.1
          'matplotlib>=2.0.2',
          'pandas>=0.20.2',
          # SBW-derived
          'libroadrunner>=1.4.24',
          'phrasedml>=1.0.9',
          'antimony>=2.9.3',
          'rrplugins>=1.1.8',
          'sbml2matlab>=0.9.1',
          # standards
          'tesbml>=5.15.0.1',
          'tenuml>=1.1.1',
          'tesedml>=0.4.3',
          'tecombine>=0.2.2',
          # misc
          'appdirs>=1.4.3',
          'jinja2>=2.9.6',
          'plotly>=2.0.12',
          'requests',
          # Jupyter / IPython
          'jupyter-client>=5.1.0',
          'jupyter-core>=4.3.0',
          'ipython',
          'ipykernel>=4.6.1',
          # testing
          'pytest',
          ]
      )

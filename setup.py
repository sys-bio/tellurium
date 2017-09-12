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
        #   'tellurium.optimization',
        #   'tellurium.visualization',
        #   'tellurium.tests',
      ],
      package_data={
          "tellurium": ["*.txt"],
          "tellurium.sedml": ["templates/*.template"],
      },
      install_requires=[
          'numpy>=1.13.1',
          'scipy>=0.19.1',
          'matplotlib>=2.0.2',
          'pandas>=0.20.3',

          'libroadrunner>=1.4.18',
          'python-libsbml>=5.15.0',
          'python-libsedml>=0.4.1',
          'python-libnuml>=1.0.1',
          'python-libcombine>=0.2.1',
          'phrasedml>=1.0.6',
          'antimony>=2.9.3',
          'rrplugins>=1.1.8',
          'sbml2matlab>=0.9.1',

          'appdirs>=1.4.3',
          'ipywidgets',
          'bioservices',
          'ipython',
          'jinja2',
          'plotly',
          'pytest',
          ]
      )

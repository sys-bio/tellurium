# -*- coding: utf-8 -*-
###################################
# tellurium setup script
#
# develop install via
# pip install -e .
###################################
from setuptools import setup  # allows 'python setup.py develop'
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
          'numpy',
          'matplotlib>=2.0.0',
          'pandas>=0.19.2',

          'libroadrunner>=1.4.18',
          'python-libsbml>=5.15.0',
          'python-libsedml>=0.4.1',
          'python-libnuml',
          'phrasedml>=1.0.6',
          'antimony>=2.9.3',
          'tecombine>=0.2.1',
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

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
          'libroadrunner>=1.4.16',
          # 'antimony>=2.9.1',
          # 'phrasedml>=1.0.5',
          # 'tesbml>=5.15.0',
          # 'tesedml>=0.4.2',
          # 'tecombine>=0.2.0',
          'pandas>=0.19.2',
          'matplotlib>=2.0.0',
          'appdirs>=1.4.3',
          ]
      )

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
          'tellurium.teio',
          'tellurium.sedml',
          'tellurium.notebooks',
          'tellurium.optimization',
          'tellurium.visualization',
          'tellurium.sedml',
          'tellurium.tests',
      ],
      package_data={
          "tellurium": ["*.txt"],
          "tellurium.sedml": ["templates/*.template"],
      },
      install_requires=['pandas>=0.19.2', 'matplotlib>=2.0.0', 'appdirs>=1.4.3']
      )

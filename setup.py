from distutils.core import setup

import os
with open(os.path.join(os.path.dirname(__file__), 'VERSION.txt'), 'r') as f:
    version = f.read().rstrip()

setup(name='tellurium',
      version=version,
      description='Tellurium',
      url='https://github.com/sys-bio/tellurium',
      packages=[
          'tellurium',
          'tellurium.analysis',
          'tellurium.Export',
          'tellurium.notebooktools',
          'tellurium.ParameterScan',
          'tellurium.widgets',
          'tellurium.optimization',
          'tellurium.visualization'
      ]
      )

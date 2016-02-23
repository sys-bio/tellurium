{% import 'macros_helpers.py' as helpers %}
"""
    tellurium {{ version }}

    auto-generated code ({{ timestamp }})
        sedmlDoc: L{{ doc.getLevel() }}V{{ doc.getVersion() }} {{ factory.sedmlDoc }}
        workingDir: {{ factory.workingDir }}
        inputType: {{ factory.inputType }}

"""
from __future__ import print_function, division
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import libsedml
import os.path

{{ helpers.heading(doc.getListOfModels(), 'Model') }}
{% for m in doc.getListOfModels() %}
# load model
{% if m|SEDML_isSBMLModel %}
{{ m.getId() }} = te.loadSBMLModel(os.path.join('{{ factory.workingDir }}', '{{ m.getSource() }}'))
{% endif %}
{% endfor %}


{{ helpers.heading(doc.getListOfSimulations(), 'Simulation') }}

{{ helpers.heading(doc.getListOfTasks(), 'Task') }}
{% for s in doc.getListOfModels() %}
# UniformTimeCourse

# SteadyState
print('{{ s.getId() }}', '{{ s.getName() }}')
{% if s.getTypeCode() == libsedml.SEDML_SIMULATION_ONESTEP %}
print('OneStep')
{% endif %}

{% endfor %}

{{ helpers.heading(doc.getListOfDataGenerators(), 'DataGenerator') }}

{{ helpers.heading(doc.getListOfOutputs(), 'Output') }}

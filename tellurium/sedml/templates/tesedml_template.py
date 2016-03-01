{% import 'macros_helpers.py' as helpers %}
"""
    tellurium {{ version }}

    auto-generated code ({{ timestamp }})
    sedmlDoc: L{{ doc.getLevel() }}V{{ doc.getVersion() }} {% if doc.isSetId() %}id={{ doc.getId() }} {% endif %} {% if doc.isSetName() %}name={{ doc.getName() }}{% endif %}

    workingDir: {{ factory.workingDir }}
    inputType: {{ factory.inputType }}
"""
from __future__ import print_function, division
import tellurium as te
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import libsedml
import libsbml
import pandas
import os.path

workingDir = '{{ factory.workingDir }}'

{{ helpers.heading(doc.getListOfModels(), 'Model') }}
{% for model in doc.getListOfModels() %}
# Model <{{ model.getId() }}>
{{ modelToPython(model) }}
{% endfor %}

{{ helpers.heading(doc.getListOfTasks(), 'Task') }}
{% for task in doc.getListOfTasks() %}
# Task <{{ task.getId() }}>
{{ taskToPython(factory.doc, task) }}

{% endfor %}
{{ helpers.heading(doc.getListOfDataGenerators(), 'DataGenerator') }}
{% for dg in doc.getListOfDataGenerators() %}
# DataGenerator <{{ dg.getId() }}>
{{ dataGeneratorToPython(factory.doc, dg) }}

{% endfor %}
{{ helpers.heading(doc.getListOfOutputs(), 'Output') }}
{% for out in doc.getListOfOutputs() %}
# Output <{{ out.getId() }}>
{{ outputToPython(factory.doc, out) }}

{% endfor %}
{# -------------------------------------
 #  Create Heading for the listOf
 #  -------------------------------------#}

{% macro heading(list, name) %}
{% if list|length > 0 %}
# --------------------------------------------------------
# {{ name }}s
# --------------------------------------------------------{#
{% for item in list %}
#  - {{ item.getId() }} {% if item.isSetName() %}({{ item.getName() }}){% endif %}
{% endfor %}#}
{% endif %}
{% endmacro %}


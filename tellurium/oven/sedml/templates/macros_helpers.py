{# -------------------------------------
 #  Create Heading for the listOf
 #  -------------------------------------#}

{% macro heading(list, name) %}
{% if list|length > 0 %}
print('-'*80)
print('*** {{ name }}s ***')
print('-'*80)
{% for item in list %}
print('{{ name }}: {{ item.getId() }}({{ item.getName() }})')
{% endfor %}
{% endif %}
{% endmacro %}


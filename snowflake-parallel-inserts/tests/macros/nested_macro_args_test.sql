{% macro nested_macro_args() %}

  {% set flow_name = kwargs['endtoend_dct']['flow_name'] %}
  {% do log(flow_name, info=True) %}
  {{ return(flow_name) }}

{% endmacro %}
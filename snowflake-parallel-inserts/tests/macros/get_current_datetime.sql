{% macro get_current_datetime() %}
  
  {% set sql = 'SELECT current_date' %}

  {% set results = run_query(sql) %}

  {{return(results)}}

{% endmacro %}
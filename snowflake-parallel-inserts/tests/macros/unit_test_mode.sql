{% macro unit_test_mode() %}
  
  {% if var is not defined %}
    {{ return(False) }}

  {% elif var('run_unit_tests') == 'true' %}
     {{ return(True) }}
    
  {% elif target.name == 'unit-test' %}
    {{ return(True) }}

  {% else %}
    {{ return(False) }}

  {% endif %}

{% endmacro %}
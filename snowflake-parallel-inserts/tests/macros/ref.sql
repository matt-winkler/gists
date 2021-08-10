{% macro ref(model_name) %}
  
  {# -- check if we are running in unit test mode #}
  {% if unit_test_mode() %}
    
    {% set test_model_name_lookup = model_name + '_unit_test_source' %}
    {% set test_model_name = var(test_model_name_lookup, model_name) %}

    {{ return(test_model_name)}}
    
  {% else %}
    {{ return(builtins.ref(model_name)) }}

  {% endif %}

{% endmacro %}
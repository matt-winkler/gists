{% macro parallel_insert_setup() %}

   {% set sql = 'drop table if exists analytics.dbt_mwinkler.parallel_insert_target' %}
   {% do run_query(sql) %}
   
   {% set sql = 'create table analytics.dbt_mwinkler.parallel_insert_target (order_key int, order_date date)' %}
   {% do run_query(sql) %}

{% endmacro %}
{% macro insert_into(target_table, sql) %}
  
     insert into {{ target.database }}.{{ target.schema }}.{{ target_table }} 
      ( {{ sql }} );

      commit;

{% endmacro %}
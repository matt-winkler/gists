{% materialization parallel_insert, adapter='snowflake' %}
  
  {% set original_query_tag = set_query_tag() %}
  {% set target_table = config.get('target_table') %}
  {% set warehouse = config.get('warehouse') %}

  {%- set target_relation = api.Relation.create(
        identifier=target_table, schema=target.schema, database=target.database,
        type='table') -%}

  {{ run_hooks(pre_hooks) }}

  {% set warehouse_sql = use_warehouse(warehouse) %}
  {% do log(warehouse_sql, info=true) %}

  {% set insert_sql = insert_into(target_table, sql) %}
  {% do log(insert_sql, info=true) %}

  {% set build_sql = warehouse_sql ~ ' ' ~ insert_sql %}
  
  {%- call statement('main') -%}
    {{ build_sql }}
  {%- endcall -%}

  {{ run_hooks(post_hooks) }}

  {% set target_relation = target_relation.incorporate(type='table') %}
  {% do persist_docs(target_relation, model) %}

  {% do unset_query_tag(original_query_tag) %}

  {{ return({'relations': [target_relation]}) }}

{% endmaterialization %}
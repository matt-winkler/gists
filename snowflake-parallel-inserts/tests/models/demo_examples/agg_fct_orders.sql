-- to unit test this: 
-- pre-requisite: dbt seed
-- first run: dbt run -m +agg_fct_orders --vars '{"run_unit_tests": "true"}'
-- then: dbt test -m mock_target__fct_orders

with source_data as (select * from {{ ref('fct_orders') }} ),

final as (
    select order_key,
           sum(gross_item_sales_amount) as gross_item_sales_amount,
           sum(item_discount_amount) as item_discount_amount,
           -- sum(net_item_sales_amount) as net_item_sales_amount,
           count(net_item_sales_amount) as net_item_sales_amount
    from   source_data
    group by 1
)

select * from final
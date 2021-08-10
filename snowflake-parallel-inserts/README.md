Welcome to the dbt Labs demo dbt project! We use the [TPCH dataset](https://docs.snowflake.com/en/user-guide/sample-data-tpch.html) to create a sample project to emulate what a production project might look like!

                        _              __                   
       ____ ___  ____ _(_)___     ____/ /__  ____ ___  ____ 
      / __ `__ \/ __ `/ / __ \   / __  / _ \/ __ `__ \/ __ \
     / / / / / / /_/ / / / / /  / /_/ /  __/ / / / / / /_/ /
    /_/ /_/ /_/\__,_/_/_/ /_/   \__,_/\___/_/ /_/ /_/\____/ 

## Special demos

- **dbt-external-tables:** Manage database objects that read data external to the warehouse within dbt. See `models/demo_examples/external_sources.yml`.
- **Lifecycle Notifications:** See examples of dbt Cloud Job Lifecycle Notifications [here](https://gist.github.com/boxysean/3166b3ac55801685b6d275e9a9ddd5ee).
- **Pivot tables:** One example of creating a pivot table using Snowflake syntax, another example using Jinja. See `models/aggregates/agg_yearly_*.sql`.
- **Unit Testing:** Examples of uploading test fixtures and running them against the models in your project.  
* Files used in unit testing setup:  
- `models/demo_examples/agg_fct_orders.sql`: A model .sql file you want to unit test  
- `models/demo_examples/unit_test_config.yml`: Defines the tests to compare the `agg_fct_orders` model with the test fixture output in `data/mock_target__fct_orders.csv`  
- `macros/ref.sql`: Overrides the default ref() implementation to handle unit test runs  
- `macros/unit_test_mode.sql`: Based on variables passed at run time, determines if unit test mode is active  
- `data/mock_source__fct_orders.csv`: Sample static input dataset for the fct_orders model  
- `data/mock_target__fct_orders.csv`: Sample static output dataset for fct_orders model  

* To simulate a unit testing run, follow these steps:  
1) To run the `agg_fct_orders` model without unit testing: `dbt run -m +agg_fct_orders`  
2) Run `dbt seed` to stage the test fixtures in the `data` folder in the database   
3) Run `dbt run -m +agg_fct_orders --vars '{"run_unit_tests": "true"}'` to trigger the run of `agg_fct_orders` with unit test logic   
4) Run `dbt test -m mock_target__fct_orders`  
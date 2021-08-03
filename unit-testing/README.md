## Unit Testing with dbt

An examples of uploading test fixtures and running them against the models in your project.  

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
select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      





with validation_errors as (

    select
        invoice_number, product_code
    from "airbyte"."analytics"."fct_sales"
    group by invoice_number, product_code
    having count(*) > 1

)

select *
from validation_errors



      
    ) dbt_internal_test
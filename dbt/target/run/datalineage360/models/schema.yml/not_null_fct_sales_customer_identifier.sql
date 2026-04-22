select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select customer_identifier
from "airbyte"."analytics"."fct_sales"
where customer_identifier is null



      
    ) dbt_internal_test
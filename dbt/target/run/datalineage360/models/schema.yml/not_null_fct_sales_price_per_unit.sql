select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select price_per_unit
from "airbyte"."analytics"."fct_sales"
where price_per_unit is null



      
    ) dbt_internal_test
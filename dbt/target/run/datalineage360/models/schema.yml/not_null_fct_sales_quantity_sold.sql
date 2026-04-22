select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select quantity_sold
from "airbyte"."analytics"."fct_sales"
where quantity_sold is null



      
    ) dbt_internal_test
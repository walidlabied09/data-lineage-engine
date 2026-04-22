select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select invoice_date
from "airbyte"."analytics"."fct_sales"
where invoice_date is null



      
    ) dbt_internal_test
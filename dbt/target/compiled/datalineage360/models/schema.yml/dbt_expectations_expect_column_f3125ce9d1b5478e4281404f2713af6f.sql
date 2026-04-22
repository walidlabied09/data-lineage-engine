






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and price_per_unit >= 0.01
)
 as expression


    from "airbyte"."analytics"."fct_sales"
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors








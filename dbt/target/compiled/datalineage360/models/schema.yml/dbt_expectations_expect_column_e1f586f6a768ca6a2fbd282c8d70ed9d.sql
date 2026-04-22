






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and quantity_sold >= 1
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








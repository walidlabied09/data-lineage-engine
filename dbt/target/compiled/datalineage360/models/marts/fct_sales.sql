

select
    -- Clés et identifiants
    invoice_no            as invoice_number,
    stock_code            as product_code,
    customer_id           as customer_identifier,

    -- Infos géographiques
    country               as customer_country,

    -- Détails temporels
    invoice_ts::timestamp as invoice_timestamp,
    invoice_ts::date      as invoice_date,
    extract(year  from invoice_ts) as invoice_year,
    extract(month from invoice_ts) as invoice_month,
    extract(day   from invoice_ts) as invoice_day,

    -- Quantités et prix
    quantity              as quantity_sold,
    unit_price            as price_per_unit,

    -- Calculs financiers
    (quantity * unit_price)::numeric(12,2) as gross_amount,
    case when country = 'United Kingdom'
         then (quantity * unit_price * 0.10)
         else 0 end                         as discount_amount,
    ((quantity * unit_price) -
     case when country = 'United Kingdom'
          then (quantity * unit_price * 0.10)
          else 0 end)::numeric(12,2)        as net_sales_amount,
    ((unit_price - (unit_price * 0.70)) * quantity)::numeric(12,2) as gross_margin,

    -- Montant ligne issu du staging
    line_amount           as line_total

from "airbyte"."analytics"."stg_sales_data"
where quantity > 0
  and unit_price > 0
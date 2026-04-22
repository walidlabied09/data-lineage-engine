{{ config(materialized='table') }}

with base as (

    select
        -- Nettoyage & normalisation des champs bruts (tout en texte propre)
        nullif(trim("InvoiceNo"), '')          as invoice_no_raw,
        nullif(trim("StockCode"), '')          as stock_code_raw,
        nullif(trim("Description"), '')        as description_raw,
        nullif(trim("Country"), '')            as country_raw,
        nullif(trim("InvoiceDate"), '')        as invoice_date_raw,
        nullif(trim(("CustomerID")::text), '') as customer_id_raw,
        nullif(trim(("Quantity")::text), '')   as quantity_raw,
        nullif(trim(("UnitPrice")::text), '')  as unit_price_raw
    from {{ source('raw_airbyte', 'sales_data') }}

), typed as (

    select
        -- Identifiants + libellés
        invoice_no_raw                as invoice_no,
        stock_code_raw                as stock_code,
        coalesce(description_raw, '') as description,

        -- Quantity : accepter entiers et décimaux -> caster via numeric puis int
        case
            when quantity_raw ~ '^-?\d+(\.\d+)?$' then (quantity_raw::numeric)::int
        end as quantity,

        -- Unit price : décimal -> numeric(12,2)
        case
            when replace(unit_price_raw, ',', '.') ~ '^-?\d+(\.\d+)?$'
            then replace(unit_price_raw, ',', '.')::numeric(12,2)
        end as unit_price,

        -- CustomerID : souvent "17850.000000000" -> accepter décimal et caster en bigint
        case
            when customer_id_raw ~ '^\d+(\.0+)?$' then (customer_id_raw::numeric)::bigint
        end as customer_id,

        -- Date : format US sans zéro à gauche, 24h, secondes optionnelles
        coalesce(
            to_timestamp(trim(invoice_date_raw), 'FMMM/FMDD/YYYY FMHH24:MI:SS'),
            to_timestamp(trim(invoice_date_raw), 'FMMM/FMDD/YYYY FMHH24:MI')
        ) as invoice_ts,

        -- Pays normalisé
        upper(regexp_replace(country_raw, '\s+', ' ', 'g')) as country

    from base
),

filtered as (
    select
        *,
        {{ dbt_utils.generate_surrogate_key(['invoice_no','stock_code']) }} as sk
    from typed
    where invoice_no  is not null
      and stock_code  is not null
      and quantity    is not null
      and unit_price  is not null
      and invoice_ts  is not null
),

dedup as (
    select *
    from (
        select
            *,
            row_number() over (
                partition by sk
                order by invoice_ts desc, quantity desc, unit_price desc
            ) as rn
        from filtered
    ) x
    where rn = 1
)

select
    invoice_no,
    stock_code,
    description,
    quantity,
    unit_price,
    (quantity * unit_price)::numeric(12,2) as line_amount,
    customer_id,
    country,
    invoice_ts,
    sk
from dedup
where quantity   >= 0
  and unit_price >= 0

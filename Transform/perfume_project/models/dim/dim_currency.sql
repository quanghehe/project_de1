with raw_currency as (
  select distinct
    currency
  from {{ ref('stg_variants') }}
  where currency is not null
)

select
  row_number() over (order by currency) as currency_id,
  currency as currency_code,

  case 
    when currency = 'EUR' then 'Euro'
    when currency = 'USD' then 'US Dollar'
    when currency = 'VND' then 'Vietnamese Dong'
    when currency = 'GBP' then 'British Pound'
    else 'Unknown'
  end as currency_name

from raw_currency
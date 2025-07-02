select distinct
  currency
from {{ ref('fact_perfume_variants') }}
where currency is not null
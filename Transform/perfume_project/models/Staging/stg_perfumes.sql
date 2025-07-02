select
  id as product_id,
  name,
  brand,
  category,
  gender,
  url
from {{ source('public', 'perfumes') }}
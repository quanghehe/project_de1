select
  variant_id,
  perfume_id as product_id,
  price,
  size,
  currency,
  link as variant_url,
  vendor,
  sku,
  in_stock
from {{ source('public', 'variants') }}
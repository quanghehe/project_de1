SELECT
    v.variant_id,
    v.product_id,
    p.name,
    p.brand,
    p.category,
    p.gender,
    v.size,
    v.price,
    v.currency,
    v.in_stock,
    p.url AS perfume_url,
    v.variant_url

from {{ref('stg_variants')}} v
join {{ref('stg_perfumes')}} p 
on v.product_id = p.product_id
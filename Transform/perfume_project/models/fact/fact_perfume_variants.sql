SELECT
    v.variant_id,
    v.product_id,              
    sz.size_id,                
    cur.currency_id,           
    v.price,
    v.in_stock,
    v.variant_url
FROM {{ ref('stg_variants') }} v
JOIN {{ ref('stg_perfumes') }} p ON v.product_id = p.product_id
LEFT JOIN {{ ref('dim_size') }} sz ON v.size = sz.size
LEFT JOIN {{ ref('dim_currency') }} cur ON v.currency = cur.currency_code
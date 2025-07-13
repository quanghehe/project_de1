SELECT
    v.variant_id,
    p.perfume_name ,
    s.size AS size_ml,
    c.currency_code,
    v.price,
    v.in_stock,
    v.variant_url
FROM {{ ref('fact_perfume_variants') }} v
JOIN {{ ref('dim_perfume') }} p ON v.product_id = p.product_id
LEFT JOIN {{ ref('dim_size') }} s ON v.size_id = s.size_id
LEFT JOIN {{ ref('dim_currency') }} c ON v.currency_id = c.currency_id
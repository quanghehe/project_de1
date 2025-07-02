select distinct
    product_id,
    name as perfume_name,
    brand,
    category,
    gender,
    url
    from {{ref('stg_perfumes')}}

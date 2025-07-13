with distinct_sizes as (
    select distinct
        size 
        from {{ref('stg_variants')}}
        where size is not null
)

select 
    row_number() over (order by size) as size_id,
    size
    from distinct_sizes
with payment_rollup as (
    select
        order_id,
        sum(amount) as net_amount,
        count(*) as payment_event_count
    from {{ ref('stg_payments') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    coalesce(p.net_amount, 0) as net_amount,
    coalesce(p.payment_event_count, 0) as payment_event_count
from {{ ref('stg_orders') }} as o
left join payment_rollup as p using (order_id)


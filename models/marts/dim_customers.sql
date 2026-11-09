with customer_metrics as (
    select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as latest_order_date,
        count(*) as order_count,
        sum(case when order_status = 'completed' then net_amount else 0 end) as lifetime_revenue
    from {{ ref('int_order_payments') }}
    group by customer_id
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.signup_date,
    c.country_code,
    m.first_order_date,
    m.latest_order_date,
    coalesce(m.order_count, 0) as order_count,
    coalesce(m.lifetime_revenue, 0) as lifetime_revenue
from {{ ref('stg_customers') }} as c
left join customer_metrics as m using (customer_id)


select
    order_id,
    customer_id,
    order_date,
    order_status,
    payment_event_count,
    net_amount,
    case when order_status = 'completed' then net_amount else 0 end as recognized_revenue
from {{ ref('int_order_payments') }}


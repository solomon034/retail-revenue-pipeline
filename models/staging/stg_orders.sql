select
    cast(order_id as integer) as order_id,
    cast(customer_id as integer) as customer_id,
    date(order_date) as order_date,
    lower(trim(status)) as order_status
from {{ ref('raw_orders') }}


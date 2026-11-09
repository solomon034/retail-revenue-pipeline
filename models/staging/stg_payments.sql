select
    cast(payment_id as integer) as payment_id,
    cast(order_id as integer) as order_id,
    lower(trim(payment_method)) as payment_method,
    cast(amount as numeric) as amount
from {{ ref('raw_payments') }}


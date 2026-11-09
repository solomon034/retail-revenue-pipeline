select *
from {{ ref('fct_orders') }}
where recognized_revenue < 0


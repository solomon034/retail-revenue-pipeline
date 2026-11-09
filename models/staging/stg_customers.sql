select
    cast(customer_id as integer) as customer_id,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    date(signup_date) as signup_date,
    upper(trim(country)) as country_code
from {{ ref('raw_customers') }}


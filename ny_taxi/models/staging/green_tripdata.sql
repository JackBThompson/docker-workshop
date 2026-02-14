select * 
from {{ source('nytaxi', 'green_tripdata') }}
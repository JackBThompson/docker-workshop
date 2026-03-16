import json
import pandas as pd
from kafka import KafkaProducer
from time import time

# Load data
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
columns = [
    'lpep_pickup_datetime', 'lpep_dropoff_datetime',
    'PULocationID', 'DOLocationID', 'passenger_count',
    'trip_distance', 'tip_amount', 'total_amount'
]
df = pd.read_parquet(url, columns=columns)
print(f"Loaded {len(df)} rows")

# Producer setup
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer
)

# Send all rows
t0 = time()

for _, row in df.iterrows():
    record = row.to_dict()
    record['lpep_pickup_datetime']  = str(record['lpep_pickup_datetime'])
    record['lpep_dropoff_datetime'] = str(record['lpep_dropoff_datetime'])
    if pd.isna(record.get('passenger_count')):
        record['passenger_count'] = None
    producer.send('green-trips', value=record)

producer.flush()
t1 = time()
print(f'took {(t1 - t0):.2f} seconds')
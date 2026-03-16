import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='hw-q3',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=10000   # auto-stops after 10s of silence
)

total = 0
over_5 = 0

for message in consumer:
    trip = message.value
    total += 1
    if trip.get('trip_distance', 0) > 5.0:
        over_5 += 1

consumer.close()
print(f"Total: {total}, Distance > 5: {over_5}")
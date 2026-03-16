# Module 7 Homework: Stream Processing with PyFlink
 
## DE Zoomcamp 2026 | Dataset: Green Taxi — October 2025
 
---
 
## Dataset
 
This homework uses **Green Taxi Trip data from October 2025**:
 
```
green_tripdata_2025-10.parquet
```
 
---
 
## Questions
 
---
 
### Question 1: Redpanda Version
 
Run `rpk version` inside the Redpanda container:
 
```bash
docker exec -it 07_streaming-redpanda-1 rpk version
```
 
> What version of Redpanda are you running?
 
**Answer:** 25.3.9
 
---
 
### Question 2: Sending Data to Redpanda
 
Create a topic called `green-trips`:
 
**See producer.py**

> How long did it take to send the entire dataset and flush?
 
**Answer:** 10 seconds
 
---
 
### Question 3: Consumer — Trip Distance
 
Write a Kafka consumer that reads **all** messages from `green-trips` (set `auto_offset_reset='earliest'`).
 
**See consumer.py**
 
> How many trips have `trip_distance > 5`?
 
**Answer:** 8506 trips
 
---
 
### Question 4: Tumbling Window — Pickup Location *(PyFlink)*
 
Create the PostgreSQL results table before running the job:
 
```sql
CREATE TABLE hw_q4_window_trips (
    window_start TIMESTAMP,
    "pulocationid" INTEGER,
    num_trips BIGINT,
    PRIMARY KEY (window_start, "pulocationid")
);
```
 
Create a Flink job that reads from `green-trips` and uses a **5-minute tumbling window** to count trips per `PULocationID`. Write results to the table above.
 
After the job processes all data, query:
 
```sql
SELECT pulocationid, num_trips
FROM hw_q4_window_trips
ORDER BY num_trips DESC
LIMIT 3;
```
 
> Which `PULocationID` had the most trips in a single 5-minute window?
 
**Answer:** 74
 
---
 
### Question 5: Session Window — Longest Streak *(PyFlink)*
 
Create the PostgreSQL results table before running the job:
 
```sql
CREATE TABLE IF NOT EXISTS hw_q5_session_trips (
    window_start TIMESTAMP,
    window_end   TIMESTAMP,
    pulocationid INTEGER,
    num_trips    BIGINT,
    PRIMARY KEY (window_start, window_end, pulocationid)
);
```
 
Create a Flink job that uses a **session window with a 5-minute gap** on `PULocationID`, using `lpep_pickup_datetime` as the event time with a 5-second watermark tolerance.
 
A session window groups events that arrive within 5 minutes of each other. A gap of more than 5 minutes closes the window.
 
After results appear, query for the longest session:
 
```sql
SELECT pulocationid, num_trips, window_start, window_end
FROM hw_q5_session_trips
ORDER BY num_trips DESC
LIMIT 5;
```
 
> How many trips were in the longest session?
 
**Answer:** 81
 
---
 
### Question 6: Tumbling Window — Largest Tip *(PyFlink)*
 
Create the PostgreSQL results table before running the job:
 
```sql
CREATE TABLE IF NOT EXISTS hw_q6_tip_per_hour (
    window_start TIMESTAMP PRIMARY KEY,
    total_tip    DOUBLE PRECISION
);
```
 
Create a Flink job that uses a **1-hour tumbling window** to compute the total `tip_amount` per hour across all locations.
 
After results appear, query:
 
```sql
SELECT pulocationid, num_trips, window_start, window_end
FROM hw_q5_session_trips
ORDER BY num_trips DESC
LIMIT 5;
```
 
> Which hour had the highest total tip amount?
 
**Answer:** 2025-10-16 18:00:00
 
---

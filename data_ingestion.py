import pandas as pd
import psycopg2

DB_HOST = "localhost"  
DB_NAME = "yellow_taxi_db"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_PORT = "5432"

file_path= 'D:\\traffic_forecasting\\Data\\yellow_tripdata_2024-01.parquet'

data= pd.read_parquet(file_path)

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
cursor = conn.cursor()


for index,row in data.iterrows():
     cursor.execute("""
        INSERT INTO yellow_taxi_data (
            VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, 
            trip_distance, RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, 
            payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, 
            improvement_surcharge, total_amount, congestion_surcharge, Airport_fee
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, row)



conn.commit()
cursor.close()
conn.close()

print("Data loaded successfully!")



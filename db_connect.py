import psycopg2

DB_HOST = "localhost"  
DB_NAME = "yellow_taxi_db"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_PORT = "5432"


def connection():

    conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
    )
    

    cursor = conn.cursor()

    if cursor:
        print('Connection Established')

   

    
    conn.commit()
    #cursor.close()
    #conn.close()

    return cursor


connection()





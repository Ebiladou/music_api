import psycopg, time
from dotenv import load_dotenv
import os

load_dotenv()

while True:
    try:
        conn = psycopg.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            host=os.getenv("DATABASE_HOST"),
            password=os.getenv("DATABASE_PASSWORD")
        )

        conn.row_factory = psycopg.rows.dict_row

        cursor = conn.cursor()
        print('connected successfully')
        break
    except Exception as error:
        print('connection failed')
        print('error:', error)
        time.sleep(5)
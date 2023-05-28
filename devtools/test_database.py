import os
import psycopg2
print("HMM")
psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    user='postgres',
    password='postgres',
    database='postgres'
)

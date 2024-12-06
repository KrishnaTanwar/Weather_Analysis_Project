import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL server
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='admin',
    host='localhost',
    port='5432'
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# Create database
try:
    cursor.execute('CREATE DATABASE weatherdb')
    print("Database 'weatherdb' created successfully!")
except psycopg2.Error as e:
    print(f"Error creating database: {e}")
finally:
    cursor.close()
    conn.close()

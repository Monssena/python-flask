import psycopg2
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Database params
DB_HOST = "db"
DB_NAME = "hitcount"
DB_USER = "postgres"
DB_PASSWORD = "password"

def create_table():
    with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS counter (
                    id SERIAL PRIMARY KEY,
                    datetime TIMESTAMP NOT NULL,
                    client_info TEXT NOT NULL
                );
            ''')
            conn.commit()

def get_hit_count(client_info):
    current_time = datetime.now()
    with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
        with conn.cursor() as cursor:
            count = cursor.execute(
                'INSERT INTO counter (datetime, client_info) VALUES (%s, %s) RETURNING id;',
                (current_time, client_info)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            return new_id

@app.route('/')
def hello():
    create_table()
    client_info = f"{request.user_agent.string}"
    count = get_hit_count(client_info)
    return 'Hello World! I have been seen {} times.\n'.format(count)
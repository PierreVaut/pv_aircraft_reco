import os
from flask import Flask, jsonify
import psycopg2
from dotenv import load_dotenv

load_dotenv()

RDS_HOST = os.getenv("RDS_HOST")
RDS_NAME = os.getenv("RDS_NAME")
RDS_USER = os.getenv("RDS_USER")
RDS_PW = os.getenv("RDS_PW")

app = Flask(__name__)

# This code was largely inspired by ChatGPT
def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=RDS_HOST,
            database=RDS_NAME,
            user=RDS_USER,
            password=RDS_PW,
            port=5432
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None

@app.route('/')
def read_database():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, created_at FROM geo;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    user_list = [{"id": row[0], "name": row[1], "created_at": row[2]} for row in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)

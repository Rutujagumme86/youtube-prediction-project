import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def insert_data(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO predictions (category_id, like_count, comment_count, duration, predicted_views)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, data)
    conn.commit()
    conn.close()
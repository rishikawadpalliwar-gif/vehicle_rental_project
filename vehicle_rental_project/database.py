import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD",
            database="vehicle_rental_db"
        )
    except Error as e:
        print("Database connection error:", e)
        raise

import os
import mysql.connector
from mysql.connector import Error


def get_all_the_appoinments():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    courses = []

    if connection.is_connected():
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT d.id_client, d.full_name FROM dental_appointments as d;
            """
            cursor.execute(query)
            courses = cursor.fetchall()
            print(courses)
        except Error as e:
            print(f"Error while getting courses from database: {e}")
        finally:
            cursor.close()
            return courses
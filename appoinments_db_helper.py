import os
import mysql.connector
from mysql.connector import Error
        
def insert_appoinments_in_bulk(df, table_name='dental_appointments'):
    connection = None
    cursor = None

    try:

        #df['course_id'] = course_id
        
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Prepare the insert query
            insert_query = f"""
            INSERT INTO {table_name} (id_appointments, id_client, full_name, appointment_date, 
            treatment, name_dentist, payment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Convert DataFrame to list of tuples
            students_data = df.to_records(index=False).tolist()

            # Execute the insert query in bulk
            cursor.executemany(insert_query, students_data)
            
            # Commit the transaction
            connection.commit()

            print(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        print(f"Error Appoinments: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
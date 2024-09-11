import os
import mysql.connector
from mysql.connector import Error

def insert_clients_in_bulk(df, table_name='clients'):
    connection = None
    cursor = None

    try:

        
        
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
            INSERT INTO {table_name} (id, name, phone, email, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            # Convert DataFrame to list of tuples
            students_data = df.to_records(index=False).tolist()

            # Execute the insert query in bulk
            cursor.executemany(insert_query, students_data)
            
            # Commit the transaction
            connection.commit()

            print(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

# Example usage
# Assuming df is the DataFrame you want to insert:
# insert_students_in_bulk(df)
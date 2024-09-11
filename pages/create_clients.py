import os
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()



st.title("Create client")
identification = st.text_input('Identification')
name = st.text_input('name')
phone = st.number_input(label="Phone")
email = st.text_input(label="Email")
last_consultation = st.date_input(label="last consultation")
next_appointment = st.date_input(label="next appointment")
submit = st.button("Submit")

if submit:
    st.write(f"Course name is: {name}")
    st.write(f'database name: {os.getenv("DB_NAME")}')
    st.write(f'database name: {os.getenv("DB_USER")}')
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            query = """
            INSERT INTO clients (id, name, phone, email, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                identification,
                name,
                phone,
                email,
                last_consultation,
                next_appointment
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()

            st.write("The client has been successfully saved")

    except Error as e:
        st.error(f"Error connecting to database:{str(e)}")
        connection = None
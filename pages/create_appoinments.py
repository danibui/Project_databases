import os
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()



st.title("Create appoinments")
identification_appointment= st.text_input('Identification appointment')
identification_client = st.text_input('Identification client')
full_name = st.text_input('Full name')
appointment_date = st.date_input (label='appointment date')
treatment = st.text_input ('Treatment')
name_dentist = st.text_input ('Name dentist')
payment = True if st.radio("Pago", ["Sí", "No"]) == "Sí" else False
submit = st.button("Submit")

if submit:
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
            INSERT INTO clients (id_appointments, id_client, full_name, appointment_date, treatment, name_dentist, payment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                identification_appointment,
                identification_client,
                full_name,
                appointment_date,
                treatment,
                name_dentist,
                payment,
                submit
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()

            st.write("The course has been successfully saved")

    except Error as e:
        st.error(f"Error connecting to database:{str(e)}")
        connection = None
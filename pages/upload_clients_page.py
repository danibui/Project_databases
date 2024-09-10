import streamlit as st
import pandas as pd
from appoinments_db_helper import get_all_the_appoinments
from clients_db_helper import insert_clients_in_bulk

st.title("Upload students")

def extract_students_from_excel(excel_file, course_id):
    """Extracts student information from the provided Excel file."""
    try:
        df = pd.read_excel(excel_file)
        st.write("Excel file loaded successfully")
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return []

    df = df.rename(columns={
        'id paciente': 'id',
        'Nombre completo': 'name',
        'Telefono': 'phone',
        'Correo': 'email',
        'Fecha de la ultima consulta': 'start_date',
        'Proxima cita': 'end_date'
    })

    df = df[['id', 'name', 'phone', 'email', 'start_date', 'end_date']]

    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce').dt.strftime('%Y-%m-%d')

    insert_clients_in_bulk(df, course_id, table_name='clients')
    
    st.write(df)

# Obtener los cursos
courses = get_all_the_appoinments()

# Crear un diccionario para mapear IDs de cursos a sus nombres
course_dict = {course['id']: course['full_name'] for course in courses}
course_ids = list(course_dict.keys())

# Crear el dropdown con los IDs como valor de selección y los nombres como valor de visualización
selected_course_id = st.selectbox("Select a course", course_ids, format_func=lambda id: course_dict[id])

# Subir el archivo de Excel
uploaded_file = st.file_uploader("Attendance list Excel file", type=["xls", "xlsx"])

# Botón para procesar la carga y mostrar los valores
if st.button("Save students"):
    if uploaded_file is not None:
        extract_students_from_excel(uploaded_file, selected_course_id)
        st.write("Students have been created successfully")
    else:
        st.write("Please upload an Excel file.")

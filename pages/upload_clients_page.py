import streamlit as st
import pandas as pd
from appoinments_db_helper import insert_appoinments_in_bulk
from clients_db_helper import insert_clients_in_bulk

st.title("Upload students")

def extract_students_from_excel(excel_file, excel_file_2):
    """Extracts student information from the provided Excel file."""
    try:
        # Cargar ambos archivos Excel
        df = pd.read_excel(excel_file)
        dfAppoinnmets = pd.read_excel(excel_file_2)
        st.write("Excel files loaded successfully")
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return []

    # Renombrar columnas del primer DataFrame (archivo 1)
    df = df.rename(columns={
        'id paciente': 'id',
        'Nombre completo': 'name',
        'Telefono': 'phone',
        'Correo': 'email',
        'Fecha de la ultima consulta': 'start_date',
        'Proxima cita': 'end_date'
    })

    dfAppoinnmets = dfAppoinnmets.rename(columns={
        'id' : 'id_appointments'
    })

    dfAppoinnmets = dfAppoinnmets[['id_appointments', 'id_client', 'full_name', 'appointment_date', 'treatment', 'name_dentist', 'payment']]
    print(df)
    df = df[['id', 'name', 'phone', 'email', 'start_date', 'end_date']]

    # Convertir el 'id' a numérico y las fechas a formato adecuado
    df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    dfAppoinnmets['appointment_date'] = pd.to_datetime(dfAppoinnmets['appointment_date'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Verificar si las columnas para hacer el merge están en ambos DataFrames
    if 'id' in df.columns and 'id_client' in dfAppoinnmets.columns:
        # Fusionar los DataFrames usando 'id' del archivo 1 y 'id_client' del archivo 2
        merged_df = pd.merge(df, dfAppoinnmets, left_on='id', right_on='id_client', how='inner')
        st.write("Data merged successfully")
        st.write(merged_df)
    else:
        st.write("No common column 'id' and 'id_client' found to merge the data")

    # Insertar el DataFrame en la base de datos
    insert_clients_in_bulk(df, table_name='clients')
    insert_appoinments_in_bulk(dfAppoinnmets, table_name='dental_appointments')


# Subir el archivo de Excel
uploaded_file = st.file_uploader("Clients list Excel file", type=["xls", "xlsx"], key="fileClients")

# Subir el archivo de Excel
uploaded_file_2 = st.file_uploader("Appoinments list Excel file", type=["xls", "xlsx"], key="fileApponments")

# Botón para procesar la carga y mostrar los valores
if st.button("Save students"):
    if uploaded_file is not None:
        extract_students_from_excel(uploaded_file, uploaded_file_2)
        st.write("Students have been created successfully")
    else:
        st.write("Please upload an Excel file.")

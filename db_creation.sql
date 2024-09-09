CREATE DATABASE dental_office;


-- Tabla para almacenar la información del curso
CREATE TABLE clients (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone int NOT NULL,
    email VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
);

-- Tabla para almacenar la lista de estudiantes
CREATE TABLE dental_appointments (
    id_appointments INT AUTO_INCREMENT PRIMARY KEY,
    id_client int NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    appointment_date DATE NOT NULL,
    treatment VARCHAR(255) NOT NULL,
    name_dentist VARCHAR(255) NOT NULL,
    payment boolean NOT NULL,
    FOREIGN KEY (id_client) REFERENCES clients(id) ON DELETE CASCADE
);
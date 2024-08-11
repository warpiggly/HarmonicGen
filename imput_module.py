import csv
import os

def save_to_csv(data):
    # Obtiene la ruta del directorio donde está ubicado el archivo Python
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta completa para el archivo CSV
    csv_file_path = os.path.join(current_directory, 'data.csv')
    
    # Abre el archivo CSV en modo 'a' (append) para agregar nuevas filas
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data])
        
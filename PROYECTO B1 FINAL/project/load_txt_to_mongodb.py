# load_txt_to_mongodb.py
from pymongo import MongoClient
import os
import json

# Configuración de MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.reuters
collection = db.documents

# Ruta a la carpeta donde se encuentran los archivos del corpus
corpus_dir = r'C:\Users\byron\OneDrive\Documentos\GitHub\Proyecto\B1\reuters\txt_files'

# Función para cargar archivos TXT a MongoDB
def load_txt_to_mongodb(corpus_dir, collection):
    for filename in os.listdir(corpus_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(corpus_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                document = {
                    'filename': filename,
                    'content': content
                }
                collection.insert_one(document)
    print("Archivos TXT cargados a MongoDB.")

# Ejecutar la carga
load_txt_to_mongodb(corpus_dir, collection)

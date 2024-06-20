# load_inverted_index.py
from pymongo import MongoClient
import json

# Configuración de MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.reuters

# Ruta al archivo JSON con el índice invertido
inverted_index_file = 'tfidf_inverted_index.json'

# Cargar el archivo JSON a MongoDB
with open(inverted_index_file, 'r', encoding='utf-8') as file:
    inverted_index = json.load(file)
    db.inverted_index.insert_one(inverted_index)

print("Índice invertido JSON cargado a MongoDB.")

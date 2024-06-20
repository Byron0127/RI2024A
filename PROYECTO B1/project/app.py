# app.py
from flask import Flask, request, render_template, send_from_directory
from pymongo import MongoClient
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import numpy as np

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración de MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.reuters
collection = db.documents

# Cargar el índice invertido desde MongoDB
inverted_index = db.inverted_index.find_one()

# Cargar documentos preprocesados desde MongoDB a un DataFrame de pandas
documents = list(collection.find())
df = pd.DataFrame(documents)

# Vectorización usando TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_vectors = tfidf_vectorizer.fit_transform(df['content'])

# Ruta a la carpeta donde se encuentran los archivos del corpus
corpus_dir = r'C:\Users\byron\OneDrive\Documentos\GitHub\Proyecto\B1\reuters\txt_files'

# Página principal y manejo de búsqueda
@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ''
    page = 1
    per_page = 10
    total_results = 0
    
    if request.method == 'POST':
        query = request.form['query']
        page = int(request.form.get('page', 1))
        results = search_cosine(query, tfidf_vectorizer, tfidf_vectors)
        total_results = len(results)
        paginated_results = results[:per_page]  # Mostrar solo los primeros 10 resultados
        results = [{'filename': df.iloc[doc[0]]['filename'], 'snippet': df.iloc[doc[0]]['content'][:200], 'score': doc[1]} for doc in paginated_results]
    
    return render_template('index.html', query=query, results=results, page=page, per_page=per_page, total_results=total_results)

@app.route('/document/<filename>')
def document(filename):
    return send_from_directory(corpus_dir, filename)

# Función de búsqueda
THRESHOLD = 0.1

def cosine_similarity_query(query_vector, doc_vectors):
    return cosine_similarity(query_vector, doc_vectors).flatten()

def search_cosine(query, vectorizer, doc_vectors, threshold=THRESHOLD):
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity_query(query_vector, doc_vectors)
    ranked_docs = [(idx, scores[idx]) for idx in np.argsort(scores)[::-1] if scores[idx] >= threshold]
    return ranked_docs

if __name__ == '__main__':
    app.run(debug=True)

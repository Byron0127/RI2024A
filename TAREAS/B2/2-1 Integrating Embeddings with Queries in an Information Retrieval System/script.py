import pandas as pd
import numpy as np
from transformers import BertTokenizer, TFBertModel
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# Inicializa el pool de procesos con el tokenizador y el modelo BERT
def inicializar_pool(nombre_modelo):
    global tokenizador, modelo
    tokenizador = BertTokenizer.from_pretrained(nombre_modelo)
    modelo = TFBertModel.from_pretrained(nombre_modelo)

# Genera los embeddings BERT para un texto dado
def generar_embeddings_bert(texto):
    entradas = tokenizador(texto, return_tensors='tf', padding=True, truncation=True)
    salidas = modelo(**entradas)
    return salidas.last_hidden_state[:, 0, :]  # Obtiene la representación del token [CLS]

# Procesa textos en paralelo usando el modelo BERT
def procesar_textos_en_paralelo(textos, nombre_modelo):
    print("Inicio de la función")
    num_nucleos = cpu_count()
    print(f"Utilizando {num_nucleos} núcleos")
    pool = Pool(processes=num_nucleos, initializer=inicializar_pool, initargs=(nombre_modelo,))

    resultados = []
    with tqdm(total=len(textos)) as barra_progreso:
        # Procesa los textos en paralelo y actualiza la barra de progreso
        for resultado in pool.imap(generar_embeddings_bert, textos):
            resultados.append(resultado)
            barra_progreso.update()

    pool.close()
    pool.join()
    # Transpone el array de resultados para obtener el formato deseado
    return np.array(resultados).transpose(0, 2, 1)

if __name__ == "__main__":
    # Carga los datos del archivo CSV
    df_vino = pd.read_csv('./datos/winemag-data_first150k.csv')
    corpus = df_vino['description']
    
    # Calcula los embeddings BERT para el corpus de descripciones
    embeddings_bert = procesar_textos_en_paralelo(corpus, 'bert-base-uncased')
    
    # Guarda los embeddings en un archivo numpy
    np.save('bert_embeddings_completo.npy', embeddings_bert)

    
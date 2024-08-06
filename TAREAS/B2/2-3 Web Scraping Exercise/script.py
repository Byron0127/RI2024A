import pickle
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from multiprocessing import Pool, cpu_count

headers = {
    "User-Agent":"My Phyton App"
}
def process_link(link):
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")
        # Extracting the title
        title = soup.find("meta", {"property": "og:title"})["content"]
        # Extracting the description
        description = soup.find("meta", {"name": "description"})["content"]
        # Extracting the ingredients
        ingredients_section = soup.find_all("li", class_="mm-recipes-structured-ingredients__list-item")
        ingredients = [ingredient.get_text().strip() for ingredient in ingredients_section]

        # Extracting the instructions
        instructions_section = soup.find_all("p", class_="comp mntl-sc-block mntl-sc-block-html")
        instructions = [instruction.get_text().strip() for instruction in instructions_section]

        # Extracting the nutrition information
        nutrition_section = soup.find_all("span", class_="mm-recipes-nutrition-facts-label__nutrient-name mm-recipes-nutrition-facts-label__nutrient-name--has-postfix")
        nutrition_facts = [fact.parent.get_text().strip().replace('\n', ' ') for fact in nutrition_section]

        return {
            'Titulo': title,
            'Descripcion': description,
            'Ingredientes': ingredients,
            'Instrucciones': instructions,
            'Informacion Nutricional': nutrition_facts
        }
    except requests.exceptions.RequestException as e:
        return {
            'Titulo': '',
            'Descripcion': '',
            'Ingredientes': '',
            'Instrucciones': '',
            'Informacion Nutricional': ''
        }
    
if __name__ == '__main__':
        print('cargando links...')
        link_total = pickle.load(open('datos/total_links.pkl', 'rb'))
        print(f'links cargados: {len(link_total)}')
        num_processes = cpu_count()
        with Pool(processes=num_processes) as pool:
            results = list(tqdm(pool.imap(process_link, link_total), total=len(link_total), desc='Procesando'))

        # Convertir los resultados en un DataFrame
        corpus = pd.DataFrame(results)

        # Guardar el DataFrame con pickle
        with open('./corpus.pkl', 'wb') as f:
            pickle.dump(corpus, f)

        # Mostrar el DataFrame
        print(corpus)    
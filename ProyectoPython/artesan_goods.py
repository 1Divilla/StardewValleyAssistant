import requests
from bs4 import BeautifulSoup
import re
import os
import json

def clean_description(description):
    # Eliminar los atributos data-sort-value
    cleaned_description = re.sub(r'data-sort-value="\d+"', '', description)

    # Limpiar precios, conservando 'g' al final
    cleaned_description = re.sub(r'(\d+)g', r'\1g', cleaned_description)

    # Limpiar caracteres especiales HTML (si hay)
    cleaned_description = re.sub(r'&gt;|&quot;', '', cleaned_description)

    # Limpiar espacios adicionales y recortar
    cleaned_description = re.sub(r'\s+', ' ', cleaned_description).strip()

    # Formatear los rangos de precios (ej. "300–1,0g" a "300–1,000g")
    cleaned_description = re.sub(r'(\d+)(–)(\d+)', r'\1–\3', cleaned_description)

    return cleaned_description


def check_article(list_products):
    product_info = {}

    for product in list_products.copy():
        url = f'https://stardewvalleywiki.com/{product.replace(" ", "_")}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_description = soup.find('meta', attrs={'name': 'description'})
            
            if meta_description and 'content' in meta_description.attrs:
                description_content = meta_description['content'].strip().lower()
                description_content = clean_description(description_content)  # Limpiar el contenido de descripción
                
                if 'is an artisan good' in description_content:
                    product_info[product] = description_content  # Guardar la descripción limpia
                else:
                    list_products.remove(product)
            else:
                print(f"No se encontró la meta descripción para {product}.")
        else:
            print(f'Error al acceder a la página de {product}: {response.status_code}')
    
    return product_info

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f'Datos guardados en {filename}')
    
def get_info():
    url = 'https://stardewvalleywiki.com/Artisan_Goods'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tables = soup.find_all('table', {'class': 'wikitable'})
        
        list_product = []
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cells = row.find_all('td')
                if cells:
                    product_name = cells[0].text.strip()
                    
                    if product_name:
                        products = product_name.split('•')
                        for product in products:
                            cleaned_product = product.strip().replace('\xa0', ' ')
                            cleaned_product = re.sub(r'\s*\(\d+\)', '', cleaned_product)
                            list_product.append(cleaned_product)
        
        product_info = check_article(list_product)

        documents_path = os.path.expanduser("~/Documents")
        json_filename = os.path.join(documents_path, "StardewValleyAssistant", "artesan_goods.json")
        save_to_json(product_info, json_filename)
    else:
        print(f'Error al acceder a la página: {response.status_code}')

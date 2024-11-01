import requests
from bs4 import BeautifulSoup
import os
import json

def get_info():
    url = 'https://stardewvalleywiki.com/Festivals'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Recoger los festivales en un diccionario
        festivals_data = {
            "Spring": [],
            "Summer": [],
            "Fall": [],
            "Winter": []
        }

        # Encontrar todos los elementos con la clase 'mw-headline'
        headline_elements = soup.find_all(class_="mw-headline")

        # Extraer nombres de festivales y sus descripciones
        for headline in headline_elements:
            festival_name = headline.text.strip()
            # Evitar el encabezado "Spring" que no es un festival
            if festival_name == "Spring":
                continue

            # Encontrar la descripción del festival
            festival_description = ""
            next_element = headline.find_next()
            
            # Iterar a través de los elementos siguientes hasta encontrar un nuevo h2 o h3
            while next_element and next_element.name not in ['h2', 'h3']:
                if next_element.name == 'p':
                    festival_description += next_element.text.strip() + " "
                next_element = next_element.find_next()
            
            # Asumir que los nombres de los festivales estarán en las estaciones correspondientes
            if 'Spring' in headline.find_previous('h2').text:
                festivals_data["Spring"].append({"name": festival_name, "description": festival_description.strip()})
            elif 'Summer' in headline.find_previous('h2').text:
                festivals_data["Summer"].append({"name": festival_name, "description": festival_description.strip()})
            elif 'Fall' in headline.find_previous('h2').text:
                festivals_data["Fall"].append({"name": festival_name, "description": festival_description.strip()})
            elif 'Winter' in headline.find_previous('h2').text:
                festivals_data["Winter"].append({"name": festival_name, "description": festival_description.strip()})

        # Guardar los datos en JSON
        documents_path = os.path.expanduser("~/Documents")
        os.makedirs(os.path.join(documents_path, "StardewValleyAssistant"), exist_ok=True)
        json_filename = os.path.join(documents_path, "StardewValleyAssistant", "festivals.json")
        save_to_json(festivals_data, json_filename)
    else:
        print(f'Error al acceder a la página: {response.status_code}')


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f'Datos guardados en {filename}')
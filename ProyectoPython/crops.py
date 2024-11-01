import requests
from bs4 import BeautifulSoup
import os
import json

def get_info():
    url = 'https://stardewvalleywiki.com/Crops'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        crop_data = []
        current_season = None
        excluded_terms = ["Tools", "Views", "Navigation", "Search", "Personal", "Namespaces", "Variants", "More", "Links", "In other languages"]

        for element in soup.find_all(['h2', 'h3']):
            if element.name == 'h2' and "Crops" in element.get_text():
                current_season = element.get_text().split(" ")[0]
            
            elif element.name == 'h3' and current_season:
                crop_name = element.get_text(strip=True)
                
                if crop_name and not any(term in crop_name for term in excluded_terms):
                    # Guardar solo el nombre del cultivo y la temporada
                    crop_data.append({
                        'name': crop_name,
                        'season': current_season
                        
                    })
        # Guardar los datos en JSON
        documents_path = os.path.expanduser("~/Documents")
        json_filename = os.path.join(documents_path, "StardewValleyAssistant", "crops.json")
        save_to_json(crop_data, json_filename)
    else:
        print(f'Error al acceder a la página: {response.status_code}')

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f'Datos guardados en {filename}')

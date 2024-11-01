import requests
from bs4 import BeautifulSoup
import os
import json

def get_info():
    url = 'https://stardewvalleywiki.com/Fish'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        fish_data = []

        # Seleccionar la tabla de interés
        table = soup.find_all('table', class_='wikitable')[0]
        
        # Recorrer las filas de la tabla (omitimos el encabezado)
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            
            # Verificar que hay suficientes columnas
            if len(columns) > 8:
                # Extraer solo los datos que nos interesan
                name = columns[1].get_text(strip=True)
                location = columns[30].get_text(strip=True)
                time = columns[31].get_text(strip=True)
                season = columns[32].get_text(strip=True).replace(" ", ", ")
                weather = columns[33].get_text(strip=True)

                # Almacenar los datos en un diccionario
                fish_data.append({
                    "name": name,
                    "location": location,
                    "time": time,
                    "season": season,
                    "weather": weather
                })

        # Guardar los datos en JSON
        documents_path = os.path.expanduser("~/Documents")
        json_filename = os.path.join(documents_path, "StardewValleyAssistant", "fishes.json")
        save_to_json(fish_data, json_filename)
        
    else:
        print(f'Error al acceder a la página: {response.status_code}')
        
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f'Datos guardados en {filename}')
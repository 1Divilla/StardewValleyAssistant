import requests
from bs4 import BeautifulSoup
import os
import json

def get_villager_data(name):
    url = f'https://stardewvalleywiki.com/{name.replace(" ", "_")}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        table = soup.find('table', id='infoboxtable')
        
        # Inicializa el diccionario para almacenar la información del aldeano
        villager_data = {
            'Name': name,
            'Birthday': "No encontrado",
            'Loved Gifts': []
        }
        
        if table:
            rows = table.find_all('tr')
            
            for row in rows:
                header = row.find('td', id="infoboxsection")
                if header and "Birthday" in header.text:
                    villager_data['Birthday'] = row.find('td', id="infoboxdetail").text.strip()
                elif header and "Loved Gifts" in header.text:
                    gift_cells = row.find_all('span', class_='nametemplate')
                    for gift in gift_cells:
                        gift_name = gift.get_text(strip=True)
                        villager_data['Loved Gifts'].append(gift_name)
        
        return villager_data  # Devuelve el diccionario
    else:
        print(f'Error al acceder a la página: {response.status_code}')
        return None

def get_info(): 
    url = 'https://stardewvalleywiki.com/Villagers'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        villagers_gallery = soup.find_all('ul', class_='gallery mw-gallery-packed villagergallery')
        
        names = []
        villagers_data = []
        
        for gallery in villagers_gallery:
            # Comprueba si el encabezado anterior indica "Non-giftable NPCs"
            previous_header = gallery.find_previous_sibling("h2")
            if previous_header and "Non-giftable NPCs" in previous_header.text:
                continue  # Omite esta galería de non-giftables
            
            for li in gallery.find_all('li', class_='gallerybox'):
                name_tag = li.find('p').find('a')
                if name_tag:
                    name = name_tag.text.strip()
                    names.append(name)
        for name in names:
            villagers_data.append(get_villager_data(name))
        # Guardar los datos en JSON
        documents_path = os.path.expanduser("~/Documents")
        json_filename = os.path.join(documents_path, "StardewValleyAssistant", "villagers.json")
        save_to_json(villagers_data, json_filename)
    else:
        print(f'Error al acceder a la página: {response.status_code}')

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f'Datos guardados en {filename}')
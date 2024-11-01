# %% Imports
import customtkinter as ctk
import os
import json
import artesan_goods
import fishes
import crops
import festivals
import villagers
# %% App
class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Stardew Valley Assistant")
        ancho = round(self.root.winfo_screenwidth() / 2)
        alto = round(self.root.winfo_screenheight() / 2)
        self.root.minsize(ancho, alto)

        # Textbox
        self.textbox = ctk.CTkTextbox(self.root, font=("Arial", 20), wrap="word")
        self.textbox.pack(expand=True, fill="both", padx=20, pady=(20, 5))

        # Entry
        self.entry = ctk.CTkEntry(self.root, font=("Arial", 22))
        self.entry.pack(fill="x", padx=20, pady=(5, 20))

        # Bind the entry to handle input on pressing Enter
        self.entry.bind("<Return>", self.handle_input)

        # Start the main menu
        self.current_menu = self.main_menu
        self.current_menu()  # Llamada inicial sin argumentos

    def handle_input(self, event):
        user_input = self.entry.get()
        self.entry.delete(0, 'end')
        self.process_input(user_input)

    def process_input(self, user_input):
        self.clear_textbox()

        if self.current_menu == self.main_menu:
            if user_input == '':
                self.main_menu()
            elif user_input == '1':
                self.current_menu = self.display_artisan_goods
                self.current_menu()  # Llamada sin argumentos
            elif user_input == '2':
                self.current_menu = self.display_villagers
                self.current_menu()  # Llamada sin argumentos
            elif user_input == '3':
                self.current_menu = self.display_crops
                self.current_menu()  # Llamada sin argumentos
            elif user_input == '4':
                self.current_menu = self.display_fishes
                self.current_menu()  # Llamada sin argumentos
            elif user_input == '5':
                self.current_menu = self.display_festivals
                self.current_menu()  # Llamada sin argumentos
            else:
                self.main_menu()

        elif self.current_menu in [self.display_artisan_goods, self.display_villagers, self.display_crops, self.display_fishes, self.display_festivals]:
            # Aquí se maneja el caso donde la entrada es necesaria para la submenu.
            self.current_menu(user_input)  # Llamada con el argumento

        self.textbox.configure(state="disabled")

    def main_menu(self):
        self.clear_textbox()
        self.textbox.insert("end", "Stardew Valley Assistant\n")
        self.textbox.insert("end", "1. Artisan Goods\n")
        self.textbox.insert("end", "2. Villagers\n")
        self.textbox.insert("end", "3. Crops\n")
        self.textbox.insert("end", "4. Fishes\n")
        self.textbox.insert("end", "5. Festivals\n")
        self.textbox.configure(state="disabled")
    
    def display_artisan_goods(self, user_input=None):
        # Ruta al archivo JSON en Documentos
        documents_path = os.path.expanduser("~/Documents/StardewValleyAssistant/artesan_goods.json")
    
        # Leer el JSON una sola vez y guardar los datos
        try:
            with open(documents_path, 'r', encoding='utf-8') as file:
                artisan_goods = json.load(file)
        except FileNotFoundError:
            self.clear_textbox()
            self.textbox.insert("end", "Error: No se encontró el archivo artesan_goods.json.\n")
            self.textbox.configure(state="disabled")
            return
    
        if user_input is None:
            self.clear_textbox()
            self.textbox.insert("end", "Stardew Valley Assistant -Artisan Goods\n")
            self.textbox.insert("end", "1. Back to Main Menu\n")
            
            # Listar todos los artículos
            for item in artisan_goods.keys():
                self.textbox.insert("end", f"{item}\n")
        else:
            if user_input == '1':
                self.current_menu = self.main_menu
                self.current_menu()
            elif user_input in artisan_goods:
                self.clear_textbox()
                self.textbox.insert("end", f"Stardew Valley Assistant -Artisan Goods -{user_input}\n")
                self.textbox.insert("end", "1. Back to Main Menu\n")
                self.textbox.insert("end", f"\n{user_input}: {artisan_goods[user_input]}\n")
            else:
                self.display_artisan_goods()
        self.textbox.configure(state="disabled")

    def display_villagers(self, user_input=None):
        # Ruta al archivo JSON en Documentos
        documents_path = os.path.expanduser("~/Documents/StardewValleyAssistant/villagers.json")
    
        # Leer el JSON una sola vez y guardar los datos
        try:
            with open(documents_path, 'r', encoding='utf-8') as file:
                villagers = json.load(file)  # Cargar como una lista de diccionarios
        except FileNotFoundError:
            self.clear_textbox()
            self.textbox.insert("end", "Error: No se encontró el archivo villagers.json.\n")
            self.textbox.configure(state="disabled")
            return
    
        if user_input is None:
            self.clear_textbox()
            self.textbox.insert("end", "Stardew Valley Assistant -Villagers\n")
            self.textbox.insert("end", "1. Back to Main Menu\n")
    
            for villager in villagers:
                self.textbox.insert("end", f"{villager['Name']}\n")
        else:
            if user_input == '1':
                self.current_menu = self.main_menu
                self.current_menu()
            else:
                villager_info = None
                for villager in villagers:
                    if villager["Name"].lower() == user_input.lower():
                        villager_info = villager
                        break
                if villager_info:
                    self.clear_textbox()
                    self.textbox.insert("end", f"Stardew Valley Assistant -Villagers - {villager_info['Name']}\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", f"\nName: {villager_info['Name']}\n")
                    self.textbox.insert("end", f"Birthday: {villager_info['Birthday']}\n")
                    self.textbox.insert("end", f"Loved Gifts: {', '.join(villager_info['Loved Gifts'])}\n")
                else:
                    self.clear_textbox()
                    self.textbox.insert("end", "Stardew Valley Assistant -Villagers\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", "Error: Villager not found\n")
    
        self.textbox.configure(state="disabled")

    def display_crops(self, user_input=None):
        # Ruta al archivo JSON en Documentos
        documents_path = os.path.expanduser("~/Documents/StardewValleyAssistant/crops.json")
    
        # Leer el JSON una sola vez y guardar los datos
        try:
            with open(documents_path, 'r', encoding='utf-8') as file:
                crops = json.load(file)  # Cargar como una lista de diccionarios
        except FileNotFoundError:
            self.clear_textbox()
            self.textbox.insert("end", "Error: No se encontró el archivo crops.json.\n")
            self.textbox.configure(state="disabled")
            return
    
        if user_input is None:
            self.clear_textbox()
            self.textbox.insert("end", "Stardew Valley Assistant -Crops\n")
            self.textbox.insert("end", "1. Back to Main Menu\n")
    
            # Listar todos los cultivos
            for crop in crops:  # Asegúrate de que crops sea una lista de diccionarios
                self.textbox.insert("end", f"{crop['name']}\n")
        else:
            if user_input == '1':
                self.current_menu = self.main_menu
                self.current_menu()
            else:
                crop_info = None
                for crop in crops:
                    if crop["name"].lower() == user_input.lower():
                        crop_info = crop
                        break
                if crop_info:
                    self.clear_textbox()
                    self.textbox.insert("end", f"Stardew Valley Assistant -Crops -{crop_info['name']}\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", f"\nName: {crop_info['name']}\n")
                    self.textbox.insert("end", f"Season: {crop_info['season']}\n")
                else:
                    self.clear_textbox()
                    self.textbox.insert("end", "Stardew Valley Assistant -Crops\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", "Error: Crop not found\n")
    
        self.textbox.configure(state="disabled")

    def display_fishes(self, user_input=None):
        # Ruta al archivo JSON en Documentos
        documents_path = os.path.expanduser("~/Documents/StardewValleyAssistant/fishes.json")
    
        # Leer el JSON una sola vez y guardar los datos
        try:
            with open(documents_path, 'r', encoding='utf-8') as file:
                fishes = json.load(file)  # Cargar como una lista de diccionarios
        except FileNotFoundError:
            self.clear_textbox()
            self.textbox.insert("end", "Error: No se encontró el archivo fishes.json.\n")
            self.textbox.configure(state="disabled")
            return
    
        if user_input is None:
            self.clear_textbox()
            self.textbox.insert("end", "Stardew Valley Assistant -Fishes\n")
            self.textbox.insert("end", "1. Back to Main Menu\n")
    
            # Listar todos los pescados
            for fish in fishes:  # Asegúrate de que fishes sea una lista de diccionarios
                self.textbox.insert("end", f"{fish['name']}\n")
        else:
            if user_input == '1':
                self.current_menu = self.main_menu
                self.current_menu()
            else:
                fish_info = None
                for fish in fishes:
                    if fish["name"].lower() == user_input.lower():
                        fish_info = fish
                        break
                if fish_info:
                    self.clear_textbox()
                    self.textbox.insert("end", f"Stardew Valley Assistant -Fishes -{fish_info['name']}\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", f"\nName: {fish_info['name']}\n")
                    self.textbox.insert("end", f"Location: {fish_info['location']}\n")
                    self.textbox.insert("end", f"Time: {fish_info['time']}\n")
                    self.textbox.insert("end", f"Season: {fish_info['season']}\n")
                    self.textbox.insert("end", f"Weather: {fish_info['weather']}\n")
                else:
                    self.clear_textbox()
                    self.textbox.insert("end", "Stardew Valley Assistant - Fishes\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", "Error: Fish not found\n")
    
        self.textbox.configure(state="disabled")

    def display_festivals(self, user_input=None):
        # Ruta al archivo JSON en Documentos
        documents_path = os.path.expanduser("~/Documents/StardewValleyAssistant/festivals.json")
    
        # Leer el JSON una sola vez y guardar los datos
        try:
            with open(documents_path, 'r', encoding='utf-8') as file:
                festivals = json.load(file)  # Cargar como una lista de diccionarios
        except FileNotFoundError:
            self.clear_textbox()
            self.textbox.insert("end", "Error: No se encontró el archivo festivals.json.\n")
            self.textbox.configure(state="disabled")
            return
    
        if user_input is None:
            self.clear_textbox()
            self.textbox.insert("end", "Stardew Valley Assistant - Festivals\n")
            self.textbox.insert("end", "1. Back to Main Menu\n")
    
            # Listar todos los festivales
            for season, events in festivals.items():
                self.textbox.insert("end", f"{season.capitalize()} Festivals:\n")
                for event in events:
                    self.textbox.insert("end", f"  - **{event['name']}**\n")
        else:
            if user_input == '1':
                self.current_menu = self.main_menu
                self.current_menu()
            else:
                festival_info = None
                # Buscar el festival por nombre
                for season, events in festivals.items():
                    for event in events:
                        if event["name"].lower() == user_input.lower():
                            festival_info = event
                            break
                    if festival_info:
                        break
                
                if festival_info:
                    self.clear_textbox()
                    self.textbox.insert("end", f"Stardew Valley Assistant - Festivals - {festival_info['name']}\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", f"\nName: {festival_info['name']}\n")
                    self.textbox.insert("end", f"Description: {festival_info['description']}\n")
                else:
                    self.clear_textbox()
                    self.textbox.insert("end", "Stardew Valley Assistant - Festivals\n")
                    self.textbox.insert("end", "1. Back to Main Menu\n")
                    self.textbox.insert("end", "Error: Festival not found\n")
    
        self.textbox.configure(state="disabled")


    def clear_textbox(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
# %% 
def load_archives():
    documents_path = os.path.expanduser("~/Documents")
    new_folder = "StardewValleyAssistant"
    new_folder_path = os.path.join(documents_path, new_folder)
    
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f'Carpeta creada: {new_folder_path}')
    else:
        print(f'La carpeta ya existe: {new_folder_path}')
    
    # Definir los archivos JSON
    jsons = ["artesan_goods.json", "fishes.json", "crops.json", "villagers.json", "festivals.json"]
    
    for row in jsons:
        json_filename = os.path.join(new_folder_path, row)
        if not os.path.exists(json_filename):
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump({}, json_file, ensure_ascii=False, indent=4)  # Crear un JSON vacío
            print(f'Archivo creado: {json_filename}')
            artesan_goods.get_info()
            fishes.get_info()
            crops.get_info()
            villagers.get_info()
            festivals.get_info()
        else:
            print(f'El archivo ya existe: {json_filename}')
# %% Main
if __name__ == "__main__":
    load_archives()
    app = App()
    app.root.mainloop()
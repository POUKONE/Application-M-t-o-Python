import requests
import json
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk # Pour gérer les images
from datetime import datetime
import os # Pour gérer les chemins des icônes


# REMPLACER CECI par votre vraie clé API
API_KEY = "b8a3988240a92c212cf95709db946207"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city_name):
    """Récupère les données météo pour une ville donnée."""
    
    # Paramètres de la requête : ville, clé API, et unités métriques
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric', # Pour obtenir les températures en Celsius
        'lang': 'fr'       # Pour obtenir la description en français
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Lève une exception si la requête échoue (ex: 404)
        
        data = response.json()
        
        # Vérification si la ville est trouvée
        if data.get("cod") == 200:
            # Extraction des informations pertinentes
            weather_info = {
                "ville": data['name'],
                "temperature": f"{data['main']['temp']}°C",
                "description": data['weather'][0]['description'].capitalize(),
                "humidite": f"{data['main']['humidity']}%",
                "vent": f"{data['wind']['speed']} m/s"
            }
            return weather_info
        else:
            return {"erreur": "Ville non trouvée ou problème d'API."}

    except requests.exceptions.RequestException as e:
        return {"erreur": f"Erreur de connexion : {e}"}

# --- Exemple d'utilisation (peut être supprimé plus tard) ---
# print(get_weather_data("Paris"))


# (Collez ici le code de la fonction get_weather_data de l'Étape 1)

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk # Pour gérer les images
import requests
import json
from datetime import datetime
import os # Pour gérer les chemins des icônes

# =======================================================
# Configuration et Clé API
# =======================================================

API_KEY = "b8a3988240a92c212cf95709db946207" # 🚨 REMPLACEZ ICI
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# =======================================================
# Fonction de Récupération des Données Météo
# =======================================================

def get_weather_data(city_name):
    """Récupère les données météo pour une ville donnée."""
    if API_KEY == "VOTRE_CLÉ_OPENWEATHERMAP" or not API_KEY:
        return {"erreur": "Veuillez insérer une clé API OpenWeatherMap valide dans le script !"}

    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric', # Températures en Celsius
        'lang': 'fr'       # Description en français
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 404:
            return {"erreur": f"Ville '{city_name}' non trouvée."}
        if response.status_code == 401:
            return {"erreur": "Clé API OpenWeatherMap invalide ou expirée."}
        if response.status_code != 200:
            return {"erreur": f"Erreur de l'API ({response.status_code})."}
        
        data = response.json()
        
        # Lever et Coucher du soleil (convertir en heure locale lisible)
        sunrise_timestamp = data['sys']['sunrise']
        sunset_timestamp = data['sys']['sunset']
        
        # Utiliser le décalage horaire de la ville pour une heure locale correcte
        timezone_offset = data['timezone'] # Offset en secondes par rapport à UTC
        
        #sunrise_dt_utc = datetime.utcfromtimestamp(sunrise_timestamp)
        #sunset_dt_utc = datetime.utcfromtimestamp(sunset_timestamp)

        #sunrise_local = sunrise_dt_utc + timedelta(seconds=timezone_offset)
        #sunset_local = sunset_dt_utc + timedelta(seconds=timezone_offset)

        weather_info = {
            "ville": data['name'],
            "pays": data['sys']['country'],
            "temperature": f"{data['main']['temp']:.1f}°C",
            "description": data['weather'][0]['description'].capitalize(),
            "icone_code": data['weather'][0]['icon'], # Code pour l'icône (ex: "01d", "04n")
            "humidite": f"{data['main']['humidity']}%",
            "vent": f"{data['wind']['speed']:.1f} m/s",
            "pression": f"{data['main']['pressure']} hPa",
            #"lever_soleil": sunrise_local.strftime('%H:%M'),
            #"coucher_soleil": sunset_local.strftime('%H:%M'),
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        return {"erreur": f"Erreur de connexion réseau : {e}"}
    except KeyError as e:
        return {"erreur": f"Données API manquantes : {e}. Réponse API inattendue."}
    except Exception as e:
        return {"erreur": f"Une erreur inattendue est survenue : {e}"}


# =======================================================
# Fonctions de Gestion des Icônes Météo
# =======================================================

# Assurez-vous d'avoir un dossier 'icons' à côté de votre script
# et des fichiers comme '01d.png', '04n.png', etc.
ICON_PATH = os.path.join(os.path.dirname(__file__), "icons")

# Mapping des codes OpenWeatherMap vers vos fichiers d'icônes
# Ces noms de fichiers doivent correspondre aux codes d'icônes OpenWeatherMap
# Vous devrez peut-être les ajuster si vos noms de fichiers sont différents
ICON_MAPPING = {
    "01d": "01d.png", # Ciel clair jour
    "01n": "01n.png", # Ciel clair nuit
    "02d": "02d.png", # Peu nuageux jour
    "02n": "02n.png", # Peu nuageux nuit
    "03d": "03d.png", # Nuageux jour
    "03n": "03n.png", # Nuageux nuit
    "04d": "04d.png", # Très nuageux jour
    "04n": "04n.png", # Très nuageux nuit
    "09d": "09d.png", # Pluie faible jour
    "09n": "09n.png", # Pluie faible nuit
    "10d": "10d.png", # Pluie jour
    "10n": "10n.png", # Pluie nuit
    "11d": "11d.png", # Orage jour
    "11n": "11n.png", # Orage nuit
    "13d": "13d.png", # Neige jour
    "13n": "13n.png", # Neige nuit
    "50d": "50d.png", # Brouillard jour
    "50n": "50n.png", # Brouillard nuit
    # Ajoutez un icône par défaut si un code n'est pas mappé
    "default": "default.png" 
}

def get_weather_icon(icon_code, size=(64, 64)):
    """Charge une icône météo basée sur le code OpenWeatherMap."""
    icon_filename = ICON_MAPPING.get(icon_code, ICON_MAPPING["default"])
    icon_filepath = os.path.join(ICON_PATH, icon_filename)

    try:
        # Charger l'image avec PIL (Pillow)
        img = Image.open(icon_filepath)
        img = img.resize(size, Image.Resampling.LANCZOS)
        # Convertir pour CustomTkinter
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except FileNotFoundError:
        print(f"Erreur : Icône '{icon_filepath}' introuvable. Utilisez une icône par défaut si disponible.")
        # Tenter de charger une icône par défaut si l'icône spécifique est manquante
        try:
            default_icon_filepath = os.path.join(ICON_PATH, ICON_MAPPING["default"])
            img = Image.open(default_icon_filepath)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except FileNotFoundError:
            messagebox.showerror("Erreur Icône", "Icône par défaut introuvable. Vérifiez le dossier 'icons'.")
            return None # Retourne None si même l'icône par défaut est manquante
    except Exception as e:
        print(f"Erreur lors du chargement de l'icône {icon_filepath}: {e}")
        return None


# =======================================================
# Fonctions de l'Interface Utilisateur
# =======================================================

def update_weather_display(weather_data):
    """Met à jour les labels de l'interface avec les données météo."""
    if "erreur" in weather_data:
        messagebox.showerror("Erreur Météo", weather_data['erreur'])
        # Nettoyer les anciens affichages
        city_country_label.configure(text="")
        weather_icon_label.configure(image=None) # Supprime l'ancienne icône
        description_label.configure(text="")
        temperature_label.configure(text="")
        details_frame.pack_forget() # Cache le cadre des détails
        return

    # Mettre à jour les labels principaux
    city_country_label.configure(text=f"{weather_data['ville']}, {weather_data['pays']}")
    description_label.configure(text=weather_data['description'].capitalize())
    temperature_label.configure(text=weather_data['temperature'])

    # Charger et afficher l'icône météo
    icon_image = get_weather_icon(weather_data['icone_code'])
    if icon_image:
        weather_icon_label.configure(image=icon_image, text="") # text="" pour enlever tout texte résiduel
    else:
        weather_icon_label.configure(text="Pas d'icône", image=None)

    # Mettre à jour les détails supplémentaires
    humidite_label.configure(text=f"Humidité: {weather_data['humidite']}")
    vent_label.configure(text=f"Vent: {weather_data['vent']}")
    pression_label.configure(text=f"Pression: {weather_data['pression']}")
    sunrise_label.configure(text=f"Lever du soleil: {weather_data['lever_soleil']}")
    sunset_label.configure(text=f"Coucher du soleil: {weather_data['coucher_soleil']}")
    details_frame.pack(pady=10) # Affiche le cadre des détails

def search_weather():
    """Fonction appelée par le bouton pour lancer la recherche météo."""
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Attention", "Veuillez entrer le nom d'une ville.")
        return
    
    weather_data = get_weather_data(city)
    update_weather_display(weather_data)

def toggle_theme():
    """Bascule entre le mode clair et le mode sombre."""
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        theme_button.configure(text="Mode Sombre")
    else:
        ctk.set_appearance_mode("Dark")
        theme_button.configure(text="Mode Clair")

# =======================================================
# Configuration de l'Interface CustomTkinter
# =======================================================

ctk.set_appearance_mode("System") # Définit le thème par défaut sur celui du système
ctk.set_default_color_theme("blue") # Définit la palette de couleurs

app = ctk.CTk()
app.title("Météo en Direct")
app.geometry("500x700") # Taille de fenêtre légèrement plus grande
app.resizable(False, False) # Empêche le redimensionnement

# --- Cadre principal ---
main_frame = ctk.CTkFrame(app, corner_radius=10)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# --- Entrée de la ville et bouton de recherche ---
city_input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
city_input_frame.pack(pady=10)

city_entry = ctk.CTkEntry(city_input_frame, width=250, placeholder_text="Entrez le nom d'une ville...")
city_entry.pack(side="left", padx=5)

search_button = ctk.CTkButton(city_input_frame, text="Rechercher", command=search_weather)
search_button.pack(side="left", padx=5)

# --- Affichage des résultats principaux ---
result_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
result_frame.pack(pady=20)

city_country_label = ctk.CTkLabel(result_frame, text="", font=ctk.CTkFont(size=24, weight="bold"))
city_country_label.pack(pady=5)

# Label pour l'icône météo
weather_icon_label = ctk.CTkLabel(result_frame, text="", image=None) # L'image sera mise à jour dynamiquement
weather_icon_label.pack(pady=5)

temperature_label = ctk.CTkLabel(result_frame, text="", font=ctk.CTkFont(size=48, weight="bold"))
temperature_label.pack(pady=10)

description_label = ctk.CTkLabel(result_frame, text="", font=ctk.CTkFont(size=18))
description_label.pack(pady=5)

# --- Cadre des détails supplémentaires ---
details_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=("gray85", "gray15"))
details_frame.pack(pady=10, padx=10, fill="x") # Sera caché/montré dynamiquement

ctk.CTkLabel(details_frame, text="Détails Météo", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

humidite_label = ctk.CTkLabel(details_frame, text="Humidité:")
humidite_label.pack(anchor="w", padx=10, pady=2)

vent_label = ctk.CTkLabel(details_frame, text="Vent:")
vent_label.pack(anchor="w", padx=10, pady=2)

pression_label = ctk.CTkLabel(details_frame, text="Pression:")
pression_label.pack(anchor="w", padx=10, pady=2)

sunrise_label = ctk.CTkLabel(details_frame, text="Lever du soleil:")
sunrise_label.pack(anchor="w", padx=10, pady=2)

sunset_label = ctk.CTkLabel(details_frame, text="Coucher du soleil:")
sunset_label.pack(anchor="w", padx=10, pady=2)

# Cacher le cadre des détails au démarrage
details_frame.pack_forget()

# --- Bouton de thème ---
theme_button = ctk.CTkButton(app, text="Mode Sombre", command=toggle_theme)
theme_button.pack(pady=10)

# Lancement de la boucle principale de l'interface graphique
app.mainloop()
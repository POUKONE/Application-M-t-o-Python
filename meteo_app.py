import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import requests
from datetime import datetime, timedelta
import os
import threading

# =======================================================
# Design system
# ---------------------------------------------------------
# Neuropath Edge  -> hiérarchie spatiale claire (zones : header,
#                    recherche, résultat hero, grille de stats)
# Ultra Design    -> échelle d'espacement fixe, rayons et
#                    typographie cohérents, pixel-perfect
# Hyperkit        -> requête réseau non bloquante (thread) +
#                    retour visuel instantané pendant le chargement
# Motion TM       -> micro-animations qui révèlent le résultat
#                    et guident l'œil vers l'action (recherche)
# =======================================================

SPACE_XS, SPACE_SM, SPACE_MD, SPACE_LG, SPACE_XL = 4, 8, 16, 24, 32
RADIUS_CARD, RADIUS_CONTROL = 18, 12

COLOR_BG = ("#EEF1F8", "#0F1120")
COLOR_CARD = ("#FFFFFF", "#1B1E30")
COLOR_CARD_ALT = ("#F3F5FB", "#161829")
COLOR_ACCENT = "#5B7CFA"
COLOR_ACCENT_HOVER = "#3F5FE0"
COLOR_TEXT_MUTED = ("#6B7280", "#8B93A8")

FONT_FAMILY = "Helvetica"


def font(size, weight="normal"):
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


# =======================================================
# Configuration et Clé API
# =======================================================

# La clé doit être fournie via la variable d'environnement OPENWEATHER_API_KEY
# (ex: export OPENWEATHER_API_KEY="votre_clé" avant de lancer le script)
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# =======================================================
# Fonction de Récupération des Données Météo
# =======================================================

def get_weather_data(city_name):
    """Récupère les données météo pour une ville donnée."""
    if not API_KEY:
        return {"erreur": "Veuillez définir la variable d'environnement OPENWEATHER_API_KEY avec une clé API OpenWeatherMap valide !"}

    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric', # Températures en Celsius
        'lang': 'fr'       # Description en français
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=8)

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

        sunrise_dt_utc = datetime.utcfromtimestamp(sunrise_timestamp)
        sunset_dt_utc = datetime.utcfromtimestamp(sunset_timestamp)

        sunrise_local = sunrise_dt_utc + timedelta(seconds=timezone_offset)
        sunset_local = sunset_dt_utc + timedelta(seconds=timezone_offset)

        weather_info = {
            "ville": data['name'],
            "pays": data['sys']['country'],
            "temperature": f"{data['main']['temp']:.1f}°",
            "description": data['weather'][0]['description'].capitalize(),
            "icone_code": data['weather'][0]['icon'], # Code pour l'icône (ex: "01d", "04n")
            "humidite": f"{data['main']['humidity']}%",
            "vent": f"{data['wind']['speed']:.1f} m/s",
            "pression": f"{data['main']['pressure']} hPa",
            "lever_soleil": sunrise_local.strftime('%H:%M'),
            "coucher_soleil": sunset_local.strftime('%H:%M'),
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

ICON_PATH = os.path.join(os.path.dirname(__file__), "icons")

ICON_MAPPING = {
    "01d": "01d.png", "01n": "01n.png",
    "02d": "02d.png", "02n": "02n.png",
    "03d": "03d.png", "03n": "03n.png",
    "04d": "04d.png", "04n": "04n.png",
    "09d": "09d.png", "09n": "09n.png",
    "10d": "10d.png", "10n": "10n.png",
    "11d": "11d.png", "11n": "11n.png",
    "13d": "13d.png", "13n": "13n.png",
    "50d": "50d.png", "50n": "50n.png",
    "default": "default.png",
}


def get_weather_icon(icon_code, size=(96, 96)):
    """Charge une icône météo basée sur le code OpenWeatherMap."""
    icon_filename = ICON_MAPPING.get(icon_code, ICON_MAPPING["default"])
    icon_filepath = os.path.join(ICON_PATH, icon_filename)

    try:
        img = Image.open(icon_filepath)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except FileNotFoundError:
        print(f"Erreur : Icône '{icon_filepath}' introuvable.")
        try:
            default_icon_filepath = os.path.join(ICON_PATH, ICON_MAPPING["default"])
            img = Image.open(default_icon_filepath)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except FileNotFoundError:
            return None
    except Exception as e:
        print(f"Erreur lors du chargement de l'icône {icon_filepath}: {e}")
        return None


# =======================================================
# Micro-animations (Motion TM)
# =======================================================

def animate_reveal(widget, start_pad=48, end_pad=SPACE_SM, steps=10, delay=14):
    """Fait glisser un widget vers sa position finale pour révéler le résultat."""
    step_size = (end_pad - start_pad) / steps

    def run(i, current):
        if i >= steps:
            widget.pack_configure(pady=(end_pad, SPACE_SM))
            return
        widget.pack_configure(pady=(round(current), SPACE_SM))
        widget.after(delay, lambda: run(i + 1, current + step_size))

    run(0, start_pad)


def pulse_text_color(label, accent, normal, times=2, delay=110):
    """Fait clignoter brièvement une valeur pour attirer l'œil dessus."""
    sequence = [accent, normal] * times

    def run(i):
        if i >= len(sequence):
            label.configure(text_color=normal)
            return
        label.configure(text_color=sequence[i])
        label.after(delay, lambda: run(i + 1))

    run(0)


def breathe_cta():
    """Fait respirer le bouton de recherche pour inviter à l'action."""
    if is_loading:
        app.after(700, breathe_cta)
        return
    current = search_button.cget("fg_color")
    target = COLOR_ACCENT_HOVER if current == COLOR_ACCENT else COLOR_ACCENT
    search_button.configure(fg_color=target)
    app.after(950, breathe_cta)


# =======================================================
# Fonctions de l'Interface Utilisateur
# =======================================================

is_loading = False


def set_loading(loading):
    """Active/désactive l'état de chargement (Hyperkit : retour instantané)."""
    global is_loading
    is_loading = loading
    if loading:
        search_button.configure(state="disabled", text="Recherche…")
        city_entry.configure(state="disabled")
        progress_bar.pack(fill="x", padx=SPACE_LG, pady=(0, SPACE_SM))
        progress_bar.start()
    else:
        progress_bar.stop()
        progress_bar.pack_forget()
        search_button.configure(state="normal", text="Rechercher")
        city_entry.configure(state="normal")


def update_weather_display(weather_data):
    """Met à jour les labels de l'interface avec les données météo."""
    if "erreur" in weather_data:
        messagebox.showerror("Erreur Météo", weather_data['erreur'])
        city_country_label.configure(text="")
        weather_icon_label.configure(image=None, text="")
        description_label.configure(text="")
        temperature_label.configure(text="")
        stats_grid.pack_forget()
        return

    city_country_label.configure(text=f"{weather_data['ville']}, {weather_data['pays']}")
    description_label.configure(text=weather_data['description'].capitalize())
    temperature_label.configure(text=weather_data['temperature'])

    icon_image = get_weather_icon(weather_data['icone_code'])
    if icon_image:
        weather_icon_label.configure(image=icon_image, text="")
    else:
        weather_icon_label.configure(text="—", image=None)

    humidite_value.configure(text=weather_data['humidite'])
    vent_value.configure(text=weather_data['vent'])
    pression_value.configure(text=weather_data['pression'])
    soleil_value.configure(text=f"{weather_data['lever_soleil']} → {weather_data['coucher_soleil']}")

    stats_grid.pack_forget()
    animate_reveal(stats_grid)
    stats_grid.pack(fill="x", padx=SPACE_LG, pady=(SPACE_SM, SPACE_SM))
    pulse_text_color(temperature_label, COLOR_ACCENT, ("#1A1A1A", "#F5F6FA"))


def fetch_and_update(city):
    """Exécuté dans un thread pour ne jamais bloquer l'interface."""
    weather_data = get_weather_data(city)

    def apply():
        set_loading(False)
        update_weather_display(weather_data)

    app.after(0, apply)


def search_weather():
    """Fonction appelée par le bouton pour lancer la recherche météo."""
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Attention", "Veuillez entrer le nom d'une ville.")
        return
    if is_loading:
        return

    set_loading(True)
    threading.Thread(target=fetch_and_update, args=(city,), daemon=True).start()


def toggle_theme():
    """Bascule entre le mode clair et le mode sombre."""
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        theme_button.configure(text="🌙")
    else:
        ctk.set_appearance_mode("Dark")
        theme_button.configure(text="☀️")


def make_stat_card(parent, caption):
    card = ctk.CTkFrame(parent, corner_radius=RADIUS_CONTROL, fg_color=COLOR_CARD_ALT)
    ctk.CTkLabel(
        card, text=caption.upper(), font=font(11, "bold"), text_color=COLOR_TEXT_MUTED
    ).pack(anchor="w", padx=SPACE_MD, pady=(SPACE_SM, 0))
    value_label = ctk.CTkLabel(card, text="—", font=font(18, "bold"))
    value_label.pack(anchor="w", padx=SPACE_MD, pady=(0, SPACE_SM))
    return card, value_label


# =======================================================
# Configuration de l'Interface CustomTkinter
# =======================================================

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Météo en Direct")
app.geometry("480x760")
app.minsize(420, 680)
app.configure(fg_color=COLOR_BG)

# --- Zone header : titre + bascule de thème (Neuropath Edge) ---
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(fill="x", padx=SPACE_LG, pady=(SPACE_LG, SPACE_SM))

ctk.CTkLabel(
    header_frame, text="Météo en direct", font=font(20, "bold")
).pack(side="left")

theme_button = ctk.CTkButton(
    header_frame, text="☀️", width=36, height=36, corner_radius=RADIUS_CONTROL,
    fg_color=COLOR_CARD, hover_color=COLOR_CARD_ALT, text_color=("#1A1A1A", "#F5F6FA"),
    command=toggle_theme,
)
theme_button.pack(side="right")

# --- Zone recherche ---
search_card = ctk.CTkFrame(app, corner_radius=RADIUS_CARD, fg_color=COLOR_CARD)
search_card.pack(fill="x", padx=SPACE_LG, pady=SPACE_SM)

search_row = ctk.CTkFrame(search_card, fg_color="transparent")
search_row.pack(fill="x", padx=SPACE_SM, pady=SPACE_SM)

city_entry = ctk.CTkEntry(
    search_row, placeholder_text="Entrez le nom d'une ville…",
    height=40, corner_radius=RADIUS_CONTROL, font=font(14),
)
city_entry.pack(side="left", fill="x", expand=True, padx=(SPACE_XS, SPACE_SM))
city_entry.bind("<Return>", lambda _event: search_weather())

search_button = ctk.CTkButton(
    search_row, text="Rechercher", width=110, height=40, corner_radius=RADIUS_CONTROL,
    fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, font=font(14, "bold"),
    command=search_weather,
)
search_button.pack(side="left")

progress_bar = ctk.CTkProgressBar(app, mode="indeterminate", height=4, progress_color=COLOR_ACCENT)

# --- Zone résultat hero ---
hero_card = ctk.CTkFrame(app, corner_radius=RADIUS_CARD, fg_color=COLOR_CARD)
hero_card.pack(fill="x", padx=SPACE_LG, pady=SPACE_SM)

city_country_label = ctk.CTkLabel(hero_card, text="", font=font(18, "bold"))
city_country_label.pack(pady=(SPACE_LG, SPACE_XS))

weather_icon_label = ctk.CTkLabel(hero_card, text="", image=None)
weather_icon_label.pack(pady=SPACE_XS)

temperature_label = ctk.CTkLabel(hero_card, text="", font=font(56, "bold"))
temperature_label.pack(pady=SPACE_XS)

description_label = ctk.CTkLabel(hero_card, text="", font=font(15), text_color=COLOR_TEXT_MUTED)
description_label.pack(pady=(0, SPACE_LG))

# --- Zone détails : grille de stats (Ultra Design : cartes alignées) ---
stats_grid = ctk.CTkFrame(app, fg_color="transparent")
stats_grid.grid_columnconfigure((0, 1), weight=1, uniform="stats")

humidite_card, humidite_value = make_stat_card(stats_grid, "Humidité")
vent_card, vent_value = make_stat_card(stats_grid, "Vent")
pression_card, pression_value = make_stat_card(stats_grid, "Pression")
soleil_card, soleil_value = make_stat_card(stats_grid, "Lever · Coucher")

humidite_card.grid(row=0, column=0, sticky="nsew", padx=(0, SPACE_XS), pady=(0, SPACE_XS))
vent_card.grid(row=0, column=1, sticky="nsew", padx=(SPACE_XS, 0), pady=(0, SPACE_XS))
pression_card.grid(row=1, column=0, sticky="nsew", padx=(0, SPACE_XS))
soleil_card.grid(row=1, column=1, sticky="nsew", padx=(SPACE_XS, 0))

# La grille de stats n'est affichée qu'après une recherche réussie
stats_grid.pack_forget()

# Démarre la respiration du bouton d'appel à l'action
app.after(950, breathe_cta)

city_entry.focus()

# Lancement de la boucle principale de l'interface graphique
app.mainloop()

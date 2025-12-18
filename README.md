☀️ Application Météo Python (GUI)

Ce projet est une application de bureau simple développée en Python qui permet aux utilisateurs de consulter la météo en temps réel pour n'importe quelle ville, en utilisant une interface graphique conviviale.

✨ Fonctionnalités

* **Saisie Géographique :** Permet à l'utilisateur de saisir le nom d'une ville.
* **Récupération de Données :** Interroge une API météo externe (OpenWeatherMap) pour obtenir les données.
* **Affichage :** Affiche la température, la description des conditions météorologiques et l'humidité.
* **Interface Simple :** Utilise `Tkinter` pour une application légère et portable.

🛠️ Technologies Utilisées

| Rôle | Outil/Bibliothèque | Description |
| :--- | :--- | :--- |
| **Langage** | Python 3.x | Le langage de programmation principal. |
| **Interface Graphique** | `Tkinter` | Bibliothèque standard de Python pour créer l'interface utilisateur. |
| **API Web** | `requests` | Pour effectuer des requêtes HTTP à l'API météo. |
| **Données Météo** | OpenWeatherMap API | Source des données météorologiques en temps réel. |

## 📁 Structure du Dépôt

* `meteo_app.py` : Le fichier principal contenant la logique de l'interface et les appels API.
* `README.md` : Ce fichier de description.

## 🚀 Installation et Exécution

### Prérequis

1.  **Clé API :** Obtenez une clé API gratuite auprès d'OpenWeatherMap.
    API_KEY = "VOTRE_CLÉ_API_ICI"
    ```

### Étapes

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/VOTRE_NOM/App-Meteo-Python.git](https://github.com/VOTRE_NOM/App-Meteo-Python.git)
    cd App-Meteo-Python
    ```
2.  **Installer les dépendances :**
    ```bash
    pip install requests
    ```
3.  **Lancer l'application :**
    ```bash
    python meteo_app.py
    ```

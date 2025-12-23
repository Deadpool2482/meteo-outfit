%%writefile weather_api.py
import requests
from config import API_KEY, LANG, WEATHER_ICONS

# Definizione URL
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_icon_name(description):
    """Trova l'icona giusta in base alla descrizione"""
    desc_lower = description.lower()
    for key, icon in WEATHER_ICONS.items():
        if key in desc_lower:
            return icon
    return "weather-cloudy"

def get_current_weather(city):
    """Scarica il meteo attuale"""
    try:
        url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric&lang={LANG}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        desc = data["weather"][0]["description"].capitalize()
        
        return {
            "temp": round(data["main"]["temp"]),
            "desc": desc,
            "humidity": data["main"]["humidity"],
            "icon": get_icon_name(data["weather"][0]["main"])
        }
    except Exception as e:
        print(f"Errore API Meteo: {e}")
        # Rilanciamo l'errore per gestirlo nella UI
        return None

def get_forecast(city):
    """Scarica le previsioni semplificate"""
    try:
        url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric&lang={LANG}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return []

        data = response.json()
        forecast_list = []
        # Prendiamo un dato ogni 8 (circa ogni 24 ore)
        for item in data["list"][::8]: 
            full_date = item["dt_txt"].split(" ")[0]
            parts = full_date.split("-")
            formatted_date = f"{parts[2]}/{parts[1]}"
            
            forecast_list.append({
                "date": formatted_date,
                "temp": round(item["main"]["temp"]),
                "desc": item["weather"][0]["description"],
                "icon": get_icon_name(item["weather"][0]["main"])
            })
        return forecast_list[:4]
    except:
        return []

def calcola_outfit(temp, desc):
    """Decide come vestirsi"""
    desc = desc.lower()
    consiglio = ""
    # Colore RGBA default (bianco)
    colore = (1, 1, 1, 1)

    if any(x in desc for x in ["pioggia", "temporale", "pioviggine"]):
        consiglio += "☔ Porta l'ombrello!\n"
        colore = (0.4, 0.7, 1, 1) # Azzurrino
    elif "neve" in desc:
        consiglio += "❄ Stivali obbligatori!\n"
        colore = (0.8, 0.9, 1, 1) # Ghiaccio
    
    if temp <= 5:
        consiglio += "🥶 Gelo artico: Piumino e sciarpa."
    elif 5 < temp <= 12:
        consiglio += "🧥 Fa freddo: Cappotto pesante."
    elif 12 < temp <= 18:
        consiglio += "😎 Fresco: Giacca leggera o pelle."
    elif 18 < temp <= 25:
        consiglio += "👕 Si sta bene: Felpa o maniche lunghe."
    elif temp > 25:
        consiglio += "🔥 Fa caldo: T-shirt e pantaloncini!"
        colore = (1, 0.6, 0, 1) # Arancio
    
    return consiglio, colore
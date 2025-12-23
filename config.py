%%writefile config.py
# config.py

PROJECT_NAME = "Meteo & Outfit"
DEFAULT_CITY = "Ravenna"
LANG = "it"

# Tua API KEY
API_KEY = "862f07a5aae218347c35c811ba49e831"

# Lista delle città
CITIES = [
    "Roma", "Milano", "Napoli", "Torino", "Palermo", "Genova",
    "Bologna", "Firenze", "Bari", "Catania", "Venezia", "Verona",
    "Messina", "Padova", "Trieste", "Taranto", "Brescia", "Parma",
    "Prato", "Modena", "Reggio Calabria", "Reggio Emilia", "Perugia",
    "Ravenna", "Livorno", "Cagliari", "Foggia", "Rimini", "Salerno", "Ferrara"
]

WEATHER_ICONS = {
    "clear": "weather-sunny",
    "sereno": "weather-sunny",
    "clouds": "weather-cloudy",
    "nubi": "weather-cloudy",
    "nuvol": "weather-cloudy",
    "rain": "weather-pouring",
    "piogg": "weather-pouring",
    "drizzle": "weather-partly-rainy",
    "thunderstorm": "weather-lightning",
    "temporale": "weather-lightning",
    "snow": "weather-snowy",
    "neve": "weather-snowy",
    "mist": "weather-fog",
    "fog": "weather-fog",
    "nebbia": "weather-fog"
}
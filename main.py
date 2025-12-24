import requests

def prendi_meteo(citta):
    # Esempio usando l'API di OpenWeatherMap (serve una chiave API)
    api_key = "862f07a5aae218347c35c811ba49e831"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={api_key}&units=metric&lang=it"
    
    try:
        risposta = requests.get(url)
        dati = risposta.json()
        
        if risposta.status_code == 200:
            temperatura = dati['main']['temp']
            descrizione = dati['weather'][0]['description']
            print(f"A {citta} ci sono {temperatura}°C e il cielo è: {descrizione}")
        else:
            print("Città non trovata o errore nell'API.")
            
    except Exception as e:
        print(f"Errore durante la connessione: {e}")

# Prova a chiamare la funzione
citta_scelta = input("Inserisci il nome di una città: ")
prendi_meteo(citta_scelta)

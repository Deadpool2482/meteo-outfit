from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
import requests
import threading
from kivy.clock import Clock

# --- INTERFACCIA ---
class WeatherTile(MDCard):
    def __init__(self, date, temp, advice, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "10dp"
        self.elevation = 2
        self.radius = [12, ]
        self.md_bg_color = [1, 1, 1, 1] 
        
        self.add_widget(MDLabel(text=date, bold=True, halign="center", font_style="Caption"))
        self.add_widget(MDLabel(text=f"{temp}°C", halign="center", font_style="H5", theme_text_color="Primary"))
        self.add_widget(MDLabel(text=advice, halign="center", font_style="Caption", theme_text_color="Secondary"))

class MeteoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing="10dp")
        
        # Toolbar
        layout.add_widget(MDTopAppBar(title="Meteo Outfit"))
        
        # Griglia
        self.grid = MDGridLayout(cols=2, spacing="15dp", padding="15dp")
        layout.add_widget(self.grid)
        
        # Bottone
        layout.add_widget(MDRaisedButton(
            text="AGGIORNA DATI",
            pos_hint={"center_x": .5},
            on_release=self.start_fetch,
            size_hint=(0.9, None),
            height="50dp"
        ))
        
        layout.add_widget(MDBoxLayout(size_hint_y=None, height="20dp"))
        self.add_widget(layout)

    def get_advice(self, t):
        if t < 12: return "Cappotto"
        if t < 20: return "Giacca"
        if t < 26: return "T-shirt"
        return "Leggero"

    def start_fetch(self, *args):
        self.grid.clear_widgets()
        self.grid.add_widget(MDLabel(text="Caricamento...", halign="center"))
        # Scarica in background per non bloccare l'app
        threading.Thread(target=self.fetch_weather).start()

    def fetch_weather(self):
        url = "https://api.open-meteo.com/v1/forecast?latitude=45.46&longitude=9.18&daily=temperature_2m_max&timezone=auto"
        try:
            r = requests.get(url, timeout=10).json()
            temps = r['daily']['temperature_2m_max']
            dates = r['daily']['time']
            # Aggiorna la grafica nel thread principale
            Clock.schedule_once(lambda dt: self.update_ui(dates, temps))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)))

    def update_ui(self, dates, temps, *args):
        self.grid.clear_widgets()
        for i in range(6):
            day = "OGGI" if i == 0 else dates[i][5:]
            self.grid.add_widget(WeatherTile(day, temps[i], self.get_advice(temps[i])))

    def show_error(self, error_msg, *args):
        self.grid.clear_widgets()
        self.grid.add_widget(MDLabel(text="Errore connessione", halign="center"))

class MeteoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return MeteoScreen()

if __name__ == "__main__":
    MeteoApp().run()

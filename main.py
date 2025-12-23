import os

# --- FIX OPENGL 2.0 ---
# Queste righe risolvono l'errore "OpenGL 2.0" su molti PC Windows
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.config import Config
# Configurazione finestra per test su PC (simula smartphone)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'multisamples', '0') # Aiuta con schede video vecchie

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
import requests

# --- LOGICA DELLE SCHEDE METEO ---
class WeatherCard(MDCard):
    def __init__(self, date, temp, advice, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "10dp"
        self.size_hint = (0.9, None)
        self.height = "130dp"
        self.elevation = 2
        self.radius = [15, ]
        self.pos_hint = {"center_x": .5}
        
        self.add_widget(MDLabel(text=date, bold=True, halign="center", font_style="Caption"))
        self.add_widget(MDLabel(text=f"{temp}°C", halign="center", font_style="H5", theme_text_color="Primary"))
        self.add_widget(MDLabel(text=advice, halign="center", theme_text_color="Secondary", font_style="Body2"))

# --- INTERFACCIA PRINCIPALE ---
class MeteoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        
        # Barra superiore
        layout.add_widget(MDTopAppBar(title="Meteo & Outfit"))
        
        # Area scorrevole per i giorni
        self.scroll = MDScrollView()
        self.card_container = MDBoxLayout(orientation='vertical', spacing="15dp", padding="15dp", size_hint_y=None)
        self.card_container.bind(minimum_height=self.card_container.setter('height'))
        
        self.scroll.add_widget(self.card_container)
        layout.add_widget(self.scroll)
        
        # Bottone Aggiorna
        layout.add_widget(MDRaisedButton(
            text="CONTROLLA OUTFIT",
            pos_hint={"center_x": .5},
            on_release=self.fetch_weather,
            size_hint=(0.9, None),
            height="50dp"
        ))
        
        layout.add_widget(MDBoxLayout(size_hint_y=None, height="10dp"))
        self.add_widget(layout)

    def get_clothing_advice(self, t):
        if t < 10: return "Gelo: Cappotto e Sciarpa 🧣"
        if t < 18: return "Fresco: Giacca o Maglione 🧥"
        if t < 25: return "Mite: T-shirt e Jeans 👕"
        return "Caldo: Vestiti Leggeri 😎"

    def fetch_weather(self, *args):
        self.card_container.clear_widgets()
        url = "https://api.open-meteo.com/v1/forecast?latitude=45.46&longitude=9.18&daily=temperature_2m_max&timezone=auto"
        try:
            r = requests.get(url, timeout=5).json()
            dates = r['daily']['time']
            temps = r['daily']['temperature_2m_max']
            
            for i in range(6): 
                day_label = "OGGI" if i == 0 else dates[i]
                advice = self.get_clothing_advice(temps[i])
                self.card_container.add_widget(WeatherCard(day_label, temps[i], advice))
        except Exception:
            self.card_container.add_widget(MDLabel(text="Controlla la connessione!", halign="center"))

class MeteoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.theme_style = "Light"
        return MeteoScreen()

if __name__ == "__main__":
    MeteoApp().run()
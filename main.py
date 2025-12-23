import os
# Fix per la grafica
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.image import Image # Per l'immagine statica
import requests

class WeatherTile(MDCard):
    def __init__(self, date, temp, advice, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "10dp"
        self.elevation = 1
        self.radius = [12, ]
        # Rendiamo le tessere leggermente trasparenti (0.85) per vedere lo sfondo
        self.md_bg_color = [1, 1, 1, 0.85]
        
        self.add_widget(MDLabel(text=date, bold=True, halign="center", font_style="Caption"))
        self.add_widget(MDLabel(text=f"{temp}°C", halign="center", font_style="H6", theme_text_color="Primary"))
        self.add_widget(MDLabel(text=advice, halign="center", font_style="Caption", theme_text_color="Secondary"))

class MeteoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. IMMAGINE DI SFONDO STATICA
        # Puoi usare un link a un'immagine online o un file locale 'sfondo.jpg'
        self.add_widget(Image(
            source='https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=500', 
            allow_stretch=True,
            keep_ratio=False
        ))

        # 2. LAYOUT PRINCIPALE (Sopra lo sfondo)
        layout = MDBoxLayout(orientation='vertical', spacing="10dp")
        
        layout.add_widget(MDTopAppBar(title="Outfit Meteo Static"))
        
        self.grid = MDGridLayout(cols=2, spacing="12dp", padding="12dp")
        layout.add_widget(self.grid)
        
        layout.add_widget(MDRaisedButton(
            text="AGGIORNA METEO",
            pos_hint={"center_x": .5},
            on_release=self.fetch_weather,
            size_hint=(0.9, None),
            height="50dp"
        ))
        layout.add_widget(MDBoxLayout(size_hint_y=None, height="20dp"))
        
        self.add_widget(layout)

    def get_advice(self, t):
        if t < 12: return "Cappotto 🧥"
        if t < 20: return "Giacca 🧥"
        if t < 26: return "T-shirt 👕"
        return "Leggero 😎"

    def fetch_weather(self, *args):
        self.grid.clear_widgets()
        url = "https://api.open-meteo.com/v1/forecast?latitude=45.46&longitude=9.18&daily=temperature_2m_max&timezone=auto"
        try:
            r = requests.get(url, timeout=5).json()
            temps = r['daily']['temperature_2m_max']
            dates = r['daily']['time']
            for i in range(6):
                day = "OGGI" if i == 0 else dates[i][5:]
                self.grid.add_widget(WeatherTile(day, temps[i], self.get_advice(temps[i])))
        except:
            self.grid.add_widget(MDLabel(text="Errore Rete", halign="center"))

class MeteoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        return MeteoScreen()

if __name__ == "__main__":
    MeteoApp().run()

%%writefile main.py
import threading
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineAvatarListItem, ImageLeftWidget
from kivy.metrics import dp
from kivy.clock import Clock

from weather_api import get_current_weather, get_forecast, calcola_outfit
from config import CITIES, DEFAULT_CITY, PROJECT_NAME

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Teal"
        
        screen = MDScreen()
        scroll = MDScrollView()
        
        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=None,
            pos_hint={"top": 1}
        )
        layout.bind(minimum_height=layout.setter('height'))

        # Titolo
        title = MDLabel(
            text="🌤 Meteo & Outfit",
            halign="center",
            font_style="H4",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)

        # Input Città
        self.city_input = MDTextField(
            text=DEFAULT_CITY,
            hint_text="Cerca città...",
            mode="rectangle",
            icon_right="magnify",
            size_hint_y=None,
            height=dp(60)
        )
        layout.add_widget(self.city_input)

        # Bottone Aggiorna
        btn_refresh = MDFillRoundFlatIconButton(
            text="Aggiorna Meteo",
            icon="weather-partly-cloudy",
            pos_hint={"center_x": 0.5},
            on_release=self.start_weather_update
        )
        layout.add_widget(btn_refresh)

        # Spinner
        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(46), dp(46)),
            pos_hint={'center_x': .5},
            active=False
        )
        layout.add_widget(self.spinner)

        # Card Meteo Attuale
        self.weather_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(150),
            radius=[15],
            elevation=4
        )
        
        self.lbl_temp = MDLabel(
            text="--°",
            halign="center",
            font_style="H2",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        self.lbl_desc = MDLabel(
            text="In attesa...",
            halign="center",
            font_style="Subtitle1"
        )
        self.icon_weather = MDFillRoundFlatIconButton(
            text="Condizione",
            icon="weather-cloudy",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0, 0, 0, 0)
        )
        
        self.weather_card.add_widget(self.icon_weather)
        self.weather_card.add_widget(self.lbl_temp)
        self.weather_card.add_widget(self.lbl_desc)
        layout.add_widget(self.weather_card)

        # Card Outfit Consigliato
        outfit_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            size_hint_y=None,
            height=dp(120),
            radius=[15],
            md_bg_color=(0.2, 0.2, 0.2, 1)
        )
        outfit_title = MDLabel(text="👗 Outfit Consigliato", font_style="H6")
        
        self.lbl_outfit_text = MDLabel(
            text="--", 
            font_style="Body1",
            theme_text_color="Custom", # Abilita colore personalizzato
            text_color=(1, 1, 1, 1)
        )
        
        outfit_card.add_widget(outfit_title)
        outfit_card.add_widget(self.lbl_outfit_text)
        layout.add_widget(outfit_card)

        # Lista Previsioni
        layout.add_widget(MDLabel(text="📅 Prossimi giorni:", font_style="H6", size_hint_y=None, height=dp(30)))
        
        self.forecast_list_container = MDList()
        layout.add_widget(self.forecast_list_container)

        scroll.add_widget(layout)
        screen.add_widget(scroll)

        return screen

    def start_weather_update(self, instance):
        self.spinner.active = True
        city = self.city_input.text
        threading.Thread(target=self.fetch_weather_thread, args=(city,)).start()

    def fetch_weather_thread(self, city):
        try:
            now = get_current_weather(city)
            forecast = get_forecast(city)
            
            temp = now['temp'] if now else 20
            desc = now['desc'] if now else ''
            consiglio_text, consiglio_color = calcola_outfit(temp, desc)
            
            Clock.schedule_once(
                lambda dt: self.update_ui(now, forecast, consiglio_text, consiglio_color)
            )
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)))

    def update_ui(self, now, forecast, consiglio_text, consiglio_color):
        if now:
            self.lbl_temp.text = f"{now['temp']}°"
            self.lbl_desc.text = f"{now['desc']} • 💧 {now['humidity']}%"
            self.icon_weather.icon = now['icon']
        
        self.lbl_outfit_text.text = consiglio_text
        self.lbl_outfit_text.text_color = consiglio_color # Applica il colore

        self.forecast_list_container.clear_widgets()
        if forecast:
            for f in forecast:
                item = TwoLineAvatarListItem(
                    text=f"{f['date']} - {f['temp']}°C",
                    secondary_text=f"{f['desc']}",
                )
                icon = ImageLeftWidget(icon=f['icon'])
                item.add_widget(icon)
                self.forecast_list_container.add_widget(item)

        self.reset_loading()

    def show_error(self, error_msg):
        self.lbl_desc.text = "❌ Errore"
        self.lbl_outfit_text.text = "Controlla internet"
        print(f"DEBUG ERROR: {error_msg}")
        self.reset_loading()

    def reset_loading(self):
        self.spinner.active = False

if __name__ == "__main__":
    WeatherApp().run()
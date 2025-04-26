import os
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
import asyncio
import websockets
import threading

# === Carica configurazione dinamica ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

# Imposta dimensione finestra
Window.size = (config.get("window_width", 1280), config.get("window_height", 800))
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Sfondo scuro

class CallCard(BoxLayout):
    def __init__(self, message, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, size_hint_y=None, height=150, **kwargs)
        self.message = message
        self.timer = 0

        self.label = Label(text=message, font_size=24, color=(1, 1, 1, 1))
        self.timer_label = Label(text="00:00", font_size=18, color=(0.7, 0.7, 0.7, 1))

        self.confirm_button = Button(text="✅ Conferma", size_hint=(1, None), height=50)
        self.confirm_button.bind(on_release=self.confirm)

        self.add_widget(self.label)
        self.add_widget(self.timer_label)
        self.add_widget(self.confirm_button)

        self.event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer += 1
        mins, secs = divmod(self.timer, 60)
        self.timer_label.text = f"{mins:02}:{secs:02}"

        if self.timer >= 30:
            self.label.color = (1, 0.5, 0.5, 1)  # Cambia colore dopo 30 secondi

    def confirm(self, instance):
        Clock.unschedule(self.event)
        self.parent.remove_widget(self)

class Dashboard(App):
    def build(self):
        self.layout = GridLayout(cols=1, spacing=20, size_hint_y=None, padding=20)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        root = ScrollView()
        root.add_widget(self.layout)

        # Audio di notifica
        self.alert_sound = SoundLoader.load("https://waiter.fedebosetti.com/static/notification.mp3")
        if not self.alert_sound:
            print("⚠️ Suono notifica non trovato!")

        threading.Thread(target=self.start_websocket_loop, daemon=True).start()

        return root

    def add_card(self, message):
        card = CallCard(message)
        self.layout.add_widget(card)

        # Suona notifica
        if self.alert_sound:
            self.alert_sound.play()

    async def websocket_handler(self):
        ws_url = config.get("ws_url")
        while True:
            try:
                async with websockets.connect(ws_url) as websocket:
                    print(f"✅ Connesso a {ws_url}")
                    while True:
                        message = await websocket.recv()
                        print(f"📩 Ricevuto: {message}")
                        Clock.schedule_once(lambda dt: self.add_card(message))
            except Exception as e:
                print(f"❌ Errore WebSocket: {e}")
                await asyncio.sleep(5)  # Riprova dopo 5 secondi

    def start_websocket_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.websocket_handler())

if __name__ == "__main__":
    Dashboard().run()

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from datetime import datetime
import json
import os

Window.clearcolor = (0.95, 0.95, 0.95, 1)

FILE = "decisions.json"


class HomeScreen(Screen):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation="vertical", padding=40, spacing=30)

        layout.add_widget(Label(
            text="PocketUmpire",
            font_size=32,
            color=(0, 0, 0, 1)
        ))

        btn = Button(text="Start Match", font_size=22, size_hint=(1, 0.3))
        btn.bind(on_press=lambda x: setattr(self.manager, "current", "match"))

        layout.add_widget(btn)
        self.add_widget(layout)


class MatchScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.decisions = self.load_decisions()

        root = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.stats = Label(font_size=16, color=(0,0,0,1), size_hint=(1, 0.15))
        self.update_stats()

        btn_row = BoxLayout(size_hint=(1, 0.2), spacing=10)

        out_btn = Button(text="OUT", background_color=(1,0,0,1))
        out_btn.bind(on_press=lambda x: self.add_decision("OUT"))

        notout_btn = Button(text="NOT OUT", background_color=(0,0.7,0,1))
        notout_btn.bind(on_press=lambda x: self.add_decision("NOT OUT"))

        reset_btn = Button(text="RESET MATCH", background_color=(0.5,0.5,0.5,1))
        reset_btn.bind(on_press=self.reset_match)

        btn_row.add_widget(out_btn)
        btn_row.add_widget(notout_btn)
        btn_row.add_widget(reset_btn)

        self.log_layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        self.log_layout.bind(minimum_height=self.log_layout.setter("height"))

        for d in self.decisions:
            self.log_layout.add_widget(Label(text=d, size_hint_y=None, height=40, color=(0,0,0,1)))

        scroll = ScrollView()
        scroll.add_widget(self.log_layout)

        root.add_widget(self.stats)
        root.add_widget(btn_row)
        root.add_widget(scroll)

        self.add_widget(root)

    def update_stats(self):
        total = len(self.decisions)
        outs = sum(1 for d in self.decisions if d.endswith("OUT"))
        notouts = sum(1 for d in self.decisions if "NOT OUT" in d)
        self.stats.text = f"Total: {total} | OUT: {outs} | NOT OUT: {notouts}"

    def add_decision(self, decision):
        time = datetime.now().strftime("%H:%M:%S")
        text = f"{time} - {decision}"
        self.decisions.append(text)
        self.save_decisions()
        self.update_stats()

        lbl = Label(text=text, size_hint_y=None, height=40, color=(0,0,0,1))
        self.log_layout.add_widget(lbl)

    def reset_match(self, *args):
        self.decisions = []
        self.save_decisions()
        self.log_layout.clear_widgets()
        self.update_stats()

    def save_decisions(self):
        with open(FILE, "w") as f:
            json.dump(self.decisions, f)

    def load_decisions(self):
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                return json.load(f)
        return []


class PocketUmpireApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(MatchScreen(name="match"))
        Clock.schedule_once(lambda dt: setattr(sm, "current", "home"), 0.1)
        return sm


if __name__ == "__main__":
    PocketUmpireApp().run()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class BottomNav(BoxLayout):

    def go_home(self):
        App.get_running_app().root.current = "home"

    def go_history(self):
        App.get_running_app().root.current = "history"

    def go_analytics(self):
        App.get_running_app().root.current = "analytics"

    def go_settings(self):
        App.get_running_app().root.current = "settings"
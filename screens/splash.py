from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class SplashScreen(Screen):

    def on_enter(self):
        """
        Called automatically when this screen becomes visible.
        """
        Clock.schedule_once(self.go_to_welcome, 2)

    def go_to_welcome(self, dt):
        """
        Switch to the Welcome screen after 2 seconds.
        """
        self.manager.current = "welcome"
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from screens.splash import SplashScreen
from screens.welcome import WelcomeScreen
from screens.choice import ChoiceScreen
from screens.login import LoginScreen
from screens.signup import SignupScreen
class PocketPilot(MDApp):
    def build(self):
        # Load the KV file
        Builder.load_file("kv/splash.kv")
        Builder.load_file("kv/welcome.kv")
        Builder.load_file("kv/choice.kv")
        Builder.load_file("kv/login.kv")
        Builder.load_file("kv/signup.kv")

        self.title = "PocketPilot"

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        screen_manager = ScreenManager()

        screen_manager.add_widget(
            SplashScreen(name="splash")
        
        )
        screen_manager.add_widget(
            WelcomeScreen(name="welcome")
        )
        screen_manager.add_widget(ChoiceScreen(name="choice"))
        screen_manager.add_widget(
        LoginScreen(name="login")
        )
        screen_manager.add_widget(SignupScreen(name="signup"))

        return screen_manager


if __name__ == "__main__":
    PocketPilot().run()
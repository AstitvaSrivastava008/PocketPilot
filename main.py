from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from screens.splash import SplashScreen
from screens.welcome import WelcomeScreen
from screens.choice import ChoiceScreen
from screens.login import LoginScreen
from screens.signup import SignupScreen
from screens.home import HomeScreen
from screens.history import HistoryScreen
from screens.analytics import AnalyticsScreen
from screens.settings import SettingsScreen
from screens.add_transaction import AddTransactionScreen

from database import create_database

from widget.bottom_nav import BottomNav
from widget.transaction_card import TransactionCard
from widget.animated_bar import AnimatedBar

class PocketPilot(MDApp):

    current_user = None

    def build(self):
        # -----------------------------
        # Create Database
        # -----------------------------
        create_database()

        # -----------------------------
        # Load KV Files
        # -----------------------------
        Builder.load_file("kv/splash.kv")
        Builder.load_file("kv/welcome.kv")
        Builder.load_file("kv/choice.kv")
        Builder.load_file("kv/login.kv")
        Builder.load_file("kv/signup.kv")
        Builder.load_file("kv/bottom_nav.kv")

        Builder.load_file("kv/home.kv")

        # Load custom widget BEFORE screens that use it
        Builder.load_file("kv/transaction_card.kv")

        Builder.load_file("kv/history.kv")
        Builder.load_file("kv/analytics.kv")
        Builder.load_file("kv/settings.kv")
        Builder.load_file("kv/add_transaction.kv")

        self.title = "PocketPilot"

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        screen_manager = ScreenManager()

        screen_manager.add_widget(SplashScreen(name="splash"))
        screen_manager.add_widget(WelcomeScreen(name="welcome"))
        screen_manager.add_widget(ChoiceScreen(name="choice"))
        screen_manager.add_widget(LoginScreen(name="login"))
        screen_manager.add_widget(SignupScreen(name="signup"))
        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(HistoryScreen(name="history"))
        screen_manager.add_widget(AnalyticsScreen(name="analytics"))
        screen_manager.add_widget(SettingsScreen(name="settings"))
        screen_manager.add_widget(AddTransactionScreen(name="add_transaction"))

        return screen_manager


if __name__ == "__main__":
    PocketPilot().run()
from kivy.uix.screenmanager import Screen


class WelcomeScreen(Screen):

    def go_to_choice(self):
        self.manager.current = "choice"

    def go_to_login(self):
        self.manager.current = "login"
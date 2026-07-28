from kivy.uix.screenmanager import Screen


class ChoiceScreen(Screen):

    def create_account(self):
        print("Create Account clicked")

    def continue_as_guest(self):
        print("Continue as Guest clicked")

    def login(self):
        self.manager.current = "login"
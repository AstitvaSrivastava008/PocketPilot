from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def login(self):
        print("Login button clicked!")

        email = self.ids.email_input.text
        password = self.ids.password_input.text

        print("Email:", email)
        print("Password:", password)
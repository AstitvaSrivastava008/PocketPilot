from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def login(self):
        print("Login button clicked!")

        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not email:
            print("Please enter your email")

        elif not password:
            print("Please enter your password")

        elif "@" not in email:
            print("Please enter a valid email")

        elif "." not in email:
            print("Please enter a valid email")

        elif len(password) < 8:
            print("Password must be at least 8 characters long")

        else:
            print("Login Successful!")
            print("Email:", email)
            print("Password:", password)
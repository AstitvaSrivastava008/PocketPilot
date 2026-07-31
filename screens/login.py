from kivy.uix.screenmanager import Screen
from database import login_user


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
            user = login_user(email, password)

            if user:
             print("Login Successful!")
             print("Welcome,", user[1])
             self.manager.current = "home"

            else:
                print("Invalid email or password")
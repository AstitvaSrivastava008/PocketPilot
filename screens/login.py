from kivy.uix.screenmanager import Screen
from database import login_user


class LoginScreen(Screen):

    def login(self):

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

                # Get the Home screen
                home_screen = self.manager.get_screen("home")

                # Pass the user's name
                home_screen.user_name = user[1]

                # Open Home Screen
                self.manager.current = "home"

            else:
                print("Invalid email or password")
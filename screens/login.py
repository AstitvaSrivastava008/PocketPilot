from kivy.uix.screenmanager import Screen
from kivy.app import App

from database import (
    login_user,
    get_theme
)


class LoginScreen(Screen):

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):

        # -----------------------------------------
        # Get login details
        # -----------------------------------------

        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        # -----------------------------------------
        # Validate email
        # -----------------------------------------

        if not email:
            print("Please enter your email")
            return

        if not password:
            print("Please enter your password")
            return

        if "@" not in email:
            print("Please enter a valid email")
            return

        if "." not in email:
            print("Please enter a valid email")
            return

        # -----------------------------------------
        # Validate password
        # -----------------------------------------

        if len(password) < 8:
            print("Password must be at least 8 characters long")
            return

        # -----------------------------------------
        # Check login credentials
        # -----------------------------------------

        user = login_user(email, password)

        if not user:
            print("Invalid email or password")
            return

        # -----------------------------------------
        # Login successful
        # -----------------------------------------

        print("Login Successful!")
        print("Welcome,", user[1])

        app = App.get_running_app()

        # -----------------------------------------
        # This is a normal user session
        # -----------------------------------------

        app.is_guest = False

        # -----------------------------------------
        # Store logged-in user
        # -----------------------------------------

        app.current_user = user

        # -----------------------------------------
        # Load user's saved theme
        # -----------------------------------------

        try:

            saved_theme = get_theme(user[0])

            if saved_theme == "Dark":

                app.theme_cls.theme_style = "Dark"

                print("Saved theme loaded: Dark")

            else:

                app.theme_cls.theme_style = "Light"

                print("Saved theme loaded: Light")

        except Exception as error:

            print(
                "Could not load saved theme:",
                error
            )

            # Safe fallback
            app.theme_cls.theme_style = "Light"

        # -----------------------------------------
        # Get Home Screen
        # -----------------------------------------

        home_screen = self.manager.get_screen("home")

        # -----------------------------------------
        # Pass user's name to Home Screen
        # -----------------------------------------

        home_screen.user_name = user[1]

        # -----------------------------------------
        # Refresh dashboard
        # -----------------------------------------

        home_screen.refresh_dashboard()

        # -----------------------------------------
        # Open Home Screen
        # -----------------------------------------

        self.manager.current = "home"

    # =========================================================
    # GO TO SIGNUP
    # =========================================================

    def go_to_signup(self):

        self.manager.current = "signup"
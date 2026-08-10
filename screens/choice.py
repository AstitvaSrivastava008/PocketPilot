from kivy.app import App
from kivy.uix.screenmanager import Screen

from database import start_guest_database


class ChoiceScreen(Screen):

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================

    def create_account(self):
        self.manager.current = "signup"

    # =========================================================
    # CONTINUE AS GUEST
    # =========================================================

    def continue_as_guest(self):

        app = App.get_running_app()

        try:
            # Create a fresh temporary guest database
            guest_user = start_guest_database()

            # Make sure the guest user was created
            if guest_user is None:
                print("Could not create Guest session.")
                return

            # Store guest user in the application
            app.current_user = guest_user

            # Tell the application that this is a guest session
            app.is_guest = True

            print("Guest Mode started successfully.")

            # Get Home screen
            home = self.manager.get_screen("home")

            # Display Guest as the username
            home.user_name = "Guest"

            # Load the empty guest dashboard
            home.refresh_dashboard()

            # Open Home
            self.manager.current = "home"

        except Exception as error:

            print(f"Could not start Guest Mode: {error}")

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):
        self.manager.current = "login"
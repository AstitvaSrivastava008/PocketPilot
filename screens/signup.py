from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from database import add_user


class SignupScreen(Screen):

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================

    def create_account(self):

        name = self.ids.name_input.text.strip()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()
        confirm_password = self.ids.confirm_password_input.text.strip()

        # -----------------------------------------------------
        # Validate Name
        # -----------------------------------------------------

        if not name:

            print("Please enter your full name")
            return

        # -----------------------------------------------------
        # Validate Email
        # -----------------------------------------------------

        if not email:

            print("Please enter your email")
            return

        if "@" not in email:

            print("Please enter a valid email")
            return

        if "." not in email:

            print("Please enter a valid email")
            return

        # -----------------------------------------------------
        # Validate Password
        # -----------------------------------------------------

        if not password:

            print("Please enter your password")
            return

        if len(password) < 8:

            print("Password must be at least 8 characters long")
            return

        # -----------------------------------------------------
        # Validate Confirm Password
        # -----------------------------------------------------

        if not confirm_password:

            print("Please confirm your password")
            return

        if password != confirm_password:

            print("Passwords do not match")
            return

        # =====================================================
        # CREATE ACCOUNT
        # =====================================================

        print("Validation Successful!")

        add_user(
            name,
            email,
            password
        )

        # =====================================================
        # SUCCESS POPUP
        # =====================================================

        layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=20
        )

        message = Label(
            text=(
                "Successfully signed up!\n\n"
                "Click the button below to go to Login."
            ),
            halign="center",
            valign="middle"
        )

        login_button = Button(
            text="Go to Login",
            size_hint_y=None,
            height=50
        )

        layout.add_widget(message)
        layout.add_widget(login_button)

        popup = Popup(
            title="Account Created",
            content=layout,
            size_hint=(0.80, 0.40),
            auto_dismiss=False
        )

        # -----------------------------------------------------
        # Go to Login
        # -----------------------------------------------------

        def go_to_login(instance):

            popup.dismiss()

            # Clear signup fields
            self.ids.name_input.text = ""
            self.ids.email_input.text = ""
            self.ids.password_input.text = ""
            self.ids.confirm_password_input.text = ""

            # Open Login screen
            self.manager.current = "login"

        login_button.bind(
            on_release=go_to_login
        )

        popup.open()
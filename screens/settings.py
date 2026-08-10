from kivy.uix.screenmanager import Screen
from kivy.app import App

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from database import (
    get_user,
    update_user_name,
    verify_password,
    update_password,
    update_theme,
    get_theme,
    update_currency,
    get_currency
)


class SettingsScreen(Screen):

    # =========================================================
    # SCREEN ENTER
    # =========================================================

    def on_pre_enter(self):
        pass

    # =========================================================
    # EDIT PROFILE
    # =========================================================

    def edit_profile(self):

        app = App.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user[0]
        user = get_user(user_id)

        if user is None:
            return

        layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=20
        )

        name_input = TextInput(
            text=user[1],
            multiline=False,
            hint_text="Name"
        )

        email_input = TextInput(
            text=user[2],
            multiline=False,
            readonly=True
        )

        save_button = Button(
            text="Save Changes",
            size_hint_y=None,
            height=50
        )

        layout.add_widget(
            Label(text="Name")
        )

        layout.add_widget(
            name_input
        )

        layout.add_widget(
            Label(text="Email")
        )

        layout.add_widget(
            email_input
        )

        layout.add_widget(
            save_button
        )

        popup = Popup(
            title="Edit Profile",
            content=layout,
            size_hint=(0.85, 0.65)
        )

        def save(instance):

            new_name = name_input.text.strip()

            if not new_name:
                return

            update_user_name(
                user_id,
                new_name
            )

            app.current_user = (
                user_id,
                new_name,
                user[2]
            )

            try:

                self.manager.get_screen(
                    "home"
                ).user_name = new_name

            except Exception:
                pass

            popup.dismiss()

        save_button.bind(
            on_release=save
        )

        popup.open()

    # =========================================================
    # CHANGE PASSWORD
    # =========================================================

    def change_password(self):

        app = App.get_running_app()
        # ==========================================
        # GUEST USERS DO NOT HAVE A PASSWORD
        # ==========================================

        if app.is_guest:
            return

        # ==========================================
        # CHECK LOGGED-IN USER
        # ==========================================

        if app.current_user is None:
            return

        user_id = app.current_user[0]

        layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=20
        )

        current = TextInput(
            hint_text="Current Password",
            password=True,
            multiline=False
        )

        new = TextInput(
            hint_text="New Password",
            password=True,
            multiline=False
        )

        confirm = TextInput(
            hint_text="Confirm New Password",
            password=True,
            multiline=False
        )

        message = Label(
            text="",
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=30
        )

        button = Button(
            text="Change Password",
            size_hint_y=None,
            height=50
        )

        layout.add_widget(current)
        layout.add_widget(new)
        layout.add_widget(confirm)
        layout.add_widget(message)
        layout.add_widget(button)

        popup = Popup(
            title="Change Password",
            content=layout,
            size_hint=(0.85, 0.70)
        )

        def save(instance):

            if not verify_password(
                user_id,
                current.text
            ):

                message.text = (
                    "Current password is incorrect."
                )

                return

            if not new.text.strip():

                message.text = (
                    "New password cannot be empty."
                )

                return

            if new.text != confirm.text:

                message.text = (
                    "Passwords do not match."
                )

                return

            update_password(
                user_id,
                new.text
            )

            popup.dismiss()

            Popup(
                title="Success",
                content=Label(
                    text="Password changed successfully!"
                ),
                size_hint=(0.7, 0.35)
            ).open()

        button.bind(
            on_release=save
        )

        popup.open()

    # =========================================================
    # CHANGE THEME
    # =========================================================

    def change_theme(self):

        app = App.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user[0]

        layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=20
        )

        current_theme = get_theme(user_id)

        current_label = Label(
            text=f"Current Theme: {current_theme}",
            size_hint_y=None,
            height=40
        )

        layout.add_widget(
            current_label
        )

        light_button = Button(
            text="Light Mode",
            size_hint_y=None,
            height=50
        )

        dark_button = Button(
            text="Dark Mode",
            size_hint_y=None,
            height=50
        )

        layout.add_widget(light_button)
        layout.add_widget(dark_button)

        popup = Popup(
            title="Choose Theme",
            content=layout,
            size_hint=(0.75, 0.45)
        )

        def set_light(instance):

            update_theme(
                user_id,
                "Light"
            )

            app.theme_cls.theme_style = "Light"

            popup.dismiss()

        def set_dark(instance):

            update_theme(
                user_id,
                "Dark"
            )

            app.theme_cls.theme_style = "Dark"

            popup.dismiss()

        light_button.bind(
            on_release=set_light
        )

        dark_button.bind(
            on_release=set_dark
        )

        popup.open()

    # =========================================================
    # CHANGE CURRENCY
    # =========================================================

    def change_currency(self):

        app = App.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user[0]

        # =====================================================
        # CURRENCY LIST
        # =====================================================

        currencies = [
            ("INR", "₹", "Indian Rupee"),
            ("USD", "$", "US Dollar"),
            ("EUR", "€", "Euro"),
            ("GBP", "£", "British Pound"),
            ("JPY", "¥", "Japanese Yen"),
            ("AUD", "A$", "Australian Dollar"),
            ("CAD", "C$", "Canadian Dollar"),
            ("SGD", "S$", "Singapore Dollar")
        ]

        # =====================================================
        # GET CURRENT CURRENCY FROM DATABASE
        # =====================================================

        current_symbol = get_currency(user_id)

        # Find the current currency details
        current_code = "INR"
        current_name = "Indian Rupee"

        for code, symbol, name in currencies:

            if symbol == current_symbol:

                current_code = code
                current_name = name

                break

        # Store current currency in App
        app.currency_code = current_code
        app.currency_symbol = current_symbol
        app.currency_name = current_name

        # =====================================================
        # MAIN POPUP LAYOUT
        # =====================================================

        main_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        # =====================================================
        # CURRENT CURRENCY LABEL
        # =====================================================

        current_label = Label(
            text=(
                f"Current Currency: "
                f"{app.currency_symbol} "
                f"{app.currency_code}"
            ),
            size_hint_y=None,
            height=40,
            font_size="17sp"
        )

        main_layout.add_widget(
            current_label
        )

        # =====================================================
        # SCROLL VIEW
        # =====================================================

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )

        currency_list = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None
        )

        currency_list.bind(
            minimum_height=currency_list.setter(
                "height"
            )
        )

        # =====================================================
        # POPUP
        # =====================================================

        popup = Popup(
            title="Choose Currency",
            content=main_layout,
            size_hint=(0.78, 0.82),
            auto_dismiss=False
        )

        # =====================================================
        # CURRENCY BUTTONS
        # =====================================================

        for code, symbol, name in currencies:

            button = Button(
                text=f"{symbol}  {code}  -  {name}",
                size_hint_y=None,
                height=52,
                background_normal="",
                color=(1, 1, 1, 1)
            )

            # -------------------------------------------------
            # BUTTON COLOUR
            # -------------------------------------------------

            if app.theme_cls.theme_style == "Dark":

                button.background_color = (
                    0.25,
                    0.25,
                    0.25,
                    1
                )

            else:

                button.background_color = (
                    0.40,
                    0.40,
                    0.40,
                    1
                )

            # -------------------------------------------------
            # CURRENCY SELECTION
            # -------------------------------------------------

            def select_currency(
                instance,
                selected_code=code,
                selected_symbol=symbol,
                selected_name=name
            ):

                # =============================================
                # SAVE TO DATABASE
                # =============================================

                update_currency(
                    user_id,
                    selected_symbol
                )

                # =============================================
                # SAVE TO APP
                # =============================================

                app.currency_code = selected_code
                app.currency_symbol = selected_symbol
                app.currency_name = selected_name

                # =============================================
                # UPDATE POPUP LABEL
                # =============================================

                current_label.text = (
                    f"Current Currency: "
                    f"{selected_symbol} "
                    f"{selected_code}"
                )

                # =============================================
                # TERMINAL MESSAGE
                # =============================================

                print(
                    "Currency changed successfully to: "
                    f"{selected_name} "
                    f"({selected_code})"
                )

                # =============================================
                # CLOSE POPUP
                # =============================================

                popup.dismiss()

                # =============================================
                # REFRESH HOME
                # =============================================

                try:

                    home = self.manager.get_screen(
                        "home"
                    )

                    home.refresh_dashboard()

                except Exception:
                    pass

                # =============================================
                # REFRESH HISTORY
                # =============================================

                try:

                    history = self.manager.get_screen(
                        "history"
                    )

                    history.load_transactions()

                except Exception:
                    pass

                # =============================================
                # REFRESH ANALYTICS
                # =============================================

                try:

                    analytics = self.manager.get_screen(
                        "analytics"
                    )

                    analytics.load_analytics()

                except Exception:
                    pass

            button.bind(
                on_release=select_currency
            )

            currency_list.add_widget(
                button
            )

        # =====================================================
        # ADD SCROLL VIEW
        # =====================================================

        scroll.add_widget(
            currency_list
        )

        main_layout.add_widget(
            scroll
        )

        # =====================================================
        # CANCEL BUTTON
        # =====================================================

        cancel_button = Button(
            text="Cancel",
            size_hint_y=None,
            height=50,
            background_normal="",
            background_color=(
                0.35,
                0.35,
                0.35,
                1
            ),
            color=(1, 1, 1, 1)
        )

        cancel_button.bind(
            on_release=popup.dismiss
        )

        main_layout.add_widget(
            cancel_button
        )

        # =====================================================
        # OPEN POPUP
        # =====================================================

        popup.open()

    # =========================================================
    # ABOUT POCKETPILOT
    # =========================================================

    def about_app(self):

        Popup(
            title="About PocketPilot",
            content=Label(
                text=(
                    "PocketPilot v1.0\n\n"
                    "A Personal Finance Manager\n\n"
                    "Developed by:\n"
                    "Astitva Srivastava\n\n"
                    "© 2026 PocketPilot"
                ),
                halign="center"
            ),
            size_hint=(0.8, 0.5)
        ).open()

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        app = App.get_running_app()

        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=20
        )

        layout.add_widget(
            Label(
                text="Are you sure you want to logout?"
            )
        )

        buttons = BoxLayout(
            spacing=15,
            size_hint_y=None,
            height=50
        )

        yes = Button(
            text="Yes"
        )

        no = Button(
            text="No"
        )

        buttons.add_widget(yes)
        buttons.add_widget(no)

        layout.add_widget(buttons)

        popup = Popup(
            title="Logout",
            content=layout,
            size_hint=(0.7, 0.35)
        )

        def confirm(instance):

            # =====================================================
            # GUEST LOGOUT
            # =====================================================

            if app.is_guest:

                from database import delete_guest_database

                # Delete temporary guest database
                delete_guest_database()

                # Reset guest session
                app.is_guest = False
                app.current_user = None

            # =====================================================
            # NORMAL USER LOGOUT
            # =====================================================

            else:

                app.current_user = None

            popup.dismiss()

            # Return to login screen
            self.manager.current = "login"

        yes.bind(
            on_release=confirm
        )

        no.bind(
            on_release=lambda *_: popup.dismiss()
        )

        popup.open()
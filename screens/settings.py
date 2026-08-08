from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from database import (
    get_user,
    update_user_name,
    verify_password,
    update_password,
    update_theme,
    get_theme
)

class SettingsScreen(Screen):

    def on_pre_enter(self):
        pass

    def edit_profile(self):
        app = App.get_running_app()
        user_id = app.current_user[0]
        user = get_user(user_id)

        layout = BoxLayout(orientation="vertical", spacing=15, padding=20)
        name_input = TextInput(text=user[1], multiline=False, hint_text="Name")
        email_input = TextInput(text=user[2], multiline=False, readonly=True)
        save_button = Button(text="Save Changes", size_hint_y=None, height=50)

        layout.add_widget(Label(text="Name"))
        layout.add_widget(name_input)
        layout.add_widget(Label(text="Email"))
        layout.add_widget(email_input)
        layout.add_widget(save_button)

        popup = Popup(title="Edit Profile", content=layout, size_hint=(0.85,0.65))

        def save(instance):
            if not name_input.text.strip():
                return
            update_user_name(user_id, name_input.text.strip())
            app.current_user = (user_id, name_input.text.strip(), user[2])
            try:
                self.manager.get_screen("home").user_name = name_input.text.strip()
            except Exception:
                pass
            popup.dismiss()

        save_button.bind(on_release=save)
        popup.open()

    def change_password(self):
        app = App.get_running_app()
        user_id = app.current_user[0]
        layout = BoxLayout(orientation="vertical", spacing=15, padding=20)
        current = TextInput(hint_text="Current Password", password=True, multiline=False)
        new = TextInput(hint_text="New Password", password=True, multiline=False)
        confirm = TextInput(hint_text="Confirm New Password", password=True, multiline=False)
        message = Label(text="", color=(1,0,0,1), size_hint_y=None, height=30)
        btn = Button(text="Change Password", size_hint_y=None, height=50)
        for w in (current,new,confirm,message,btn):
            layout.add_widget(w)
        popup=Popup(title="Change Password",content=layout,size_hint=(0.85,0.70))
        def save(instance):
            if not verify_password(user_id,current.text):
                message.text="Current password is incorrect."; return
            if not new.text.strip():
                message.text="New password cannot be empty."; return
            if new.text!=confirm.text:
                message.text="Passwords do not match."; return
            update_password(user_id,new.text)
            popup.dismiss()
            Popup(title="Success",content=Label(text="Password changed successfully!"),size_hint=(0.7,0.35)).open()
        btn.bind(on_release=save)
        popup.open()

    def change_theme(self):
        app=App.get_running_app()
        user_id=app.current_user[0]
        layout=BoxLayout(orientation="vertical",spacing=15,padding=20)
        layout.add_widget(Label(text=f"Current Theme: {get_theme(user_id)}"))
        light=Button(text="☀ Light Mode")
        dark=Button(text="🌙 Dark Mode")
        layout.add_widget(light); layout.add_widget(dark)
        popup=Popup(title="Choose Theme",content=layout,size_hint=(0.75,0.45))
        light.bind(on_release=lambda *_:(setattr(app.theme_cls,"theme_style","Light"),update_theme(user_id,"Light"),popup.dismiss()))
        dark.bind(on_release=lambda *_:(setattr(app.theme_cls,"theme_style","Dark"),update_theme(user_id,"Dark"),popup.dismiss()))
        popup.open()

    def about_app(self):
        Popup(title="About PocketPilot",
              content=Label(text="PocketPilot v1.0\n\nA Personal Finance Manager\n\nDeveloped by:\nAstitva Srivastava\n\n© 2026 PocketPilot",halign="center"),
              size_hint=(0.8,0.5)).open()

    def logout(self):
        layout=BoxLayout(orientation="vertical",spacing=20,padding=20)
        layout.add_widget(Label(text="Are you sure you want to logout?"))
        buttons=BoxLayout(spacing=15,size_hint_y=None,height=50)
        yes=Button(text="Yes"); no=Button(text="No")
        buttons.add_widget(yes); buttons.add_widget(no)
        layout.add_widget(buttons)
        popup=Popup(title="Logout",content=layout,size_hint=(0.7,0.35))
        def confirm(instance):
            App.get_running_app().current_user=None
            popup.dismiss()
            self.manager.current="login"
        yes.bind(on_release=confirm)
        no.bind(on_release=lambda *_: popup.dismiss())
        popup.open()
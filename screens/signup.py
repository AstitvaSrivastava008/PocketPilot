from kivy.uix.screenmanager import Screen


class SignupScreen(Screen):

    def create_account(self):

       name = self.ids.name_input.text.strip()
       email = self.ids.email_input.text.strip()
       password = self.ids.password_input.text.strip()
       confirm_password = self.ids.confirm_password_input.text.strip()

       if not name:
        print("Please enter your full name")

       elif not email:
        print("Please enter your email")

       elif "@" not in email:
        print("Please enter a valid email")

       elif "." not in email:
        print("Please enter a valid email")

       elif not password:
        print("Please enter your password")

       elif len(password) < 8:
        print("Password must be at least 8 characters long")

       elif not confirm_password:
        print("Please confirm your password")

       elif password != confirm_password:
        print("Passwords do not match")

       else:
        print("Validation Successful!")
from kivy.app import App
from kivy.uix.screenmanager import Screen
from datetime import datetime

from database import add_transaction


class AddTransactionScreen(Screen):

    # Default mode
    transaction_mode = "expense"

    income_categories = (
        "Salary",
        "Freelance",
        "Business",
        "Investment",
        "Gift",
        "Other"
    )

    expense_categories = (
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Entertainment",
        "Medical",
        "Education",
        "Other"
    )

    # -----------------------------
    # Screen Opens
    # -----------------------------
    def on_pre_enter(self):

        self.clear_form()

        if self.transaction_mode == "income":

            self.ids.income_toggle.state = "down"
            self.load_income_categories()

        else:

            self.ids.expense_toggle.state = "down"
            self.load_expense_categories()

    # -----------------------------
    # Category Loaders
    # -----------------------------
    def load_income_categories(self):
        self.ids.category_spinner.values = self.income_categories
        self.ids.category_spinner.text = "Select Category"

    def load_expense_categories(self):
        self.ids.category_spinner.values = self.expense_categories
        self.ids.category_spinner.text = "Select Category"

    # -----------------------------
    # Clear Form
    # -----------------------------
    def clear_form(self):

        self.ids.amount_input.text = ""
        self.ids.description_input.text = ""
        self.ids.category_spinner.text = "Select Category"

    # -----------------------------
    # Save Transaction
    # -----------------------------
    def save_transaction(self):

        app = App.get_running_app()

        if app.current_user is None:
            print("No user logged in.")
            return

        user_id = app.current_user[0]

        if self.ids.income_toggle.state == "down":
            transaction_type = "income"
        else:
            transaction_type = "expense"

        amount = self.ids.amount_input.text.strip()
        category = self.ids.category_spinner.text
        description = self.ids.description_input.text.strip()

        date = datetime.now().strftime("%d-%m-%Y")

        # -----------------------------
        # Validation
        # -----------------------------
        if amount == "":
            print("Please enter an amount.")
            return

        if category == "Select Category":
            print("Please select a category.")
            return

        try:
            amount = float(amount)
        except ValueError:
            print("Invalid amount.")
            return

        # -----------------------------
        # Save to Database
        # -----------------------------
        add_transaction(
            user_id,
            transaction_type,
            amount,
            category,
            description,
            date
        )

        print("Transaction Saved Successfully!")

        # -----------------------------
        # Refresh Dashboard
        # -----------------------------
        home_screen = self.manager.get_screen("home")
        home_screen.refresh_dashboard()

        # -----------------------------
        # Clear Form
        # -----------------------------
        self.clear_form()

        # -----------------------------
        # Return Home
        # -----------------------------
        self.manager.current = "home"
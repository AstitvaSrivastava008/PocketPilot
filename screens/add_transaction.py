from kivy.app import App
from kivy.uix.screenmanager import Screen
from datetime import datetime

from database import (
    add_transaction,
    update_transaction
)


class AddTransactionScreen(Screen):

    # =====================================
    # SCREEN MODE
    # =====================================
    edit_mode = False
    editing_transaction_id = None

    # Default Transaction Mode
    transaction_mode = "expense"

    # =====================================
    # CATEGORIES
    # =====================================
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

    # =====================================
    # SCREEN OPENS
    # =====================================
    def on_pre_enter(self):

        # Only clear the form if we're adding a new transaction
        if not self.edit_mode:
            self.clear_form()

        if self.transaction_mode == "income":

            self.ids.expense_toggle.state = "normal"
            self.ids.income_toggle.state = "down"
            self.load_income_categories()

        else:

            self.ids.income_toggle.state = "normal"
            self.ids.expense_toggle.state = "down"
            self.load_expense_categories()

    # =====================================
    # CATEGORY LOADERS
    # =====================================
    def load_income_categories(self):

        self.transaction_mode = "income"

        self.ids.category_spinner.values = self.income_categories

        if not self.edit_mode:
            self.ids.category_spinner.text = "Select Category"

    def load_expense_categories(self):

        self.transaction_mode = "expense"

        self.ids.category_spinner.values = self.expense_categories

        if not self.edit_mode:
            self.ids.category_spinner.text = "Select Category"

    # =====================================
    # CLEAR FORM
    # =====================================
    def clear_form(self):

        self.ids.amount_input.text = ""
        self.ids.description_input.text = ""
        self.ids.category_spinner.text = "Select Category"

    # =====================================
    # LOAD TRANSACTION (USED FOR EDIT)
    # =====================================
    def load_transaction(
            self,
            transaction_id,
            transaction_type,
            amount,
            category,
            description):

        self.edit_mode = True
        self.editing_transaction_id = transaction_id

        if transaction_type == "income":

            self.transaction_mode = "income"

            self.ids.expense_toggle.state = "normal"
            self.ids.income_toggle.state = "down"

            self.load_income_categories()

        else:

            self.transaction_mode = "expense"

            self.ids.income_toggle.state = "normal"
            self.ids.expense_toggle.state = "down"

            self.load_expense_categories()

        self.ids.amount_input.text = str(amount)
        self.ids.category_spinner.text = category
        self.ids.description_input.text = description if description else ""

    # =====================================
    # SAVE / UPDATE TRANSACTION
    # =====================================
    def save_transaction(self):

        app = App.get_running_app()

        if app.current_user is None:
            print("No user logged in.")
            return

        user_id = app.current_user[0]

        # Use transaction_mode instead of toggle state
        transaction_type = self.transaction_mode

        amount = self.ids.amount_input.text.strip()
        category = self.ids.category_spinner.text
        description = self.ids.description_input.text.strip()

        date = datetime.now().strftime("%d-%b-%Y")

        # =============================
        # VALIDATION
        # =============================
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

        # =============================
        # UPDATE MODE
        # =============================
        if self.edit_mode:

            update_transaction(
                self.editing_transaction_id,
                transaction_type,
                amount,
                category,
                description,
                date
            )

            print("Transaction Updated Successfully!")

            self.edit_mode = False
            self.editing_transaction_id = None

        # =============================
        # ADD MODE
        # =============================
        else:

            add_transaction(
                user_id,
                transaction_type,
                amount,
                category,
                description,
                date
            )

            print("Transaction Saved Successfully!")

        # =============================
        # REFRESH HOME
        # =============================
        home_screen = self.manager.get_screen("home")
        home_screen.refresh_dashboard()

        # =============================
        # CLEAR FORM
        # =============================
        self.clear_form()

        # Reset to default expense mode for next new transaction
        self.transaction_mode = "expense"

        # =============================
        # RETURN HOME
        # =============================
        self.manager.current = "home"
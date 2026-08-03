from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from database import (
    get_total_income,
    get_total_expense,
    get_current_balance,
    get_recent_transaction
)


class HomeScreen(Screen):

    user_name = StringProperty("User")

    balance = StringProperty("₹0.00")
    income = StringProperty("₹0.00")
    expense = StringProperty("₹0.00")
    recent_transaction = StringProperty("No transactions yet.")

    def refresh_dashboard(self):

        app = App.get_running_app()

        if not app.current_user:
            return

        user_id = app.current_user[0]

        total_income = get_total_income(user_id)
        total_expense = get_total_expense(user_id)
        balance = get_current_balance(user_id)

        self.income = f"₹{total_income:.2f}"
        self.expense = f"₹{total_expense:.2f}"
        self.balance = f"₹{balance:.2f}"

        self.recent_transaction = get_recent_transaction(user_id)

    # -------------------------
    # Open Income Screen
    # -------------------------
    def open_income(self):

        screen = self.manager.get_screen("add_transaction")

        screen.transaction_mode = "income"

        self.manager.current = "add_transaction"

    # -------------------------
    # Open Expense Screen
    # -------------------------
    def open_expense(self):

        screen = self.manager.get_screen("add_transaction")

        screen.transaction_mode = "expense"

        self.manager.current = "add_transaction"
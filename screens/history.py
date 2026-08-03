from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp

from database import get_all_transactions
from widget.transaction_card import TransactionCard


class HistoryScreen(Screen):

    def on_pre_enter(self):
        self.load_transactions()

    def load_transactions(self):

        app = App.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user[0]

        transactions = get_all_transactions(user_id)

        container = self.ids.transaction_container

        # Remove old cards
        container.clear_widgets()

        if not transactions:
            card = TransactionCard()

            card.category = "No Transactions"
            card.description = "Start adding your expenses!"
            card.date = ""
            card.amount = ""
            card.icon = "information"
            card.amount_color = [0.5, 0.5, 0.5, 1]

            container.add_widget(card)
            return

        for transaction in transactions:

            transaction_type, category, amount, description, date = transaction

            card = TransactionCard()

            card.category = category
            card.description = description if description else "No Description"
            card.date = date

            if transaction_type == "income":
                card.amount = f"+₹{amount:.2f}"
                card.amount_color = [0, 0.7, 0, 1]
                card.icon = "cash"

            else:
                card.amount = f"-₹{amount:.2f}"
                card.amount_color = [0.85, 0, 0, 1]
                card.icon = "credit-cash-minus"

            container.add_widget(card)
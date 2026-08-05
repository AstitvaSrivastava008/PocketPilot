from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from database import (
    get_all_transactions,
    delete_transaction
)

from widget.transaction_card import TransactionCard


class HistoryScreen(Screen):

    dialog = None

    def on_pre_enter(self):
        self.load_transactions()

    # =====================================
    # LOAD ALL TRANSACTIONS
    # =====================================
    def load_transactions(self):

        app = App.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user[0]

        transactions = get_all_transactions(user_id)

        container = self.ids.transaction_container
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

            transaction_id, transaction_type, category, amount, description, date = transaction

            card = TransactionCard()

            card.transaction_id = transaction_id
            card.category = category
            card.description = description if description else ""
            card.date = date

            if transaction_type == "income":
                card.amount = f"+₹{amount:.2f}"
                card.amount_color = [0, 0.7, 0, 1]
                card.icon = "cash"

            else:
                card.amount = f"-₹{amount:.2f}"
                card.amount_color = [0.85, 0, 0, 1]
                card.icon = "credit-card-minus"

            container.add_widget(card)

    # =====================================
    # EDIT TRANSACTION
    # =====================================
    def edit_transaction(self, transaction_id):

        app = App.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user[0]

        transactions = get_all_transactions(user_id)

        for transaction in transactions:

            tid, transaction_type, category, amount, description, date = transaction

            if tid == transaction_id:

                screen = self.manager.get_screen("add_transaction")

                screen.load_transaction(
                    tid,
                    transaction_type,
                    amount,
                    category,
                    description
                )

                self.manager.current = "add_transaction"
                return

    # =====================================
    # DELETE CONFIRMATION
    # =====================================
    def confirm_delete(self, transaction_id):

        self.dialog = MDDialog(
            title="Delete Transaction?",
            text="This transaction will be permanently deleted.",

            buttons=[

                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),

                MDFlatButton(
                    text="DELETE",
                    on_release=lambda x: self.delete_selected_transaction(transaction_id)
                )

            ]
        )

        self.dialog.open()

    # =====================================
    # DELETE TRANSACTION
    # =====================================
    def delete_selected_transaction(self, transaction_id):

        delete_transaction(transaction_id)

        self.dialog.dismiss()

        self.load_transactions()

        home = self.manager.get_screen("home")
        home.refresh_dashboard()

        print("Transaction Deleted Successfully!")
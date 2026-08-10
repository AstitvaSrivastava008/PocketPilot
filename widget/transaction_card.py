from kivy.properties import (
    StringProperty,
    ListProperty,
    NumericProperty
)

from kivymd.uix.card import MDCard


class TransactionCard(MDCard):

    # ==========================================
    # TRANSACTION ID
    # Used for Edit / Delete operations
    # ==========================================
    transaction_id = NumericProperty(0)

    # ==========================================
    # TRANSACTION DETAILS
    # ==========================================
    category = StringProperty("")
    description = StringProperty("")
    date = StringProperty("")
    amount = StringProperty("")

    # Icon displayed on the transaction card
    icon = StringProperty("cash")

    # ==========================================
    # AMOUNT COLOR
    # Green = Income
    # Red = Expense
    # ==========================================
    amount_color = ListProperty([0, 0.7, 0, 1])
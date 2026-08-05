from kivy.properties import (
    StringProperty,
    ListProperty,
    NumericProperty
)
from kivymd.uix.card import MDCard


class TransactionCard(MDCard):

    # Transaction ID (used for Edit/Delete)
    transaction_id = NumericProperty(0)

    # Transaction Details
    category = StringProperty("")
    description = StringProperty("")
    date = StringProperty("")
    amount = StringProperty("")
    icon = StringProperty("cash")

    # Amount color (Green for Income, Red for Expense)
    amount_color = ListProperty([0, 0.7, 0, 1])
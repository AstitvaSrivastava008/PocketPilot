from kivy.properties import (
    StringProperty,
    ListProperty
)
from kivymd.uix.card import MDCard


class TransactionCard(MDCard):

    category = StringProperty("")
    description = StringProperty("")
    date = StringProperty("")
    amount = StringProperty("")
    icon = StringProperty("cash")

    amount_color = ListProperty([0, 0.7, 0, 1])
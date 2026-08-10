from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivy.properties import (
    StringProperty,
    NumericProperty
)

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from database import (
    get_total_income,
    get_total_expense,
    get_current_balance,
    get_recent_transaction,
    get_goal,
    save_goal,
    delete_goal,
    mark_goal_completed,
    get_currency
)


class HomeScreen(Screen):

    # =========================================================
    # USER
    # =========================================================

    user_name = StringProperty("User")

    # =========================================================
    # DASHBOARD VALUES
    # =========================================================

    balance = StringProperty("₹0.00")
    income = StringProperty("₹0.00")
    expense = StringProperty("₹0.00")

    recent_transaction = StringProperty(
        "No transactions yet."
    )

    # =========================================================
    # SAVINGS GOAL
    # =========================================================

    goal_progress = StringProperty(
        "No Goal Set"
    )

    goal_percentage = NumericProperty(0)

    goal_percentage_text = StringProperty(
        "0% Completed"
    )

    goal_remaining = StringProperty(
        "Remaining: ₹0.00"
    )

    # =========================================================
    # CURRENCY HELPER
    # =========================================================

    def get_currency_symbol(self):

        app = App.get_running_app()

        # Try to use the currency already loaded in App
        symbol = getattr(
            app,
            "currency_symbol",
            None
        )

        if symbol:
            return symbol

        # Fallback
        return "₹"

    # =========================================================
    # REFRESH DASHBOARD
    # =========================================================

    def refresh_dashboard(self):

        app = App.get_running_app()

        if not app.current_user:
            return

        user_id = app.current_user[0]

        # -----------------------------------------------------
        # Username
        # -----------------------------------------------------

        self.user_name = app.current_user[1]

        # -----------------------------------------------------
        # Load saved currency from database
        # -----------------------------------------------------

        try:

            currency_symbol = get_currency(
                user_id
            )

            if not currency_symbol:
                currency_symbol = "₹"

        except Exception:

            currency_symbol = "₹"

        # Save currency to App
        app.currency_symbol = currency_symbol

        # -----------------------------------------------------
        # Dashboard values
        # -----------------------------------------------------

        total_income = get_total_income(
            user_id
        )

        total_expense = get_total_expense(
            user_id
        )

        balance = get_current_balance(
            user_id
        )

        # -----------------------------------------------------
        # Display currency
        # -----------------------------------------------------

        self.income = (
            f"{currency_symbol}"
            f"{total_income:,.2f}"
        )

        self.expense = (
            f"{currency_symbol}"
            f"{total_expense:,.2f}"
        )

        self.balance = (
            f"{currency_symbol}"
            f"{balance:,.2f}"
        )

        # -----------------------------------------------------
        # Recent transaction
        # -----------------------------------------------------

        self.recent_transaction = (
            get_recent_transaction(user_id)
        )

        # =====================================================
        # SAVINGS GOAL
        # =====================================================

        goal = get_goal(user_id)

        if goal:

            (
                goal_name,
                goal_amount,
                saved_amount,
                saving_percentage,
                target_date,
                goal_completed
            ) = goal

            # -------------------------------------------------
            # Calculate percentage
            # -------------------------------------------------

            percentage = 0

            if goal_amount > 0:

                percentage = min(
                    (saved_amount / goal_amount) * 100,
                    100
                )

            # -------------------------------------------------
            # Calculate remaining
            # -------------------------------------------------

            remaining = max(
                goal_amount - saved_amount,
                0
            )

            # -------------------------------------------------
            # Goal progress
            # -------------------------------------------------

            self.goal_progress = (
                f"{goal_name}\n"
                f"{currency_symbol}"
                f"{saved_amount:,.2f}"
                f" / "
                f"{currency_symbol}"
                f"{goal_amount:,.2f}"
            )

            # -------------------------------------------------
            # Progress bar
            # -------------------------------------------------

            self.goal_percentage = percentage

            # -------------------------------------------------
            # Percentage text
            # -------------------------------------------------

            self.goal_percentage_text = (
                f"{percentage:.1f}% Completed"
            )

            # -------------------------------------------------
            # Remaining amount
            # -------------------------------------------------

            self.goal_remaining = (
                f"Remaining: "
                f"{currency_symbol}"
                f"{remaining:,.2f}"
            )

            # =================================================
            # GOAL COMPLETED POPUP
            # =================================================

            if (
                goal_amount > 0
                and saved_amount >= goal_amount
                and not goal_completed
            ):

                popup = Popup(
                    title="Congratulations!",

                    content=Label(
                        text=(
                            "You achieved your "
                            "savings goal!\n\n"
                            f"{goal_name}\n"
                            f"{currency_symbol}"
                            f"{goal_amount:,.2f}"
                        ),
                        halign="center"
                    ),

                    size_hint=(0.75, 0.40)
                )

                popup.open()

                mark_goal_completed(
                    user_id
                )

        else:

            # -------------------------------------------------
            # No goal
            # -------------------------------------------------

            self.goal_progress = (
                "No Goal Set"
            )

            self.goal_percentage = 0

            self.goal_percentage_text = (
                "0% Completed"
            )

            self.goal_remaining = (
                f"Remaining: "
                f"{currency_symbol}"
                f"0.00"
            )

    # =========================================================
    # SMART SAVINGS GOAL POPUP
    # =========================================================

    def open_goal_popup(self):

        app = App.get_running_app()

        if not app.current_user:
            return

        user_id = app.current_user[0]

        currency_symbol = (
            self.get_currency_symbol()
        )

        goal = get_goal(user_id)

        # -----------------------------------------------------
        # Layout
        # -----------------------------------------------------

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20
        )

        # -----------------------------------------------------
        # Goal name
        # -----------------------------------------------------

        goal_name = TextInput(
            hint_text="Goal Name (Laptop, Bike...)",
            multiline=False
        )

        # -----------------------------------------------------
        # Goal amount
        # -----------------------------------------------------

        goal_amount = TextInput(
            hint_text=(
                f"Goal Amount "
                f"({currency_symbol})"
            ),
            multiline=False,
            input_filter="float"
        )

        # -----------------------------------------------------
        # Saving percentage
        # -----------------------------------------------------

        saving_percentage = TextInput(
            hint_text="Saving Percentage (%)",
            multiline=False,
            input_filter="float"
        )

        # -----------------------------------------------------
        # Target date
        # -----------------------------------------------------

        target_date = TextInput(
            hint_text="Target Date (Optional)",
            multiline=False
        )

        # =====================================================
        # PRE-FILL EXISTING GOAL
        # =====================================================

        if goal:

            (
                current_name,
                current_goal,
                current_saved,
                current_percentage,
                current_target,
                current_completed
            ) = goal

            goal_name.text = current_name

            goal_amount.text = str(
                current_goal
            )

            saving_percentage.text = str(
                current_percentage
            )

            target_date.text = (
                current_target
                if current_target
                else ""
            )

        # =====================================================
        # SAVE BUTTON
        # =====================================================

        save_button = Button(
            text="Save Goal",
            size_hint_y=None,
            height=50
        )

        # =====================================================
        # DELETE BUTTON
        # =====================================================

        delete_button = Button(
            text="Delete Goal",
            size_hint_y=None,
            height=50,
            background_color=(
                0.85,
                0.20,
                0.20,
                1
            )
        )

        # =====================================================
        # ADD WIDGETS
        # =====================================================

        layout.add_widget(
            goal_name
        )

        layout.add_widget(
            goal_amount
        )

        layout.add_widget(
            saving_percentage
        )

        layout.add_widget(
            target_date
        )

        layout.add_widget(
            save_button
        )

        if goal:
            layout.add_widget(
                delete_button
            )

        # =====================================================
        # POPUP
        # =====================================================

        popup = Popup(
            title="Smart Savings Goal",
            content=layout,
            size_hint=(0.85, 0.75)
        )

        # =====================================================
        # SAVE GOAL
        # =====================================================

        def save(instance):

            if (
                goal_name.text.strip() == ""
                or goal_amount.text.strip() == ""
                or saving_percentage.text.strip() == ""
            ):
                return

            save_goal(
                user_id,
                goal_name.text.strip(),
                float(goal_amount.text),
                float(
                    saving_percentage.text
                ),
                target_date.text.strip()
            )

            popup.dismiss()

            self.refresh_dashboard()

        # =====================================================
        # DELETE GOAL
        # =====================================================

        def delete(instance):

            delete_goal(
                user_id
            )

            popup.dismiss()

            self.refresh_dashboard()

        # =====================================================
        # BUTTON EVENTS
        # =====================================================

        save_button.bind(
            on_release=save
        )

        if goal:

            delete_button.bind(
                on_release=delete
            )

        popup.open()

    # =========================================================
    # OPEN INCOME SCREEN
    # =========================================================

    def open_income(self):

        screen = self.manager.get_screen(
            "add_transaction"
        )

        screen.transaction_mode = "income"

        self.manager.current = (
            "add_transaction"
        )

    # =========================================================
    # OPEN EXPENSE SCREEN
    # =========================================================

    def open_expense(self):

        screen = self.manager.get_screen(
            "add_transaction"
        )

        screen.transaction_mode = "expense"

        self.manager.current = (
            "add_transaction"
        )
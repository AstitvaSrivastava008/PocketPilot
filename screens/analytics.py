from kivy.app import App
from kivy.uix.screenmanager import Screen


from database import (
    get_expense_by_category,
    get_highest_expense_category,
    get_income_vs_expense,
    get_expense_category_count,
    get_balance,
    get_transaction_count
)


from charts import (
    create_expense_pie_chart,
    create_income_expense_chart,
    create_category_bar_chart
)


class AnalyticsScreen(Screen):

    # =========================================================
    # SCREEN ENTER
    # =========================================================

    def on_pre_enter(self):

        self.load_analytics()

    # =========================================================
    # LOAD ANALYTICS
    # =========================================================

    def load_analytics(self):

        app = App.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user[0]

        # =====================================================
        # GET CURRENT CURRENCY
        # =====================================================

        currency_symbol = getattr(
            app,
            "currency_symbol",
            "₹"
        )

        if not currency_symbol:
            currency_symbol = "₹"

        # =====================================================
        # EXPENSE DATA
        # =====================================================

        expense_data = get_expense_by_category(
            user_id
        )

        # =====================================================
        # EXPENSE PIE CHART
        # =====================================================

        create_expense_pie_chart(
            expense_data,
            "assets/expense_chart.png"
        )

        self.ids.expense_chart.source = ""

        self.ids.expense_chart.source = (
            "assets/expense_chart.png"
        )

        self.ids.expense_chart.reload()

        # =====================================================
        # INCOME VS EXPENSE
        # =====================================================

        income, expense = get_income_vs_expense(
            user_id
        )

        create_income_expense_chart(
            income,
            expense,
            "assets/income_expense_chart.png"
        )

        self.ids.income_expense_chart.source = ""

        self.ids.income_expense_chart.source = (
            "assets/income_expense_chart.png"
        )

        self.ids.income_expense_chart.reload()

        # =====================================================
        # CATEGORY-WISE SPENDING
        # =====================================================

        create_category_bar_chart(
            expense_data,
            "assets/category_chart.png"
        )

        self.ids.category_chart.source = ""

        self.ids.category_chart.source = (
            "assets/category_chart.png"
        )

        self.ids.category_chart.reload()

        # =====================================================
        # HIGHEST EXPENSE CATEGORY
        # =====================================================

        highest = get_highest_expense_category(
            user_id
        )

        if highest:

            category, amount = highest

            self.ids.highest_category.text = (
                category
            )

            self.ids.highest_amount.text = (
                f"{currency_symbol}"
                f"{amount:,.2f}"
            )

        else:

            self.ids.highest_category.text = (
                "No Expenses"
            )

            self.ids.highest_amount.text = (
                f"{currency_symbol}0.00"
            )

        # =====================================================
        # FINANCIAL INSIGHTS
        # =====================================================

        balance = get_balance(
            user_id
        )

        transaction_count = (
            get_transaction_count(
                user_id
            )
        )

        category_count = (
            get_expense_category_count(
                user_id
            )
        )

        # -----------------------------------------------------
        # Current Balance
        # -----------------------------------------------------

        self.ids.balance_label.text = (
            f"{currency_symbol}"
            f"{balance:,.2f}"
        )

        # -----------------------------------------------------
        # Total Transactions
        # -----------------------------------------------------

        self.ids.transaction_count_label.text = (
            str(transaction_count)
        )

        # -----------------------------------------------------
        # Expense Categories
        # -----------------------------------------------------

        self.ids.category_count_label.text = (
            str(category_count)
        )
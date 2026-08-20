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
        # CURRENCY
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

            category, highest_amount = highest

            self.ids.highest_category.text = (
                str(category)
            )

            self.ids.highest_amount.text = (
                f"{currency_symbol}"
                f"{highest_amount:,.2f}"
            )

        else:

            category = "No Expenses"
            highest_amount = 0

            self.ids.highest_category.text = (
                "No Expenses"
            )

            self.ids.highest_amount.text = (
                f"{currency_symbol}0.00"
            )

        # =====================================================
        # FINANCIAL OVERVIEW
        # =====================================================

        balance = get_balance(
            user_id
        )

        transaction_count = get_transaction_count(
            user_id
        )

        category_count = get_expense_category_count(
            user_id
        )

        # =====================================================
        # BALANCE
        # =====================================================

        self.ids.balance_label.text = (
            f"{currency_symbol}"
            f"{balance:,.2f}"
        )

        # =====================================================
        # TRANSACTION COUNT
        # =====================================================

        self.ids.transaction_count_label.text = (
            str(transaction_count)
        )

        # =====================================================
        # CATEGORY COUNT
        # =====================================================

        self.ids.category_count_label.text = (
            str(category_count)
        )

        # =====================================================
        # FINANCIAL INSIGHTS
        # =====================================================

        # Total income
        self.ids.total_income_label.text = (
            f"{currency_symbol}"
            f"{income:,.2f}"
        )

        # Total expenses
        self.ids.total_expense_label.text = (
            f"{currency_symbol}"
            f"{expense:,.2f}"
        )

        # Highest spending category
        self.ids.insight_category_label.text = (
            str(category)
        )

        self.ids.insight_category_amount.text = (
            f"{currency_symbol}"
            f"{highest_amount:,.2f}"
        )

        # =====================================================
        # SAVINGS RATE
        # =====================================================

        if income > 0:

            savings_rate = (
                (income - expense) / income
            ) * 100

        else:

            savings_rate = 0

        self.ids.savings_rate_label.text = (
            f"{savings_rate:.1f}%"
        )

        # =====================================================
        # DYNAMIC INSIGHT MESSAGE
        # =====================================================

        if income <= 0 and expense <= 0:

            insight = (
                "Start adding transactions to see "
                "your financial insights."
            )

        elif income <= 0:

            insight = (
                "You currently have expenses recorded "
                "but no income recorded."
            )

        elif expense <= 0:

            insight = (
                "Great start! You have income recorded "
                "but no expenses yet."
            )

        elif expense > income:

            insight = (
                "Your expenses are higher than your "
                "income. Consider reviewing your spending."
            )

        elif savings_rate >= 50:

            insight = (
                "Excellent! You are keeping more than "
                "half of your income after expenses."
            )

        elif savings_rate >= 20:

            insight = (
                "Good progress! You are saving a healthy "
                "portion of your income."
            )

        else:

            insight = (
                "Your expenses are taking a large share "
                "of your income. Keep an eye on spending."
            )

        self.ids.insight_message.text = insight
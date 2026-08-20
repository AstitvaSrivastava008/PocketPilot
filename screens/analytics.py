from kivy.app import App
from kivy.uix.screenmanager import Screen

from database import (
    get_expense_by_category,
    get_highest_expense_category,
    get_income_vs_expense,
    get_expense_category_count,
    get_balance,
    get_transaction_count,
)

from charts import (
    create_expense_pie_chart,
    create_income_expense_chart,
    create_category_bar_chart,
)

from ai.financial_advisor import FinancialAdvisor


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

        expense_data = get_expense_by_category(user_id)

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

        income, expense = get_income_vs_expense(user_id)

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

        highest = get_highest_expense_category(user_id)

        if highest:

            category, highest_amount = highest

        else:

            category = "No Expenses"
            highest_amount = 0

        # =====================================================
        # HIGHEST CATEGORY
        #
        # These IDs are required by this Python file.
        # =====================================================

        if "highest_category" in self.ids:
            self.ids.highest_category.text = str(category)

        if "highest_amount" in self.ids:
            self.ids.highest_amount.text = (
                f"{currency_symbol}"
                f"{highest_amount:,.2f}"
            )

        # =====================================================
        # FINANCIAL OVERVIEW
        # =====================================================

        balance = get_balance(user_id)

        transaction_count = get_transaction_count(user_id)

        category_count = get_expense_category_count(user_id)

        # =====================================================
        # BALANCE
        # =====================================================

        if "balance_label" in self.ids:

            self.ids.balance_label.text = (
                f"{currency_symbol}"
                f"{balance:,.2f}"
            )

        # =====================================================
        # TRANSACTION COUNT
        # =====================================================

        if "transaction_count_label" in self.ids:

            self.ids.transaction_count_label.text = (
                str(transaction_count)
            )

        # =====================================================
        # CATEGORY COUNT
        # =====================================================

        if "category_count_label" in self.ids:

            self.ids.category_count_label.text = (
                str(category_count)
            )

        # =====================================================
        # TOTAL INCOME
        # =====================================================

        if "total_income_label" in self.ids:

            self.ids.total_income_label.text = (
                f"{currency_symbol}"
                f"{income:,.2f}"
            )

        # =====================================================
        # TOTAL EXPENSE
        # =====================================================

        if "total_expense_label" in self.ids:

            self.ids.total_expense_label.text = (
                f"{currency_symbol}"
                f"{expense:,.2f}"
            )

        # =====================================================
        # HIGHEST SPENDING INSIGHT
        # =====================================================

        if "insight_category_label" in self.ids:

            self.ids.insight_category_label.text = (
                str(category)
            )

        if "insight_category_amount" in self.ids:

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

        if "savings_rate_label" in self.ids:

            self.ids.savings_rate_label.text = (
                f"{savings_rate:.1f}%"
            )

        # =====================================================
        # AI FINANCIAL ADVISOR
        # =====================================================

        try:

            recommendation = (
                FinancialAdvisor.generate_recommendation(
                    user_id
                )
            )

            # -------------------------------------------------
            # AI TITLE
            # -------------------------------------------------

            if "ai_title" in self.ids:

                self.ids.ai_title.text = (
                    recommendation.get(
                        "title",
                        "Financial Recommendation"
                    )
                )

            # -------------------------------------------------
            # AI MESSAGE
            # -------------------------------------------------

            if "insight_message" in self.ids:

                self.ids.insight_message.text = (
                    recommendation.get(
                        "message",
                        "Keep tracking your finances "
                        "to receive personalised recommendations."
                    )
                )

            # -------------------------------------------------
            # AI PRIORITY
            # -------------------------------------------------

            priority = recommendation.get(
                "priority",
                "info"
            )

            priority_text = str(priority).upper()

            if "ai_priority" in self.ids:

                self.ids.ai_priority.text = priority_text

            # -------------------------------------------------
            # UPDATE AI PRIORITY COLOUR
            # -------------------------------------------------

            if "ai_priority" in self.ids:

                if priority == "danger":

                    self.ids.ai_priority.color = (
                        1, 0.20, 0.20, 1
                    )

                elif priority == "warning":

                    self.ids.ai_priority.color = (
                        1, 0.65, 0.10, 1
                    )

                elif priority == "success":

                    self.ids.ai_priority.color = (
                        0.10, 0.80, 0.35, 1
                    )

                else:

                    self.ids.ai_priority.color = (
                        0.25, 0.55, 1, 1
                    )

        except Exception as error:

            print(
                "AI Advisor Error:",
                error
            )

            if "ai_title" in self.ids:

                self.ids.ai_title.text = (
                    "Financial Advisor"
                )

            if "insight_message" in self.ids:

                self.ids.insight_message.text = (
                    "Your financial data is available. "
                    "Continue tracking your income and "
                    "expenses for personalised insights."
                )

            if "ai_priority" in self.ids:

                self.ids.ai_priority.text = "INFO"
                self.ids.ai_priority.color = (
                    0.25, 0.55, 1, 1
                )
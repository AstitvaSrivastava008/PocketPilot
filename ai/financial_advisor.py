from database import (
    get_balance,
    get_transaction_count,
    get_highest_expense_category,
    get_expense_by_category,
    get_income_vs_expense,
    get_expense_category_count,
)


class FinancialAdvisor:
    """
    PocketPilot Financial Advisor

    Generates personalised financial recommendations
    from the user's local transaction data.

    This version is intentionally rule-based and local.
    It does not require an internet connection or an
    external AI service.

    The recommendation engine analyses:
        - Income
        - Expenses
        - Balance
        - Savings rate
        - Transaction count
        - Expense categories
        - Highest spending category
        - Category concentration
    """

    # =========================================================
    # RESULT BUILDER
    # =========================================================

    @staticmethod
    def _build_result(
        title,
        message,
        priority,
        savings_rate,
        balance,
        highest_category,
        highest_amount,
        category_count,
    ):
        """
        Creates a consistent recommendation dictionary.
        """

        return {
            "title": title,
            "message": message,
            "priority": priority,
            "savings_rate": round(savings_rate, 1),
            "balance": balance,
            "highest_category": highest_category,
            "highest_amount": highest_amount,
            "category_count": category_count,
        }

    # =========================================================
    # GENERATE RECOMMENDATION
    # =========================================================

    @staticmethod
    def generate_recommendation(user_id):

        # =====================================================
        # GET FINANCIAL DATA
        # =====================================================

        balance = get_balance(user_id)

        transaction_count = get_transaction_count(user_id)

        income, expense = get_income_vs_expense(user_id)

        expense_data = get_expense_by_category(user_id)

        category_count = get_expense_category_count(user_id)

        highest = get_highest_expense_category(user_id)

        # =====================================================
        # SAVINGS RATE
        # =====================================================

        if income > 0:

            savings_rate = (
                (income - expense) / income
            ) * 100

        else:

            savings_rate = 0

        # =====================================================
        # HIGHEST EXPENSE CATEGORY
        # =====================================================

        if highest:

            highest_category, highest_amount = highest

        else:

            highest_category = "None"
            highest_amount = 0

        # =====================================================
        # CATEGORY CONCENTRATION
        # =====================================================

        category_share = 0

        if expense > 0 and highest_amount > 0:

            category_share = (
                highest_amount / expense
            ) * 100

        # =====================================================
        # NO TRANSACTIONS
        # =====================================================

        if transaction_count == 0:

            return FinancialAdvisor._build_result(
                title="Start Tracking",
                message=(
                    "Add your first income or expense "
                    "to start receiving personalised "
                    "financial recommendations."
                ),
                priority="info",
                savings_rate=0,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # NO INCOME AND NO EXPENSES
        # =====================================================

        if income <= 0 and expense <= 0:

            return FinancialAdvisor._build_result(
                title="Start Your Financial Journey",
                message=(
                    "Start recording your income and expenses "
                    "to understand your financial habits and "
                    "receive personalised recommendations."
                ),
                priority="info",
                savings_rate=0,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # EXPENSES BUT NO INCOME
        # =====================================================

        if income <= 0 and expense > 0:

            return FinancialAdvisor._build_result(
                title="Income Tracking Needed",
                message=(
                    f"You have recorded "
                    f"₹{expense:,.2f} in expenses but no income. "
                    "Make sure your income transactions are "
                    "being recorded so PocketPilot can accurately "
                    "analyse your financial position."
                ),
                priority="danger",
                savings_rate=0,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # EXPENSES GREATER THAN INCOME
        # =====================================================

        if expense > income:

            difference = expense - income

            return FinancialAdvisor._build_result(
                title="Overspending Alert",
                message=(
                    f"Your expenses are currently "
                    f"₹{difference:,.2f} higher than your income. "
                    f"Your largest expense is {highest_category} "
                    f"at ₹{highest_amount:,.2f}. "
                    "Consider reviewing non-essential spending "
                    "and reducing your largest expense categories."
                ),
                priority="danger",
                savings_rate=savings_rate,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # NO EXPENSES
        # =====================================================

        if expense <= 0:

            return FinancialAdvisor._build_result(
                title="Great Start",
                message=(
                    "You have recorded income but no expenses yet. "
                    "Continue tracking your spending so PocketPilot "
                    "can provide more useful financial recommendations."
                ),
                priority="success",
                savings_rate=savings_rate,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # DOMINANT CATEGORY
        # =====================================================

        # If one category represents more than 60% of all
        # recorded expenses, highlight that concentration.

        if category_share >= 60:

            return FinancialAdvisor._build_result(
                title="High Category Concentration",
                message=(
                    f"{highest_category} accounts for "
                    f"{category_share:.1f}% of your recorded "
                    f"expenses, totalling "
                    f"₹{highest_amount:,.2f}. "
                    "Consider reviewing this category and "
                    "setting a spending limit if possible."
                ),
                priority="warning",
                savings_rate=savings_rate,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # EXCELLENT SAVINGS
        # =====================================================

        if savings_rate >= 50:

            return FinancialAdvisor._build_result(
                title="Excellent Saving Habit",
                message=(
                    f"You're currently saving "
                    f"{savings_rate:.1f}% of your recorded income. "
                    "That's a strong savings rate. Consider "
                    "directing part of your surplus toward your "
                    "savings goals or long-term financial plans."
                ),
                priority="success",
                savings_rate=savings_rate,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # HEALTHY SAVINGS
        # =====================================================

        if savings_rate >= 20:

            return FinancialAdvisor._build_result(
                title="Healthy Financial Progress",
                message=(
                    f"Your current savings rate is "
                    f"{savings_rate:.1f}%. You're maintaining "
                    "a reasonable balance between income and "
                    f"expenses. Keep monitoring {highest_category}, "
                    "your largest expense category."
                ),
                priority="info",
                savings_rate=savings_rate,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # MODERATE SAVINGS
        # =====================================================

        if savings_rate >= 10:

            return FinancialAdvisor._build_result(
                title="Room to Improve Savings",
                message=(
                    f"Your current savings rate is "
                    f"{savings_rate:.1f}%. You're saving some "
                    f"of your income, but {highest_category} is "
                    f"your largest expense at "
                    f"₹{highest_amount:,.2f}. "
                    "Reviewing this category could help "
                    "increase your monthly savings."
                ),
                priority="warning",
                savings_rate=savings_rate,
                balance=balance,
                highest_category=highest_category,
                highest_amount=highest_amount,
                category_count=category_count,
            )

        # =====================================================
        # VERY LOW SAVINGS
        # =====================================================

        return FinancialAdvisor._build_result(
            title="Spending Recommendation",
            message=(
                f"Your current savings rate is only "
                f"{savings_rate:.1f}%. Your largest expense "
                f"category is {highest_category} at "
                f"₹{highest_amount:,.2f}. "
                "Consider setting a spending limit for this "
                "category and reviewing non-essential expenses "
                "to improve your savings."
            ),
            priority="warning",
            savings_rate=savings_rate,
            balance=balance,
            highest_category=highest_category,
            highest_amount=highest_amount,
            category_count=category_count,
        )
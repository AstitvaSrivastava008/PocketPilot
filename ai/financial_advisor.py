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
    Generates personalised financial recommendations
    from the user's PocketPilot transaction data.

    This is the first version of the recommendation engine.
    It is intentionally local/rule-based so PocketPilot
    continues working without an internet connection.
    """

    @staticmethod
    def generate_recommendation(user_id):
        # -------------------------------------------------
        # Get financial data
        # -------------------------------------------------

        balance = get_balance(user_id)

        transaction_count = get_transaction_count(user_id)

        income, expense = get_income_vs_expense(user_id)

        expense_data = get_expense_by_category(user_id)

        category_count = get_expense_category_count(user_id)

        highest = get_highest_expense_category(user_id)

        # -------------------------------------------------
        # Calculate savings rate
        # -------------------------------------------------

        if income > 0:
            savings_rate = ((income - expense) / income) * 100
        else:
            savings_rate = 0

        # -------------------------------------------------
        # Highest expense category
        # -------------------------------------------------

        if highest:
            highest_category, highest_amount = highest
        else:
            highest_category = "None"
            highest_amount = 0

        # -------------------------------------------------
        # No transactions
        # -------------------------------------------------

        if transaction_count == 0:

            return {
                "title": "Start Tracking",
                "message": (
                    "Add your first income or expense "
                    "to start receiving personalised "
                    "financial recommendations."
                ),
                "priority": "info",
                "savings_rate": 0,
                "balance": balance,
                "highest_category": highest_category,
                "highest_amount": highest_amount,
                "category_count": category_count,
            }

        # -------------------------------------------------
        # No income and no expenses
        # -------------------------------------------------

        if income <= 0 and expense <= 0:

            return {
                "title": "Start Your Financial Journey",
                "message": (
                    "Start recording your income and expenses "
                    "to understand your financial habits."
                ),
                "priority": "info",
                "savings_rate": 0,
                "balance": balance,
                "highest_category": highest_category,
                "highest_amount": highest_amount,
                "category_count": category_count,
            }

        # -------------------------------------------------
        # Expenses higher than income
        # -------------------------------------------------

        if expense > income:

            difference = expense - income

            return {
                "title": "Overspending Alert",
                "message": (
                    f"Your expenses are currently "
                    f"₹{difference:,.2f} higher than your income. "
                    "Consider reviewing your largest spending "
                    "categories and reducing non-essential expenses."
                ),
                "priority": "danger",
                "savings_rate": round(savings_rate, 1),
                "balance": balance,
                "highest_category": highest_category,
                "highest_amount": highest_amount,
                "category_count": category_count,
            }

        # -------------------------------------------------
        # No expenses
        # -------------------------------------------------

        if expense <= 0:

            return {
                "title": "Great Start",
                "message": (
                    "You have recorded income but no expenses yet. "
                    "Continue tracking your spending so PocketPilot "
                    "can provide more useful recommendations."
                ),
                "priority": "success",
                "savings_rate": round(savings_rate, 1),
                "balance": balance,
                "highest_category": highest_category,
                "highest_amount": highest_amount,
                "category_count": category_count,
            }

        # -------------------------------------------------
        # Excellent savings rate
        # -------------------------------------------------

        if savings_rate >= 50:

            return {
                "title": "Excellent Saving Habit",
                "message": (
                    f"You're currently saving {savings_rate:.1f}% "
                    "of your recorded income. That's a strong "
                    "saving rate. Consider directing part of "
                    "your surplus toward your financial goals."
                ),
                "priority": "success",
                "savings_rate": round(savings_rate, 1),
                "balance": balance,
                "highest_category": highest_category,
                "highest_amount": highest_amount,
                "category_count": category_count,
            }

        # -------------------------------------------------
        # Healthy savings rate
        # -------------------------------------------------

        if savings_rate >= 20:

            return {
                "title": "Healthy Financial Progress",
                "message": (
                    f"Your current savings rate is "
                    f"{savings_rate:.1f}%. You're maintaining "
                    f"a reasonable balance between income and "
                    f"expenses. Keep monitoring {highest_category}, "
                    "your largest expense category."
                ),
                "priority": "info",
                "savings_rate": round(savings_rate, 1),
                "balance": balance,
                "highest_category": highest_category,
                "highest_amount": highest_amount,
                "category_count": category_count,
            }

        # -------------------------------------------------
        # Low savings rate
        # -------------------------------------------------

        return {
            "title": "Spending Recommendation",
            "message": (
                f"Your current savings rate is only "
                f"{savings_rate:.1f}%. Your largest expense "
                f"category is {highest_category} at "
                f"₹{highest_amount:,.2f}. Consider setting "
                "a spending limit for this category to improve "
                "your savings."
            ),
            "priority": "warning",
            "savings_rate": round(savings_rate, 1),
            "balance": balance,
            "highest_category": highest_category,
            "highest_amount": highest_amount,
            "category_count": category_count,
        }
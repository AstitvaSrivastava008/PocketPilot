import matplotlib.pyplot as plt


# ==========================================
# EXPENSE PIE CHART
# ==========================================
def create_expense_pie_chart(expense_data, output_path):

    if not expense_data:
        return

    categories = []
    amounts = []

    for category, amount in expense_data:
        categories.append(category)
        amounts.append(amount)

    colors = [
        "#4CAF50",
        "#2196F3",
        "#FF9800",
        "#F44336",
        "#9C27B0",
        "#009688",
        "#FFC107",
        "#795548"
    ]

    plt.figure(figsize=(7, 6))

    plt.pie(
        amounts,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[:len(categories)],
        textprops={"fontsize": 11}
    )

    plt.legend(
        categories,
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.axis("equal")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight"
    )

    plt.close()


# ==========================================
# INCOME VS EXPENSE BAR CHART
# ==========================================
def create_income_expense_chart(income, expense, output_path):

    labels = ["Income", "Expense"]
    values = [income, expense]
    colors = ["#4CAF50", "#F44336"]

    plt.figure(figsize=(6, 4))

    bars = plt.bar(
        labels,
        values,
        color=colors,
        width=0.55
    )

    plt.title("Income vs Expense")
    plt.ylabel("Amount (₹)")

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"₹{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight"
    )

    plt.close()


# ==========================================
# CATEGORY-WISE SPENDING
# ==========================================
def create_category_bar_chart(expense_data, output_path):

    if not expense_data:
        return

    categories = []
    amounts = []

    for category, amount in expense_data:
        categories.append(category)
        amounts.append(amount)

    # Biggest category at the top
    categories.reverse()
    amounts.reverse()

    plt.figure(figsize=(7, 5))

    bars = plt.barh(
        categories,
        amounts,
        color="#42A5F5"
    )

    plt.title("Category-wise Spending")
    plt.xlabel("Amount (₹)")

    for bar, value in zip(bars, amounts):
        plt.text(
            value + max(amounts) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"₹{value:,.0f}",
            va="center",
            fontsize=10
        )

    plt.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight"
    )

    plt.close()
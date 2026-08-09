import matplotlib.pyplot as plt
from kivy.app import App


# ==================================================
# Theme Helper
# ==================================================

def is_dark_mode():
    app = App.get_running_app()
    return app and app.theme_cls.theme_style == "Dark"


# ==================================================
# EXPENSE PIE CHART
# ==================================================

def create_expense_pie_chart(expense_data, output_path):

    if not expense_data:
        return

    dark = is_dark_mode()

    categories = [c for c, a in expense_data]
    amounts = [a for c, a in expense_data]

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

    fig, ax = plt.subplots(figsize=(7, 6))

    # Transparent background
    ax.set_facecolor("none")

    wedges, texts, autotexts = ax.pie(
        amounts,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[:len(categories)],
        textprops={
            "fontsize": 11,
            "color": "white" if dark else "black"
        }
    )

    legend = ax.legend(
        categories,
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    if dark:
        legend.get_frame().set_alpha(0)
        for txt in legend.get_texts():
            txt.set_color("white")

    ax.axis("equal")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight",
        transparent=True
    )

    plt.close(fig)


# ==================================================
# INCOME VS EXPENSE
# ==================================================

def create_income_expense_chart(income, expense, output_path):

    dark = is_dark_mode()

    labels = ["Income", "Expense"]
    values = [income, expense]

    colors = [
        "#4CAF50",
        "#F44336"
    ]

    fig, ax = plt.subplots(figsize=(6, 4))

    # Transparent background
    ax.set_facecolor("none")

    bars = ax.bar(
        labels,
        values,
        color=colors,
        width=0.55
    )

    ax.set_title(
        "Income vs Expense",
        color="white" if dark else "black"
    )

    ax.set_ylabel(
        "Amount (₹)",
        color="white" if dark else "black"
    )

    ax.tick_params(
        colors="white" if dark else "black"
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    if dark:
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            value,
            f"₹{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=10,
            color="white" if dark else "black"
        )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight",
        transparent=True
    )

    plt.close(fig)


# ==================================================
# CATEGORY BAR CHART
# ==================================================

def create_category_bar_chart(expense_data, output_path):

    if not expense_data:
        return

    dark = is_dark_mode()

    categories = [c for c, a in expense_data]
    amounts = [a for c, a in expense_data]

    categories.reverse()
    amounts.reverse()

    fig, ax = plt.subplots(figsize=(7, 5))

    # Transparent background
    ax.set_facecolor("none")

    bars = ax.barh(
        categories,
        amounts,
        color="#42A5F5"
    )

    ax.set_title(
        "Category-wise Spending",
        color="white" if dark else "black"
    )

    ax.set_xlabel(
        "Amount (₹)",
        color="white" if dark else "black"
    )

    ax.tick_params(
        colors="white" if dark else "black"
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )

    if dark:
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    max_amount = max(amounts) if amounts else 0

    for bar, value in zip(bars, amounts):
        ax.text(
            value + max_amount * 0.02,
            bar.get_y() + bar.get_height()/2,
            f"₹{value:,.0f}",
            va="center",
            fontsize=10,
            color="white" if dark else "black"
        )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight",
        transparent=True
    )

    plt.close(fig)
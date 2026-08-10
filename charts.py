import os

import matplotlib.pyplot as plt

from kivy.app import App


# ============================================================
# THEME
# ============================================================

def is_dark_mode():
    """Return True when PocketPilot is using Dark mode."""

    app = App.get_running_app()

    if app is None:
        return False

    return app.theme_cls.theme_style == "Dark"


def get_text_color():
    """Return chart text colour based on current theme."""

    if is_dark_mode():
        return "#FFFFFF"

    return "#222222"


# ============================================================
# CURRENCY
# ============================================================

def get_currency_symbol():
    """
    Return the currently selected currency symbol.

    The currency is stored in the App object by the
    Settings screen.
    """

    app = App.get_running_app()

    if app is None:
        return "₹"

    symbol = getattr(
        app,
        "currency_symbol",
        None
    )

    if symbol:
        return symbol

    return "₹"


# ============================================================
# OUTPUT PATH
# ============================================================

def prepare_output_path(output_path):
    """Make sure the output directory exists."""

    directory = os.path.dirname(output_path)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )


# ============================================================
# EXPENSE PIE CHART
# ============================================================

def create_expense_pie_chart(
    expense_data,
    output_path
):
    """
    Create an expense breakdown pie chart.

    expense_data example:

        [
            ("Food", 5000),
            ("Bills", 2500),
            ("Travel", 1500)
        ]
    """

    prepare_output_path(
        output_path
    )

    text_color = get_text_color()

    # --------------------------------------------------------
    # NO DATA
    # --------------------------------------------------------

    if not expense_data:

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        fig.patch.set_alpha(0)

        ax.set_facecolor(
            "none"
        )

        ax.text(
            0.5,
            0.5,
            "No expense data available",
            ha="center",
            va="center",
            fontsize=16,
            color=text_color
        )

        ax.axis("off")

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=180,
            bbox_inches="tight",
            transparent=True
        )

        plt.close(fig)

        return

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    categories = [
        category
        for category, amount in expense_data
    ]

    amounts = [
        float(amount)
        for category, amount in expense_data
    ]

    # --------------------------------------------------------
    # POCKETPILOT COLOURS
    # --------------------------------------------------------

    colors = [
        "#1F5BD7",
        "#42A5F5",
        "#4CAF50",
        "#FF9800",
        "#F44336",
        "#9C27B0",
        "#009688",
        "#FFC107",
        "#795548",
        "#607D8B"
    ]

    chart_colors = [
        colors[index % len(colors)]
        for index in range(len(categories))
    ]

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    fig.patch.set_alpha(0)

    ax.set_facecolor(
        "none"
    )

    wedges, texts, autotexts = ax.pie(
        amounts,
        autopct="%1.1f%%",
        startangle=90,
        colors=chart_colors,
        pctdistance=0.70,
        wedgeprops={
            "linewidth": 1,
            "edgecolor": "white"
        }
    )

    # --------------------------------------------------------
    # PERCENTAGE TEXT
    # --------------------------------------------------------

    for autotext in autotexts:

        autotext.set_color(
            "white"
        )

        autotext.set_fontsize(
            10
        )

        autotext.set_weight(
            "bold"
        )

    # --------------------------------------------------------
    # LEGEND
    # --------------------------------------------------------

    legend = ax.legend(
        wedges,
        categories,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        frameon=False,
        fontsize=10
    )

    for text in legend.get_texts():

        text.set_color(
            text_color
        )

    ax.axis("equal")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight",
        transparent=True
    )

    plt.close(fig)


# ============================================================
# INCOME VS EXPENSE
# ============================================================

def create_income_expense_chart(
    income,
    expense,
    output_path
):
    """
    Create an Income vs Expense bar chart.

    The currency symbol is taken from the current
    PocketPilot currency setting.
    """

    prepare_output_path(
        output_path
    )

    text_color = get_text_color()

    currency = get_currency_symbol()

    income = float(
        income or 0
    )

    expense = float(
        expense or 0
    )

    labels = [
        "Income",
        "Expense"
    ]

    values = [
        income,
        expense
    ]

    colors = [
        "#4CAF50",
        "#F44336"
    ]

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    fig.patch.set_alpha(0)

    ax.set_facecolor(
        "none"
    )

    bars = ax.bar(
        labels,
        values,
        color=colors,
        width=0.55
    )

    # --------------------------------------------------------
    # AXIS
    # --------------------------------------------------------

    ax.set_ylabel(
        f"Amount ({currency})",
        fontsize=10,
        color=text_color
    )

    ax.tick_params(
        axis="both",
        colors=text_color,
        labelsize=10
    )

    # --------------------------------------------------------
    # GRID
    # --------------------------------------------------------

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(
        True
    )

    # --------------------------------------------------------
    # SPINES
    # --------------------------------------------------------

    ax.spines[
        "top"
    ].set_visible(False)

    ax.spines[
        "right"
    ].set_visible(False)

    if is_dark_mode():

        ax.spines[
            "left"
        ].set_color("#777777")

        ax.spines[
            "bottom"
        ].set_color("#777777")

    else:

        ax.spines[
            "left"
        ].set_color("#CCCCCC")

        ax.spines[
            "bottom"
        ].set_color("#CCCCCC")

    # --------------------------------------------------------
    # Y AXIS SPACE
    # --------------------------------------------------------

    maximum = max(
        values
    )

    if maximum > 0:

        ax.set_ylim(
            0,
            maximum * 1.20
        )

    else:

        ax.set_ylim(
            0,
            1
        )

    # --------------------------------------------------------
    # VALUE LABELS
    # --------------------------------------------------------

    for bar, value in zip(
        bars,
        values
    ):

        if maximum > 0:

            y_position = (
                value
                + maximum * 0.03
            )

        else:

            y_position = 0.03

        ax.text(
            bar.get_x()
            + bar.get_width() / 2,

            y_position,

            f"{currency}{value:,.0f}",

            ha="center",
            va="bottom",

            fontsize=10,
            fontweight="bold",

            color=text_color
        )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight",
        transparent=True
    )

    plt.close(fig)


# ============================================================
# CATEGORY-WISE SPENDING
# ============================================================

def create_category_bar_chart(
    expense_data,
    output_path
):
    """
    Create a horizontal bar chart for category spending.

    The currency symbol is taken from the current
    PocketPilot currency setting.
    """

    prepare_output_path(
        output_path
    )

    text_color = get_text_color()

    currency = get_currency_symbol()

    # --------------------------------------------------------
    # NO DATA
    # --------------------------------------------------------

    if not expense_data:

        fig, ax = plt.subplots(
            figsize=(7, 4)
        )

        fig.patch.set_alpha(0)

        ax.set_facecolor(
            "none"
        )

        ax.text(
            0.5,
            0.5,
            "No category spending data available",
            ha="center",
            va="center",
            fontsize=15,
            color=text_color
        )

        ax.axis("off")

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=180,
            bbox_inches="tight",
            transparent=True
        )

        plt.close(fig)

        return

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    categories = [
        category
        for category, amount in expense_data
    ]

    amounts = [
        float(amount)
        for category, amount in expense_data
    ]

    # Don't modify original database data
    categories = list(
        categories
    )

    amounts = list(
        amounts
    )

    # Reverse order for cleaner presentation
    categories.reverse()
    amounts.reverse()

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    fig.patch.set_alpha(0)

    ax.set_facecolor(
        "none"
    )

    bars = ax.barh(
        categories,
        amounts,
        color="#1F5BD7",
        height=0.60
    )

    # --------------------------------------------------------
    # AXIS
    # --------------------------------------------------------

    ax.set_xlabel(
        f"Amount ({currency})",
        fontsize=10,
        color=text_color
    )

    ax.tick_params(
        axis="both",
        colors=text_color,
        labelsize=10
    )

    # --------------------------------------------------------
    # GRID
    # --------------------------------------------------------

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(
        True
    )

    # --------------------------------------------------------
    # SPINES
    # --------------------------------------------------------

    ax.spines[
        "top"
    ].set_visible(False)

    ax.spines[
        "right"
    ].set_visible(False)

    if is_dark_mode():

        ax.spines[
            "left"
        ].set_color("#777777")

        ax.spines[
            "bottom"
        ].set_color("#777777")

    else:

        ax.spines[
            "left"
        ].set_color("#CCCCCC")

        ax.spines[
            "bottom"
        ].set_color("#CCCCCC")

    # --------------------------------------------------------
    # VALUE LABELS
    # --------------------------------------------------------

    maximum = max(
        amounts
    )

    if maximum > 0:

        label_offset = (
            maximum * 0.02
        )

        ax.set_xlim(
            0,
            maximum * 1.18
        )

    else:

        label_offset = 1

    for bar, value in zip(
        bars,
        amounts
    ):

        ax.text(
            value + label_offset,

            bar.get_y()
            + bar.get_height() / 2,

            f"{currency}{value:,.0f}",

            va="center",

            fontsize=10,
            fontweight="bold",

            color=text_color
        )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=180,
        bbox_inches="tight",
        transparent=True
    )

    plt.close(fig)
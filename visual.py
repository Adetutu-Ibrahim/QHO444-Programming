"""
This module is responsible for visualising the data using Matplotlib.
Any visualisations should be generated via functions in this module.
"""





import matplotlib.pyplot as plt
import calendar


def pie_chart_reviews_per_park(counts):
    """
    Display a pie chart showing the number of reviews per park.

    Args:
        counts (dict): { park_name: review_count }
    """
    if not counts:
        print("No data available to plot.")
        return

    labels = list(counts.keys())
    sizes = list(counts.values())

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
    )
    ax.set_title("Number of Reviews per Disneyland Park", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def bar_chart_top_locations(top_locations, park):
    """
    Display a bar chart of the top 10 locations by average rating for a park.

    Args:
        top_locations (list): List of (location, avg_rating) tuples.
        park (str): The park name (used in the chart title).
    """
    if not top_locations:
        print(f"No data available to plot for '{park}'.")
        return

    locations = [item[0] for item in top_locations]
    averages = [item[1] for item in top_locations]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(locations, averages, color="steelblue", edgecolor="black")

    ax.set_xlabel("Reviewer Location", fontsize=12)
    ax.set_ylabel("Average Rating", fontsize=12)
    ax.set_title(
        f"Top 10 Locations by Average Rating – {park}",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_ylim(0, 5.5)
    ax.tick_params(axis="x", rotation=45)

    for bar, avg in zip(bars, averages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"{avg:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    plt.show()


def bar_chart_avg_rating_by_month(monthly_avgs, park):
    """
    Display a bar chart of average rating per month of the year for a park.
    Months are ordered January–December.

    Args:
        monthly_avgs (dict): { month_int: avg_rating }
        park (str): The park name (used in the chart title).
    """
    if not monthly_avgs:
        print(f"No data available to plot for '{park}'.")
        return

    # Build ordered month data (1-12)
    months_ordered = list(range(1, 13))
    month_names = [calendar.month_abbr[m] for m in months_ordered]
    averages = [monthly_avgs.get(m, 0) for m in months_ordered]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(month_names, averages, color="coral", edgecolor="black")

    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Average Rating", fontsize=12)
    ax.set_title(
        f"Average Rating by Month – {park}",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_ylim(0, 5.5)

    for bar, avg in zip(bars, averages):
        if avg > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                f"{avg:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    plt.tight_layout()
    plt.show()

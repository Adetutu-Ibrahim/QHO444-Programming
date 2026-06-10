"""
This module is responsible for the overall program flow. It controls how the user interacts with the
program and how the program behaves. It uses the other modules to interact with the user, carry out
processing, and for visualising information.

Note:   any user input/output should be done in the module 'tui'
        any processing should be done in the module 'process'
        any visualisation should be done in the module 'visual'
"""




import tui
import process
import visual
from exporter import create_exporter

CSV_FILE = "data/disneyland_reviews.csv"



def load_data():
    """Load the dataset from CSV and inform the user."""
    dataset = process.read_dataset(CSV_FILE)
    tui.display_dataset_loaded(len(dataset))
    return dataset


def handle_view_menu(dataset):
    """
    Present the View Data sub-menu and dispatch to the chosen handler.

    Args:
        dataset (list): The loaded dataset.
    """
    tui.display_view_menu()
    choice = tui.get_user_choice()
    tui.display_confirmed_choice(choice)

    if choice == "A":
        park = tui.get_string_input("Enter park name: ")
        reviews = process.get_reviews_by_park(dataset, park)
        tui.display_reviews(reviews, park)

    elif choice == "B":
        park = tui.get_string_input("Enter park name: ")
        location = tui.get_string_input("Enter reviewer location: ")
        count = process.count_reviews_by_park_and_location(dataset, park, location)
        tui.display_review_count(park, location, count)

    elif choice == "C":
        park = tui.get_string_input("Enter park name: ")
        year = tui.get_integer_input("Enter year: ")
        avg = process.average_rating_by_park_and_year(dataset, park, year)
        tui.display_average_rating(park, year, avg)

    elif choice == "D":
        all_avgs = process.average_rating_by_park_and_location(dataset)
        for park, averages in sorted(all_avgs.items()):
            tui.display_avg_by_location(park, averages)

    else:
        tui.display_invalid_choice()


def handle_visualise_menu(dataset):
    """
    Present the Visualise Data sub-menu and dispatch chart rendering.

    Args:
        dataset (list): The loaded dataset.
    """
    tui.display_visualise_menu()
    choice = tui.get_user_choice()
    tui.display_confirmed_choice(choice)

    if choice == "A":
        counts = process.count_reviews_per_park(dataset)
        visual.pie_chart_reviews_per_park(counts)

    elif choice == "B":
        park = tui.get_string_input("Enter park name: ")
        top_locations = process.top_locations_by_avg_rating(dataset, park)
        visual.bar_chart_top_locations(top_locations, park)

    elif choice == "C":
        park = tui.get_string_input("Enter park name: ")
        monthly_avgs = process.avg_rating_by_month(dataset, park)
        visual.bar_chart_avg_rating_by_month(monthly_avgs, park)

    else:
        tui.display_invalid_choice()


def handle_export_menu(dataset):
    """
    Present the Export Data sub-menu, build aggregate stats, and export.

    Args:
        dataset (list): The loaded dataset.
    """
    tui.display_export_menu()
    choice = tui.get_user_choice()
    tui.display_confirmed_choice(choice)

    format_map = {"A": "TXT", "B": "CSV", "C": "JSON"}
    export_format = format_map.get(choice)

    if export_format is None:
        tui.display_invalid_choice()
        return

    stats = process.aggregate_park_stats(dataset)
    exporter = create_exporter(export_format, stats)
    exporter.export()



def main():
    """Main entry point – loads data then runs the menu loop."""
    tui.display_title()
    dataset = load_data()

    while True:
        tui.display_main_menu()
        choice = tui.get_user_choice()
        tui.display_confirmed_choice(choice)

        if choice == "A":
            handle_view_menu(dataset)

        elif choice == "B":
            handle_visualise_menu(dataset)

        elif choice == "C":
            handle_export_menu(dataset)

        elif choice == "X":
            tui.display_message("Goodbye!")
            break

        else:
            tui.display_invalid_choice()


if __name__ == "__main__":
    main()
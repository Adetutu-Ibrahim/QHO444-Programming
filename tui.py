"""
This module is responsible for processing the data.  It will largely contain functions that will recieve the overall dataset and 
perfrom necessary processes in order to provide the desired result in the desired format.
It is likely that most sections will require functions to be placed in this module.
"""





def display_title():
    """Display the application title banner."""
    print("=" * 50)
    print("    Disneyland Reviews Analysis System")
    print("=" * 50)
    print()


def display_main_menu():
    """Display the main menu options."""
    print("\nPlease enter one of the following options:")
    print("  A - View Data")
    print("  B - Visualise Data")
    print("  C - Export Data")
    print("  X - Exit")
    print()


def display_view_menu():
    """Display the View Data sub-menu options."""
    print("\nPlease enter one of the following options:")
    print("  A - View Reviews for a Park")
    print("  B - Number of Reviews by Park and Location")
    print("  C - Average Rating by Park and Year")
    print("  D - Average Score per Park by Reviewer Location")
    print()


def display_visualise_menu():
    """Display the Visualise Data sub-menu options."""
    print("\nPlease enter one of the following options:")
    print("  A - Most Reviewed Parks")
    print("  B - Park Ranking by Nationality")
    print("  C - Most Popular Month by Park")
    print()


def display_export_menu():
    """Display the Export Data sub-menu options."""
    print("\nPlease select an export format:")
    print("  A - TXT")
    print("  B - CSV")
    print("  C - JSON")
    print()


def get_user_choice(prompt="Enter your choice: "):
    """
    Prompt the user for input and return it uppercased.

    Args:
        prompt (str): The prompt message shown to the user.

    Returns:
        str: The user's input, stripped and uppercased.
    """
    return input(prompt).strip().upper()


def display_message(message):
    """
    Print a generic message to the screen.

    Args:
        message (str): The message to display.
    """
    print(message)


def display_invalid_choice():
    """Inform the user they entered an invalid menu choice."""
    print("Invalid choice. Please try again.")


def display_confirmed_choice(choice):
    """
    Confirm back to the user what they entered.

    Args:
        choice (str): The choice the user made.
    """
    print(f"You have entered: {choice}")


def get_string_input(prompt):
    """
    Retrieve a non-empty string from the user.

    Args:
        prompt (str): The prompt message.

    Returns:
        str: The user's input, stripped.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_integer_input(prompt):
    """
    Retrieve an integer value from the user.

    Args:
        prompt (str): The prompt message.

    Returns:
        int: The integer entered by the user.
    """
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid integer.")


def display_reviews(reviews, park):
    """
    Display a list of reviews for a given park.

    Args:
        reviews (list): A list of review dictionaries.
        park (str): The name of the park.
    """
    if not reviews:
        print(f"No reviews found for '{park}'.")
        return

    print(f"\n--- Reviews for {park} ({len(reviews)} total) ---")
    for review in reviews:
        print(
            f"  ID: {review['Review_ID']} | "
            f"Rating: {review['Rating']} | "
            f"Date: {review['Year_Month']} | "
            f"Location: {review['Reviewer_Location']}"
        )


def display_review_count(park, location, count):
    """
    Display the number of reviews a park received from a location.

    Args:
        park (str): The park name.
        location (str): The reviewer's location.
        count (int): The number of reviews.
    """
    print(f"\n'{park}' received {count} review(s) from '{location}'.")


def display_average_rating(park, year, average):
    """
    Display the average rating
    """

    if average is None:
        print(f"No reviews found for '{park}' in {year}.")
    else:
        print(f"\nAverage rating for '{park}' in {year}: {average:.2f}")


def display_avg_by_location(park, averages):
    """
    Display the average rating per reviewer location for a park.

    Args:
        park (str): The park name.
        averages (dict): Mapping of location -> average rating.
    """
    if not averages:
        print(f"No data found for '{park}'.")
        return

    print(f"\n--- Average Rating for '{park}' by Reviewer Location ---")
    for location, avg in sorted(averages.items()):
        print(f"  {location}: {avg:.2f}")


def display_dataset_loaded(row_count):
    """
    Inform the user the dataset has been loaded.

    Args:
        row_count (int): Number of rows loaded.
    """
    print(f"\nDataset loaded successfully. {row_count} rows found.\n")
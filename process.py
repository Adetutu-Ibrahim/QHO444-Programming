"""
This module is responsible for processing the data.  It will largely contain functions that will recieve the overall dataset and 
perfrom necessary processes in order to provide the desired result in the desired format.
It is likely that most sections will require functions to be placed in this module.
"""





import csv


def read_dataset(filepath):
    """
    Read the Disneyland reviews CSV file into a list of dictionaries.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        list: A list of row dictionaries, with Rating cast to int.
    """
    dataset = []
    with open(filepath, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                row["Rating"] = int(row["Rating"])
            except (ValueError, KeyError):
                pass
            dataset.append(row)
    return dataset


def get_reviews_by_park(dataset, park):
    """
    Return all reviews for a specific park (case-insensitive match).

    Args:
        dataset (list): The full dataset.
        park (str): The park name to filter by.

    Returns:
        list: Filtered list of review dictionaries.
    """
    return [
        row for row in dataset
        if row.get("Branch", "").strip().lower() == park.strip().lower()
    ]


def count_reviews_by_park_and_location(dataset, park, location):
    """
    Count reviews for a specific park from a specific location.

    Args:
        dataset (list): The full dataset.
        park (str): Park name.
        location (str): Reviewer location.

    Returns:
        int: The count of matching reviews.
    """
    return sum(
        1 for row in dataset
        if row.get("Branch", "").strip().lower() == park.strip().lower()
        and row.get("Reviewer_Location", "").strip().lower() == location.strip().lower()
    )


def average_rating_by_park_and_year(dataset, park, year):
    """
    Calculate the average rating for a park in a given year.

    Args:
        dataset (list): The full dataset.
        park (str): Park name.
        year (int): Year as an integer.

    Returns:
        float or None: The average rating, or None if no matching reviews.
    """
    ratings = [
        row["Rating"] for row in dataset
        if row.get("Branch", "").strip().lower() == park.strip().lower()
        and row.get("Year_Month", "").startswith(str(year))
        and isinstance(row.get("Rating"), int)
    ]
    return sum(ratings) / len(ratings) if ratings else None


def average_rating_by_park_and_location(dataset):
    """
    Compute the average rating per park per reviewer location.

    Args:
        dataset (list): The full dataset.

    Returns:
        dict: Nested dict { park: { location: avg_rating } }
    """
    totals = {}
    counts = {}

    for row in dataset:
        park = row.get("Branch", "").strip()
        location = row.get("Reviewer_Location", "").strip()
        rating = row.get("Rating")

        if not park or not location or not isinstance(rating, int):
            continue

        totals.setdefault(park, {}).setdefault(location, 0)
        counts.setdefault(park, {}).setdefault(location, 0)
        totals[park][location] += rating
        counts[park][location] += 1

    averages = {}
    for park, locations in totals.items():
        averages[park] = {
            loc: totals[park][loc] / counts[park][loc]
            for loc in locations
        }
    return averages


def count_reviews_per_park(dataset):
    """
    Count total reviews received by each park.

    Args:
        dataset (list): The full dataset.

    Returns:
        dict: { park_name: count }
    """
    counts = {}
    for row in dataset:
        park = row.get("Branch", "").strip()
        if park:
            counts[park] = counts.get(park, 0) + 1
    return counts


def top_locations_by_avg_rating(dataset, park, top_n=10):
    """
    Find the top N locations that gave the highest average rating for a park.

    Args:
        dataset (list): The full dataset.
        park (str): Park name.
        top_n (int): Number of top locations to return.

    Returns:
        list: List of (location, avg_rating) tuples, sorted descending.
    """
    totals = {}
    counts = {}
    for row in dataset:
        if row.get("Branch", "").strip().lower() != park.strip().lower():
            continue
        location = row.get("Reviewer_Location", "").strip()
        rating = row.get("Rating")
        if not location or not isinstance(rating, int):
            continue
        totals[location] = totals.get(location, 0) + rating
        counts[location] = counts.get(location, 0) + 1

    averages = {loc: totals[loc] / counts[loc] for loc in totals}
    sorted_avgs = sorted(averages.items(), key=lambda x: x[1], reverse=True)
    return sorted_avgs[:top_n]


def avg_rating_by_month(dataset, park):
    """
    Compute the average rating per calendar month for a given park.

    Args:
        dataset (list): The full dataset.
        park (str): Park name.

    Returns:
        dict: { month_int: avg_rating } for months 1-12 that have data.
    """
    totals = {}
    counts = {}
    for row in dataset:
        if row.get("Branch", "").strip().lower() != park.strip().lower():
            continue
        year_month = row.get("Year_Month", "")
        rating = row.get("Rating")
        if not isinstance(rating, int):
            continue
        try:
            month = int(year_month.split("-")[1])
        except (IndexError, ValueError):
            continue
        totals[month] = totals.get(month, 0) + rating
        counts[month] = counts.get(month, 0) + 1

    return {month: totals[month] / counts[month] for month in totals}


def get_unique_parks(dataset):
    """
    Return a sorted list of unique park names in the dataset.

    Args:
        dataset (list): The full dataset.

    Returns:
        list: Sorted list of unique park name strings.
    """
    return sorted({row.get("Branch", "").strip() for row in dataset if row.get("Branch")})


def aggregate_park_stats(dataset):
    """
    Build aggregate statistics per park for the export feature.

    Returns a list of dicts with keys:
        park, total_reviews, positive_reviews, avg_rating, country_count

    A 'positive' review is defined as rating >= 4.

    Args:
        dataset (list): The full dataset.

    Returns:
        list: List of aggregate stat dictionaries.
    """
    stats = {}
    for row in dataset:
        park = row.get("Branch", "").strip()
        rating = row.get("Rating")
        location = row.get("Reviewer_Location", "").strip()

        if not park or not isinstance(rating, int):
            continue

        if park not in stats:
            stats[park] = {
                "park": park,
                "total_reviews": 0,
                "positive_reviews": 0,
                "rating_sum": 0,
                "countries": set(),
            }

        stats[park]["total_reviews"] += 1
        stats[park]["rating_sum"] += rating
        if rating >= 4:
            stats[park]["positive_reviews"] += 1
        if location:
            stats[park]["countries"].add(location)

    result = []
    for park_data in stats.values():
        total = park_data["total_reviews"]
        result.append({
            "park": park_data["park"],
            "total_reviews": total,
            "positive_reviews": park_data["positive_reviews"],
            "avg_rating": round(park_data["rating_sum"] / total, 2) if total else 0,
            "country_count": len(park_data["countries"]),
        })
    return result
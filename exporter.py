

import csv
import json


class Exporter:
    """
    Abstract base class for exporting park aggregate statistics.

    Subclasses must implement the export() method.
    """

    def __init__(self, stats, filename):
        """
        Initialise the exporter.

        Args:
            stats (list): List of park aggregate stat dicts produced by
                          process.aggregate_park_stats().
            filename (str): Output file path (without extension).
        """
        self._stats = stats
        self._filename = filename

    def export(self):
        """Perform the export. Must be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement export().")

    def _get_filepath(self, extension):
        """
        Build the full output file path.

        Args:
            extension (str): File extension (e.g. 'txt', 'csv', 'json').

        Returns:
            str: The complete filepath.
        """
        return f"{self._filename}.{extension}"


class TXTExporter(Exporter):
    """Exports park statistics to a plain-text (.txt) file."""

    def export(self):
        """Write aggregate stats to a .txt file."""
        filepath = self._get_filepath("txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Disneyland Reviews – Park Aggregate Statistics\n")
            f.write("=" * 50 + "\n\n")
            for park_data in self._stats:
                f.write(f"Park:              {park_data['park']}\n")
                f.write(f"Total Reviews:     {park_data['total_reviews']}\n")
                f.write(f"Positive Reviews:  {park_data['positive_reviews']}\n")
                f.write(f"Average Rating:    {park_data['avg_rating']:.2f}\n")
                f.write(f"Countries:         {park_data['country_count']}\n")
                f.write("-" * 50 + "\n")
        print(f"Data exported to {filepath}")
        return filepath


class CSVExporter(Exporter):
    """Exports park statistics to a CSV (.csv) file."""

    def export(self):
        """Write aggregate stats to a .csv file."""
        filepath = self._get_filepath("csv")
        fieldnames = ["park", "total_reviews", "positive_reviews", "avg_rating", "country_count"]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for park_data in self._stats:
                writer.writerow({
                    "park": park_data["park"],
                    "total_reviews": park_data["total_reviews"],
                    "positive_reviews": park_data["positive_reviews"],
                    "avg_rating": park_data["avg_rating"],
                    "country_count": park_data["country_count"],
                })
        print(f"Data exported to {filepath}")
        return filepath


class JSONExporter(Exporter):
    """Exports park statistics to a JSON (.json) file."""

    def export(self):
        """Write aggregate stats to a .json file."""
        filepath = self._get_filepath("json")
        exportable = [
            {
                "park": d["park"],
                "total_reviews": d["total_reviews"],
                "positive_reviews": d["positive_reviews"],
                "avg_rating": d["avg_rating"],
                "country_count": d["country_count"],
            }
            for d in self._stats
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(exportable, f, indent=4)
        print(f"Data exported to {filepath}")
        return filepath


def create_exporter(export_format, stats, filename="park_stats"):
    """
    Factory function – returns the correct Exporter subclass instance.

    Args:
        export_format (str): One of 'TXT', 'CSV', or 'JSON'.
        stats (list): Aggregate
      Args:
        export_format (str): One of 'TXT', 'CSV', or 'JSON'.
        stats (list): Aggregate stats from process.aggregate_park_stats().
        filename (str): Base filename without extension.

    Returns:
        Exporter: An instance of the appropriate subclass.

    Raises:
        ValueError: If export_format is not recognised.
    """
    format_map = {
        "TXT": TXTExporter,
        "CSV": CSVExporter,
        "JSON": JSONExporter,
    }
    cls = format_map.get(export_format.upper())
    if cls is None:
        raise ValueError(f"Unknown export format: {export_format}")
    return cls(stats, filename)  
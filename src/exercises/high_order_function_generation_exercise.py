"""
Utilities to work with iterables: `count` to count elements matching a predicate
and `average` to compute the mean of a numeric iterable.

This module also contains a small CLI demo (guarded by __name__ == "__main__")
that reads a CSV named '1kSalesRec.csv' placed in a sibling 'data' folder
(next to the 'exercises' folder). Using Path(__file__).resolve() ensures the
CSV path is built relative to this source file rather than the current working
directory, avoiding OS / cwd conflicts.
"""

import csv
from pathlib import Path
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def count(predicate: Callable[[T], bool], iterable: Iterable[T]) -> int:
    """
    Count how many items in `iterable` satisfy `predicate`.

    Uses an iterator-friendly approach (no intermediate list is used).
    """
    return sum(1 for item in iterable if predicate(item))


def average(itr: Iterable[float]) -> float:
    """
    Compute the average (mean) of the numeric iterable `itr`.

    Raises:
        ValueError: if the iterable is empty (no elements to average).
    """
    total = 0.0
    n = 0
    for x in itr:
        total += x
        n += 1
    if n == 0:
        raise ValueError("average() arg is an empty iterable")
    return total / n


# Example/demo code is executed only when running the module directly.
if __name__ == "__main__":
    # Resolve this file's path (safe with symlinks) and build the data file path
    # Data file is expected at: <repo>/src/data/1kSalesRec.csv when this file is at
    # src/exercises/...
    repo_src_dir = Path(__file__).resolve().parent.parent  # points to src/
    csv_path = repo_src_dir / "data" / "1kSalesRec.csv"

    print(f"Reading CSV file from: {csv_path}")

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
    else:
        # Open CSV and demonstrate `count` and `average`.
        with csv_path.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar="|")

            # Remove header row so subsequent processing works with data rows only.
            header = next(reader, None)

            # Count rows where country (assumed at index 1) equals "Belgium".
            # Note: `reader` is an iterator; it will be consumed once.
            count_belgium = count(
                lambda row: len(row) > 1 and row[1] == "Belgium", reader
            )
            print(f"Belgium rows: {count_belgium}")

            # Reset reader by reopening file to iterate again.
            csvfile.seek(0)
            reader = csv.reader(csvfile, delimiter=",", quotechar="|")
            header = next(reader, None)

            # Compute average of column index 13 (converted to float) for rows where
            # country (index 1) == "Portugal". Guard conversions and missing columns.
            portugal_values = (
                float(row[13])
                for row in reader
                if len(row) > 13 and row[13].strip() != "" and row[1] == "Portugal"
            )

            try:
                avg_portugal = average(portugal_values)
                print(f"Average (Portugal, col 13): {avg_portugal:.2f}")
            except ValueError:
                print("No Portugal rows found or no numeric values in column 13.")

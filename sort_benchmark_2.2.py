import statistics
import time
import random
import csv
from pathlib import Path

from dsa.sorting import (
    bubble_sort,
    insertion_sort,
    selection_sort
)


SIZES = [1000, 5000, 10000]
REPEATS = 3


def measure_sort(sort_function, values):
    """Return median execution time in milliseconds."""
    measurements = []

    for _ in range(REPEATS):
        data = list(values)

        start = time.perf_counter()
        sort_function(data)
        end = time.perf_counter()

        measurements.append((end - start) * 1000)

    return statistics.median(measurements)


def main():
    results = []

    random_generator = random.Random(42)

    print("=" * 75)
    print("LIBRARYHUB - PHASE 2.2 SORTING BENCHMARK")
    print("=" * 75)

    print(f"Repeats: {REPEATS}")
    print()

    for size in SIZES:
        print(f"Benchmarking {size:,} titles...")

        titles = [
            f"Book {number:06d}"
            for number in range(size)
        ]

        random_generator.shuffle(titles)

        bubble_time = measure_sort(
            lambda data: bubble_sort(
                data,
                show_passes=False
            ),
            titles
        )

        insertion_time = measure_sort(
            lambda data: insertion_sort(
                data,
                show_passes=False
            ),
            titles
        )

        selection_time = measure_sort(
            lambda data: selection_sort(
                data,
                show_passes=False
            ),
            titles
        )

        python_time = measure_sort(
            lambda data: sorted(data),
            titles
        )

        row = {
            "size": size,
            "bubble_sort_ms": bubble_time,
            "insertion_sort_ms": insertion_time,
            "selection_sort_ms": selection_time,
            "python_sorted_ms": python_time
        }

        results.append(row)

        print(f"Bubble sort:    {bubble_time:.3f} ms")
        print(f"Insertion sort: {insertion_time:.3f} ms")
        print(f"Selection sort: {selection_time:.3f} ms")
        print(f"Python sorted:  {python_time:.3f} ms")
        print()

    csv_path = (
        Path(__file__).resolve().parent
        / "phase2_2_sort_results.csv"
    )

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("=" * 75)
    print("SORTING BENCHMARK COMPLETED")
    print("=" * 75)

    print(
        f"{'Size':<12}"
        f"{'Bubble':<15}"
        f"{'Insertion':<15}"
        f"{'Selection':<15}"
        f"{'Python sorted':<15}"
    )

    for row in results:
        print(
            f"{row['size']:<12}"
            f"{row['bubble_sort_ms']:<15.3f}"
            f"{row['insertion_sort_ms']:<15.3f}"
            f"{row['selection_sort_ms']:<15.3f}"
            f"{row['python_sorted_ms']:<15.3f}"
        )

    print(f"\nCSV saved: {csv_path.name}")


if __name__ == "__main__":
    main()
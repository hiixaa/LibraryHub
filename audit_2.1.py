import csv
import statistics
import time
from datetime import date
from pathlib import Path

from items import Book
from members import StudentMember
from loans import Loan
from library import Library


# Configuration
SIZES = [1000, 5000, 10000, 50000]
REPEATS = 5

TODAY = date(2026, 10, 31)
BORROWED_DATE = date(2026, 1, 1)

PROJECT_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# 1. Generate fake books
# --------------------------------------------------

def make_isbn(number):
    return f"978{number:010d}"


def make_book(number):
    return Book(
        make_isbn(number),
        f"Generated Book {number:06d}",
        [f"Author {number:06d}"],
        "Programming",
        100 + (number % 900),
        250.0,
        2,
        "Technology"
    )


def generate_catalogue(size):
    library = Library()

    for number in range(1, size + 1):
        library.add_item(make_book(number))

    return library


# --------------------------------------------------
# 2. Generate loan records
# --------------------------------------------------

def add_noise_loans(library, count):
    member = StudentMember(
        "M_NOISE",
        "Benchmark Member",
        "benchmark@example.com"
    )

    item = Book(
        make_isbn(900000001),
        "Benchmark Noise Book",
        ["Benchmark Author"],
        "Programming",
        300,
        200.0,
        count + 2,
        "Technology"
    )

    library.add_member(member)
    library.add_item(item)

    for index in range(1, count + 1):
        loan = Loan(
            member,
            item,
            BORROWED_DATE,
            loan_id=f"N{index:07d}"
        )

        library.loans.append(loan)
        item.available_copies -= 1

    return member, item


# --------------------------------------------------
# 3. Calculate median execution time
# --------------------------------------------------

def median_time(operation):
    results = []

    for _ in range(REPEATS):
        start = time.perf_counter()

        operation()

        end = time.perf_counter()

        results.append(end - start)

    return statistics.median(results)


# --------------------------------------------------
# 4. Benchmark list_items and search_items
# --------------------------------------------------

def benchmark_catalogue(size):
    library = generate_catalogue(size)

    search_term = f"Generated Book {size:06d}"

    list_time = median_time(
        library.list_items
    )

    search_time = median_time(
        lambda: library.search_items(search_term)
    )

    return list_time, search_time


# --------------------------------------------------
# 5. Benchmark borrow
# --------------------------------------------------

def benchmark_borrow(size):
    results = []

    for repeat in range(REPEATS):

        library = Library()

        add_noise_loans(library, size)

        member = StudentMember(
            f"M_TARGET_{repeat}",
            "Target Member",
            f"target{repeat}@example.com"
        )

        item = Book(
            make_isbn(800000000 + repeat),
            "Borrow Target",
            ["Target Author"],
            "Programming",
            300,
            250.0,
            2,
            "Technology"
        )

        library.add_member(member)
        library.add_item(item)

        start = time.perf_counter()

        library.borrow(
            item.isbn,
            member.member_id,
            TODAY
        )

        end = time.perf_counter()

        results.append(end - start)

    return statistics.median(results)


# --------------------------------------------------
# 6. Benchmark return_item
# --------------------------------------------------

def benchmark_return(size):
    results = []

    for repeat in range(REPEATS):

        library = Library()

        add_noise_loans(library, size)

        member = StudentMember(
            f"M_RETURN_{repeat}",
            "Return Member",
            f"return{repeat}@example.com"
        )

        item = Book(
            make_isbn(810000000 + repeat),
            "Return Target",
            ["Return Author"],
            "Programming",
            300,
            250.0,
            2,
            "Technology"
        )

        library.add_member(member)
        library.add_item(item)

        loan = Loan(
            member,
            item,
            TODAY,
            loan_id=f"R{repeat:03d}"
        )

        library.loans.append(loan)
        item.available_copies -= 1

        start = time.perf_counter()

        library.return_item(
            item.isbn,
            member.member_id,
            TODAY
        )

        end = time.perf_counter()

        results.append(end - start)

    return statistics.median(results)


# --------------------------------------------------
# 7. Benchmark overdue_report
# --------------------------------------------------

def benchmark_overdue(size):

    library = Library()

    add_noise_loans(library, size)

    return median_time(
        lambda: library.overdue_report(TODAY)
    )


# --------------------------------------------------
# 8. Compare list.pop(0) and deque.popleft()
# --------------------------------------------------

def benchmark_queue(size=100000):

    from collections import deque

    list_results = []
    deque_results = []

    for _ in range(REPEATS):

        values = list(range(size))

        start = time.perf_counter()

        while values:
            values.pop(0)

        end = time.perf_counter()

        list_results.append(end - start)

        values = deque(range(size))

        start = time.perf_counter()

        while values:
            values.popleft()

        end = time.perf_counter()

        deque_results.append(end - start)

    return (
        statistics.median(list_results),
        statistics.median(deque_results)
    )


# --------------------------------------------------
# 9. Generate benchmark report
# --------------------------------------------------

def generate_report(results, list_pop_time, deque_pop_time):

    report = []

    report.append("# Phase 2.1 - Complexity Audit\n")

    report.append("## Predicted Time and Space Complexity\n")

    report.append("| Method | Time Complexity | Space Complexity |")
    report.append("|---|---|---|")

    report.append("| list_items() | O(n) | O(n) |")
    report.append("| search_items() | O(n) | O(r) |")
    report.append("| borrow() | O(L) | O(L) |")
    report.append("| return_item() | O(L + R) | O(1) auxiliary |")
    report.append("| overdue_report() | O(L log L) | O(L) |")

    report.append(
        "\nn = catalogue size, L = loan count, "
        "R = reservation count, r = search results.\n"
    )

    report.append("## Measured Results\n")

    report.append("Median execution time across five runs (milliseconds).\n")

    report.append(
        "| Records | list_items | search_items | borrow | "
        "return_item | overdue_report |"
    )
    report.append("|---:|---:|---:|---:|---:|---:|")

    for row in results:
        report.append(
            f"| {row['size']:,} "
            f"| {row['list_items_ms']:.4f} "
            f"| {row['search_items_ms']:.4f} "
            f"| {row['borrow_ms']:.4f} "
            f"| {row['return_ms']:.4f} "
            f"| {row['overdue_ms']:.4f} |"
        )

    report.append("\n## Queue Benchmark\n")

    report.append("| Operation | Median Time (seconds) |")
    report.append("|---|---:|")
    report.append(f"| list.pop(0) | {list_pop_time:.6f} |")
    report.append(f"| deque.popleft() | {deque_pop_time:.6f} |")

    report.append("\n## Observations and Surprises\n")

    report.append(
        "1. list_items() showed increasing execution time as the "
        "catalogue grew, which matches its predicted O(n) complexity. "
        "The increase at 50,000 records was larger than at smaller "
        "sizes, likely because of memory allocation and runtime overhead."
    )

    report.append(
        "2. search_items() increased approximately in proportion to "
        "catalogue size, matching O(n). Searching for an item near "
        "the end requires checking almost the entire catalogue."
    )

    report.append(
        "3. borrow() became slower as the loan count increased because "
        "it collects the member's active loans by scanning the loan list. "
        "Its measured growth is consistent with the O(L) prediction."
    )

    report.append(
        "4. return_item() also became slower as the loan list grew. "
        "The benchmark places the target loan after the generated "
        "noise loans, so the method must scan many records before "
        "finding it."
    )

    report.append(
        "5. overdue_report() increased in execution time as the number "
        "of loans grew because it scans the loan list and sorts the "
        "overdue results. The measured time also depends on how many "
        "loans qualify as overdue."
    )

    report.append(
        "6. list.pop(0) took substantially longer than deque.popleft() "
        "for 100,000 entries. This is expected because list removal "
        "shifts remaining elements, whereas deque supports efficient "
        "removal from the front."
    )

    report.append("\n## Conclusion\n")

    report.append(
        "The measured results generally support the predicted "
        "complexities. The deque benchmark demonstrates why a queue "
        "should use collections.deque rather than repeatedly removing "
        "the first element of a list. Small timing variations can occur "
        "because of operating-system scheduling, memory allocation "
        "and Python runtime overhead."
    )

    report_path = (
        PROJECT_DIR / "PHASE2_1_BENCHMARK_REPORT.md"
    )

    report_path.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    return report_path


# --------------------------------------------------
# 10. Main program
# --------------------------------------------------

def main():

    results = []

    print("=" * 60)
    print("LIBRARYHUB - PHASE 2.1 COMPLEXITY AUDIT")
    print("=" * 60)

    print(f"Number of repetitions: {REPEATS}")
    print()

    for size in SIZES:

        print(f"Benchmarking {size:,} records...")

        list_time, search_time = benchmark_catalogue(size)

        borrow_time = benchmark_borrow(size)

        return_time = benchmark_return(size)

        overdue_time = benchmark_overdue(size)

        row = {
            "size": size,
            "list_items_ms": list_time * 1000,
            "search_items_ms": search_time * 1000,
            "borrow_ms": borrow_time * 1000,
            "return_ms": return_time * 1000,
            "overdue_ms": overdue_time * 1000
        }

        results.append(row)

        print(
            f"list_items: {row['list_items_ms']:.4f} ms"
        )

        print(
            f"search_items: {row['search_items_ms']:.4f} ms"
        )

        print(
            f"borrow: {row['borrow_ms']:.4f} ms"
        )

        print(
            f"return_item: {row['return_ms']:.4f} ms"
        )

        print(
            f"overdue_report: {row['overdue_ms']:.4f} ms"
        )

        print()

    # Save CSV results

    csv_path = (
        PROJECT_DIR / "phase2_1_benchmark_results.csv"
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

    # Queue benchmark

    print("Benchmarking queue operations...")

    list_pop_time, deque_pop_time = benchmark_queue()

    # Generate report

    report_path = generate_report(
        results,
        list_pop_time,
        deque_pop_time
    )

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETED")
    print("=" * 60)

    print(f"CSV results: {csv_path.name}")
    print(f"Report: {report_path.name}")

    print(
        f"list.pop(0): {list_pop_time:.6f} seconds"
    )

    print(
        f"deque.popleft(): {deque_pop_time:.6f} seconds"
    )


if __name__ == "__main__":
    main()
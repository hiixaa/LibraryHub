def bubble_sort(values, key=None, show_passes=True):
    """Sort values using bubble sort."""
    result = list(values)
    get_key = key if key is not None else lambda value: value

    for pass_number in range(len(result) - 1):
        for index in range(len(result) - pass_number - 1):
            if get_key(result[index]) > get_key(result[index + 1]):
                result[index], result[index + 1] = (
                    result[index + 1],
                    result[index]
                )

        if show_passes:
            print(f"  after pass {pass_number + 1}: {result}")

    return result


def insertion_sort(values, key=None, show_passes=True):
    """Sort values using insertion sort."""
    result = list(values)
    get_key = key if key is not None else lambda value: value

    for index in range(1, len(result)):
        current = result[index]
        position = index - 1

        while (
            position >= 0
            and get_key(result[position]) > get_key(current)
        ):
            result[position + 1] = result[position]
            position -= 1

        result[position + 1] = current

        if show_passes:
            print(
                f"  after inserting index {index}: {result}"
            )

    return result


def selection_sort(values, key=None, show_passes=True):
    """Sort values using selection sort."""
    result = list(values)
    get_key = key if key is not None else lambda value: value

    for index in range(len(result) - 1):
        minimum_index = index

        for position in range(index + 1, len(result)):
            if (
                get_key(result[position])
                < get_key(result[minimum_index])
            ):
                minimum_index = position

        result[index], result[minimum_index] = (
            result[minimum_index],
            result[index]
        )

        if show_passes:
            print(
                f"  after pass {index + 1} "
                f"(min={result[index]}): {result}"
            )

    return result


def top_level_category(item):
    """Return the top-level category for an item."""
    if item.parent_category:
        return item.parent_category

    category = item.category.strip()

    if category in ("Programming", "Software Engineering"):
        return "Technology"

    return category


def catalogue_sort(items):
    """
    Sort catalogue by:
    1. Top-level category ascending
    2. Pages descending
    3. Title ascending
    """
    return sorted(
        items,
        key=lambda item: (
            top_level_category(item).casefold(),
            -item.pages,
            item.title.casefold()
        )
    )


def print_catalogue(items):
    """Print catalogue in the required format."""
    for item in items:
        category = top_level_category(item)

        print(
            f"{category:<12}"
            f"{item.title:<30}"
            f"{item.pages:>5}"
        )


if __name__ == "__main__":

    numbers = [5, 2, 4, 1]

    print("bubble_sort([5, 2, 4, 1])")
    bubble_sort(numbers)

    print("\ninsertion_sort([5, 2, 4, 1])")
    insertion_sort(numbers)

    print("\nselection_sort([5, 2, 4, 1])")
    selection_sort(numbers)
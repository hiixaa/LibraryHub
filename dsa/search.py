def linear_search_by_title(items, title):
    """
    Search titles linearly.
    Returns the index of the first matching title, or -1.
    Matching is case-insensitive and exact.
    """
    target = title.strip().casefold()

    for index, item in enumerate(items):
        if item.title.casefold() == target:
            return index

    return -1


def binary_search(isbns, target_isbn):
    """
    Search a sorted ISBN list using binary search.

    Returns:
        (index, comparisons)

    If not found, index is -1.
    """
    low = 0
    high = len(isbns) - 1
    comparisons = 0

    while low <= high:
        middle = (low + high) // 2
        comparisons += 1

        if isbns[middle] == target_isbn:
            return middle, comparisons

        if isbns[middle] < target_isbn:
            low = middle + 1
        else:
            high = middle - 1

    return -1, comparisons